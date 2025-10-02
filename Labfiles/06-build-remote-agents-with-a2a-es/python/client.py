""" Código cliente que se conecta al agente de enrutamiento """

import os
import asyncio
import requests
from dotenv import load_dotenv

load_dotenv()

server = os.environ["SERVER_URL"]
port = os.environ["ROUTING_AGENT_PORT"]

def send_prompt(prompt: str):
    url = f"http://{server}:{port}/message"
    payload = {"message": prompt}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "Sin respuesta del agente.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Solicitud fallida: {e}"

async def main():
    print("Ingresa un prompt para el agente. Escribe 'quit' para salir.")
    while True:
        user_input = input("Usuario: ")
        if user_input.lower() == "quit":
            print("¡Adiós!")
            break
        response = send_prompt(user_input)
        print(f"Agente: {response}")

if __name__ == "__main__":
    asyncio.run(main())

