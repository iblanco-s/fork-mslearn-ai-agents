import os
from dotenv import load_dotenv
from typing import Any
from pathlib import Path


# Agregar referencias

def main(): 

    # Limpiar la consola
    os.system('cls' if os.name=='nt' else 'clear')

    # Cargar variables de entorno desde el archivo .env
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


    # Conectar al cliente del Agente
    


    # Definir un agente que puede usar las funciones personalizadas


    
        # Bucle hasta que el usuario escriba 'quit'
        while True:
            # Obtener texto de entrada
            user_prompt = input("Ingresa un prompt (o escribe 'quit' para salir): ")
            if user_prompt.lower() == "quit":
                break
            if len(user_prompt) == 0:
                print("Por favor ingresa un prompt.")
                continue

            # Enviar un prompt al agente


            # Verificar el estado de ejecución por fallos

                
            # Mostrar la última respuesta del agente


        # Obtener el historial de conversación


        # Limpiar

    



if __name__ == '__main__': 
    main()

