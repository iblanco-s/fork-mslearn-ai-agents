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
from outline_agent.agent_executor import create_foundry_agent_executor

load_dotenv()

host = os.environ["SERVER_URL"]
port = os.environ["OUTLINE_AGENT_PORT"]

# Definir habilidades del agente
skills = [
    AgentSkill(
        id='generate_blog_outline',
        name='Generate Blog Outline',
        description='Genera un esquema de blog basado en un título',
        tags=['outline'],
        examples=[
            '¿Puedes darme un esquema para este artículo?',
        ],
    ),
]

# Crear tarjeta del agente
agent_card = AgentCard(
    name='AI Foundry Outline Agent',
    description='Un agente generador de esquemas inteligente potenciado por Azure AI Foundry. '
    'Puedo ayudarte a generar esquemas estructurados para tus artículos.',
    url=f'http://{host}:{port}/',
    version='1.0.0',
    default_input_modes=['text'],
    default_output_modes=['text'],
    capabilities=AgentCapabilities(),
    skills=skills,
)

# Crear ejecutor del agente
agent_executor = create_foundry_agent_executor(agent_card)

# Crear manejador de solicitudes
request_handler = DefaultRequestHandler(
    agent_executor=agent_executor, task_store=InMemoryTaskStore()
)

# Crear aplicación A2A
a2a_app = A2AStarletteApplication(
    agent_card=agent_card, http_handler=request_handler
)

# Obtener rutas
routes = a2a_app.routes()

# Agregar endpoint de verificación de salud
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse('¡El Agente de Esquema de AI Foundry está en ejecución!')

routes.append(Route(path='/health', methods=['GET'], endpoint=health_check))

# Crear aplicación Starlette
app = Starlette(routes=routes)

def main():
    # Ejecutar el servidor
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    main()


