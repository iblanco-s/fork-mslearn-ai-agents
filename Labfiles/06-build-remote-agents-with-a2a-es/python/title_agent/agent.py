""" Agente de Azure AI Foundry que genera un título """

import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import Agent, ListSortOrder, MessageRole

class TitleAgent:

    def __init__(self):

        # Crear el cliente de agentes


        self.agent: Agent | None = None

    async def create_agent(self) -> Agent:
        if self.agent:
            return self.agent

        # Crear el agente de título


        return self.agent
        
    async def run_conversation(self, user_message: str) -> list[str]:
        # Agregar un mensaje al hilo, procesarlo y recuperar la respuesta

        if not self.agent:
            await self.create_agent()

        # Crear un hilo para la sesión de chat


        # Enviar mensaje del usuario
        

        # Crear y ejecutar el agente


        if run.status == 'failed':
            print(f'Agente de Título: Ejecución fallida - {run.last_error}')
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

async def create_foundry_title_agent() -> TitleAgent:
    agent = TitleAgent()
    await agent.create_agent()
    return agent

