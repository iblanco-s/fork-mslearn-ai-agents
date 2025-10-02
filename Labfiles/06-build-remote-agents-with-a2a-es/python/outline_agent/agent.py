""" Agente de Azure AI Foundry que genera un esquema """

import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import Agent, ListSortOrder, MessageRole

class OutlineAgent:

    def __init__(self):

        # Crear el cliente de agentes
        self.client = AgentsClient(
            endpoint=os.environ['PROJECT_ENDPOINT'],
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            )
        )

        self.agent: Agent | None = None

    async def create_agent(self) -> Agent:
        if self.agent:
            return self.agent

        # Crear el agente de esquema
        self.agent = self.client.create_agent(
            model=os.environ['MODEL_DEPLOYMENT_NAME'],
            name='outline-agent',
            instructions="""
            Eres un asistente útil de escritura.
            Dado un título de publicación de blog, sugiere un esquema breve y estructurado con 3-5 puntos principales.
            """,
        )

        return self.agent
        
    async def run_conversation(self, user_message: str) -> list[str]:
        # Agregar un mensaje al hilo, procesarlo y recuperar la respuesta

        if not self.agent:
            await self.create_agent()

        # Crear un hilo para la sesión de chat
        thread = self.client.threads.create()

        # Enviar mensaje del usuario
        self.client.messages.create(thread_id=thread.id, role=MessageRole.USER, content=user_message)

        # Crear y ejecutar el agente
        run = self.client.runs.create_and_process(thread_id=thread.id, agent_id=self.agent.id)

        if run.status == 'failed':
            print(f'Agente de Esquema: Ejecución fallida - {run.last_error}')
            return [f'Error: {run.last_error}']

        # Obtener mensajes de respuesta
        messages = self.client.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING)
        responses = []
        for msg in messages:
            # Solo obtener la última respuesta del asistente
            if msg.role == MessageRole.AGENT and msg.text_messages:
                for text_msg in msg.text_messages:
                    responses.append(text_msg.text.value)
                break 

        return responses if responses else ['No se recibió respuesta']

async def create_foundry_outline_agent() -> OutlineAgent:
    agent = OutlineAgent()
    await agent.create_agent()
    return agent

