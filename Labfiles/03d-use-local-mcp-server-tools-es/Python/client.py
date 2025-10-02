import os, time
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
# Agregar referencias


# Limpiar la consola
os.system('cls' if os.name=='nt' else 'clear')

# Cargar variables de entorno desde el archivo .env
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

async def connect_to_server(exit_stack: AsyncExitStack):
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    # Iniciar el servidor MCP
    
    # Crear una sesión de cliente MCP

    # Listar herramientas disponibles

    return session

async def chat_loop(session):

    # Conectar al cliente de agentes
    

    # Listar herramientas disponibles en el servidor
    

    # Construir una función para cada herramienta
    

    # Crear el agente
    

    # Habilitar llamada automática de funciones
    

    # Crear un hilo para la sesión de chat
    

    while True:
        user_input = input("Ingresa un prompt para el agente de inventario. Usa 'quit' para salir.\nUSUARIO: ").strip()
        if user_input.lower() == "quit":
            print("Saliendo del chat.")
            break

        # Invocar el prompt


        # Monitorear el estado de ejecución
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
            tool_outputs = []

            if run.status == "requires_action":

                tool_calls = run.required_action.submit_tool_outputs.tool_calls

                for tool_call in tool_calls:

                    # Recuperar la herramienta de función coincidente
                    

                    # Agregar el texto de salida
                    
                
                # Enviar la salida de la llamada a herramienta
                
        # Verificar fallas
        if run.status == "failed":
            print(f"Ejecución fallida: {run.last_error}")

        # Mostrar la respuesta
        

    # Eliminar el agente cuando termine
    print("Limpiando agentes:")
    agents_client.delete_agent(agent.id)
    print("Agente de inventario eliminado.")


async def main():
    import sys
    exit_stack = AsyncExitStack()
    try:
        session = await connect_to_server(exit_stack)
        await chat_loop(session)
    finally:
        await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(main())

