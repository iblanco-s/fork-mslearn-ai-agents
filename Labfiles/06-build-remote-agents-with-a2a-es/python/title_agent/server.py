import os
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from title_agent.agent_executor import create_foundry_agent_executor

load_dotenv()

host = os.environ["SERVER_URL"]
port = os.environ["TITLE_AGENT_PORT"]

# Definir habilidades del agente


# Crear tarjeta del agente


# Crear ejecutor del agente


# Crear manejador de solicitudes


# Crear aplicación A2A


# Obtener rutas
routes = a2a_app.routes()

# Agregar endpoint de verificación de salud
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse('¡El Agente de Título de AI Foundry está en ejecución!')

routes.append(Route(path='/health', methods=['GET'], endpoint=health_check))

# Crear aplicación Starlette
app = Starlette(routes=routes)

def main():
    # Ejecutar el servidor
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    main()


