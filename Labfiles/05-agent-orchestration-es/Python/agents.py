# Agregar referencias


async def main():
    # Instrucciones del agente
    summarizer_instructions="""
    Resume los comentarios del cliente en una oración corta. Manténlo neutral y conciso.
    Ejemplo de salida:
    La aplicación se bloquea durante la carga de fotos.
    El usuario elogia la función de modo oscuro.
    """

    classifier_instructions="""
    Clasifica los comentarios como uno de los siguientes: Positivo, Negativo, o Solicitud de característica.
    """

    action_instructions="""
    Basado en el resumen y la clasificación, sugiere la siguiente acción en una oración corta.
    Ejemplo de salida:
    Escalar como un error de alta prioridad para el equipo móvil.
    Registrar como comentario positivo para compartir con diseño y marketing.
    Registrar como solicitud de mejora para el backlog del producto.
    """

    # Crear el cliente de chat
    

    # Crear agentes
    

    # Inicializar los comentarios actuales
    

    # Construir orquestación secuencial
    
    
    # Ejecutar y recopilar salidas
    
    
    # Mostrar salidas
    
    
    
if __name__ == "__main__":
    asyncio.run(main())
