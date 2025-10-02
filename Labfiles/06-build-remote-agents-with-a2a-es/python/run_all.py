""" Ejecuta cada servidor de agente e inicia el cliente """

import asyncio
import subprocess
import sys
import time
import signal
import httpx
import os
import threading
from dotenv import load_dotenv

load_dotenv()

server_url = os.environ["SERVER_URL"]
servers = [
    {
        "name": "title_agent_server",
        "module": "title_agent.server:app",
        "port": os.environ["TITLE_AGENT_PORT"]
    },
    {
        "name": "outline_agent_server",
        "module": "outline_agent.server:app",
        "port": os.environ["OUTLINE_AGENT_PORT"]
    },
    {
        "name": "routing_agent_server",
        "module": "routing_agent.server:app",
        "port": os.environ["ROUTING_AGENT_PORT"]
    },
]

server_procs = []

async def wait_for_server_ready(server, timeout=30):
    async with httpx.AsyncClient() as client:
        start = time.time()
        while True:
            try:
                health_url = f"http://{server_url}:{server['port']}/health"
                r = await client.get(health_url, timeout=2)
                if r.status_code == 200:
                    print(f"✅ ¡{server['name']} está saludable y listo!")
                    return True
            except Exception:
                pass
            if time.time() - start > timeout:
                print(f"❌ Tiempo de espera agotado esperando salud del servidor en {health_url}")
                return False
            await asyncio.sleep(1)

def stream_subprocess_output(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.rstrip())


async def run_client_main():
    from client import main as client_main
    await client_main()

async def main():
    print("🚀 Iniciando subprocesos de servidor...")
    for server in servers:
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            server["module"],
            "--host",
            server_url,
            "--port",
            str(server["port"]),
            "--log-level",
            "info"
        ]
        
        print(f"🚀 Iniciando {server['name']} en puerto {server['port']}")
        process = subprocess.Popen(
            cmd,
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True,
        )
        server_procs.append(process)

        thread = threading.Thread(target=stream_subprocess_output, args=(process,), daemon=True)
        thread.start()

        ready = await wait_for_server_ready(server)
        if not ready:
            print(f"❌ El servidor '{server['name']}' falló al iniciar, matando proceso...")
            process.kill()
            sys.exit(1)

    try:
        await run_client_main()
    except Exception as e:
        print(f"❌ Cliente detenido: {e}")
    finally:
        print("🛑 Deteniendo subprocesos de servidor...")
        # Terminar el subproceso del servidor elegantemente
        for process in server_procs:
            if process.poll() is None:  # Aún en ejecución
                if sys.platform == "win32":
                    process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

if __name__ == "__main__":
    asyncio.run(main())

