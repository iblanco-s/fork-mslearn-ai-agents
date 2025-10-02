import os
import asyncio
from pathlib import Path

# Agregar referencias



async def main():
    # Limpiar la consola
    os.system('cls' if os.name=='nt' else 'clear')

    # Cargar el archivo de datos de gastos
    script_dir = Path(__file__).parent
    file_path = script_dir / 'data.txt'
    with file_path.open('r') as file:
        data = file.read() + "\n"

    # Solicitar un prompt
    user_prompt = input(f"Aquí están los datos de gastos en tu archivo:\n\n{data}\n\n¿Qué te gustaría que hiciera con ellos?\n\n")
    
    # Ejecutar el código asíncrono del agente
    await process_expenses_data (user_prompt, data)
    
async def process_expenses_data(prompt, expenses_data):

    # Crear un agente de chat
    

        # Usar el agente para procesar los datos de gastos    



# Crear una función de herramienta para la funcionalidad de correo electrónico




if __name__ == "__main__":
    asyncio.run(main())

