---
lab:
    title: 'Desarrollar una solución multi-agente con Microsoft Agent Framework'
    description: 'Aprende a configurar múltiples agentes para colaborar usando el SDK de Microsoft Agent Framework'
---

# Desarrollar una solución multi-agente

En este ejercicio, practicarás el uso del patrón de orquestación secuencial en el SDK de Microsoft Agent Framework. Crearás una pipeline simple de tres agentes que trabajan juntos para procesar comentarios de clientes y sugerir próximos pasos. Crearás los siguientes agentes:

- El agente Resumidor condensará comentarios sin procesar en una oración corta y neutral.
- El agente Clasificador categorizará los comentarios como Positivos, Negativos o una solicitud de Característica.
- Finalmente, el agente de Acción Recomendada recomendará un paso de seguimiento apropiado.

Aprenderás a usar el SDK de Microsoft Agent Framework para descomponer un problema, enrutarlo a través de los agentes correctos y producir resultados accionables. ¡Comencemos!

Este ejercicio debería tomar aproximadamente **30** minutos para completar.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Desplegar un modelo en un proyecto de Azure AI Foundry

Comencemos desplegando un modelo en un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Ayuda** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./Media/ai-foundry-home.png)

1. En la página de inicio, en la sección **Explora modelos y capacidades**, busca el modelo `gpt-4o`; que usaremos en nuestro proyecto.
1. En los resultados de búsqueda, selecciona el modelo **gpt-4o** para ver sus detalles, y luego en la parte superior de la página del modelo, selecciona **Usar este modelo**.
1. Cuando se te solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Opciones avanzadas**.
1. Confirma las siguientes configuraciones para tu proyecto:
    - **Recurso de Azure AI Foundry**: *Un nombre válido para tu recurso de Azure AI Foundry*
    - **Suscripción**: *Tu suscripción de Azure*
    - **Grupo de recursos**: *Crea o selecciona un grupo de recursos*
    - **Región**: *Selecciona cualquiera **recomendada por AI Foundry***\*

    > \* Algunos recursos de Azure AI están limitados por cuotas de modelo regionales. En el caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Crear** y espera a que se cree tu proyecto, incluyendo la implementación del modelo gpt-4 que seleccionaste.

1. Cuando se cree tu proyecto, el playground de chat se abrirá automáticamente.

1. En el panel de navegación a la izquierda, selecciona **Modelos y endpoints** y selecciona tu implementación **gpt-4o**.

1. En el panel **Configuración**, observa el nombre de tu implementación del modelo; que debería ser **gpt-4o**. Puedes confirmar esto viendo la implementación en la página **Modelos y endpoints** (solo abre esa página en el panel de navegación a la izquierda).
1. En el panel de navegación a la izquierda, selecciona **Información general** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de los detalles de un proyecto de IA de Azure en el portal de Azure AI Foundry.](./Media/ai-foundry-project.png)

## Crear una aplicación cliente de Agente de IA

Ahora estás listo para crear una aplicación cliente que define un agente y una función personalizada. Se te ha proporcionado algo de código en un repositorio de GitHub.

### Preparar el entorno

1. Abre una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego en la nueva pestaña, navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con tus credenciales de Azure si se te solicita.

    Cierra cualquier notificación de bienvenida para ver la página de inicio del portal de Azure.

1. Usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno ***PowerShell*** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puedes redimensionar o maximizar este panel para facilitar el trabajo.

    > **Nota**: Si has creado previamente un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Configuración**, selecciona **Ir a la versión Clásica** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pega como texto sin formato):

    ```
   rm -r ai-agents -f
   git clone https://github.com/MicrosoftLearning/mslearn-ai-agents ai-agents
    ```

    > **Consejo**: A medida que ingresas comandos en el cloud shell, la salida puede ocupar una gran cantidad del búfer de pantalla y el cursor en la línea actual puede quedar oculto. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Cuando el repositorio haya sido clonado, ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```
   cd ai-agents/Labfiles/05-agent-orchestration/Python
   ls -a -l
    ```

    Los archivos proporcionados incluyen código de aplicación y un archivo para configuraciones.

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install azure-identity agent-framework
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_openai_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry). Reemplaza el marcador de posición **your_model_deployment** con el nombre que asignaste a tu implementación del modelo gpt-4o.

1. Después de haber reemplazado los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Crear agentes de IA

Ahora estás listo para crear los agentes para tu solución multi-agente! ¡Comencemos!

1. Ingresa el siguiente comando para editar el archivo **agents.py**:

    ```
   code agents.py
    ```

1. En la parte superior del archivo bajo el comentario **Add references**, y agrega el siguiente código para hacer referencia a los espacios de nombres en las bibliotecas que necesitarás para implementar tu agente:

    ```python
   # Add references
   import asyncio
   from typing import cast
   from agent_framework import ChatMessage, Role, SequentialBuilder, WorkflowOutputEvent
   from agent_framework.azure import AzureOpenAIChatClient
   from azure.identity import AzureCliCredential
    ```

1. En la función **main**, tómate un momento para revisar las instrucciones del agente. Estas instrucciones definen el comportamiento de cada agente en la orquestación.

1. Agrega el siguiente código bajo el comentario **Create the chat client**:

    ```python
   # Create the chat client
   chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())
    ```

1. Agrega el siguiente código bajo el comentario **Create agents**:

    ```python
   # Create agents
   summarizer = chat_client.create_agent(
       instructions=summarizer_instructions,
       name="summarizer",
   )

   classifier = chat_client.create_agent(
       instructions=classifier_instructions,
       name="classifier",
   )

   action = chat_client.create_agent(
       instructions=action_instructions,
       name="action",
   )
    ```

## Crear una orquestación secuencial

1. En la función **main**, encuentra el comentario **Initialize the current feedback** y agrega el siguiente código:
    
    ```python
   # Initialize the current feedback
   feedback="""
   I use the dashboard every day to monitor metrics, and it works well overall. 
   But when I'm working late at night, the bright screen is really harsh on my eyes. 
   If you added a dark mode option, it would make the experience much more comfortable.
   """
    ```

1. Bajo el comentario **Build a sequential orchestration**, agrega el siguiente código para definir una orquestación secuencial con los agentes que definiste:

    ```python
   # Build sequential orchestration
    workflow = SequentialBuilder().participants([summarizer, classifier, action]).build()
    ```

    Los agentes procesarán los comentarios en el orden en que se agreguen a la orquestación.

1. Agrega el siguiente código bajo el comentario **Run and collect outputs**:

    ```python
   # Run and collect outputs
   outputs: list[list[ChatMessage]] = []
   async for event in workflow.run_stream(f"Customer feedback: {feedback}"):
       if isinstance(event, WorkflowOutputEvent):
           outputs.append(cast(list[ChatMessage], event.data))
    ```

    Este código ejecuta la orquestación y recopila la salida de cada uno de los agentes participantes.

1. Agrega el siguiente código bajo el comentario **Display outputs**:

    ```python
   # Display outputs
   if outputs:
       for i, msg in enumerate(outputs[-1], start=1):
           name = msg.author_name or ("assistant" if msg.role == Role.ASSISTANT else "user")
           print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
    ```

    Este código formatea y muestra los mensajes de las salidas del flujo de trabajo que recopilaste de la orquestación.

1. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. Puedes mantenerlo abierto (en caso de que necesites editar el código para corregir errores) o usar el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Iniciar sesión en Azure y ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tus agentes de IA colaboran.

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```
   az login
    ```

    **<font color="red">Debes iniciar sesión en Azure - aunque la sesión del cloud shell ya esté autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, simplemente usar *az login* será suficiente. Sin embargo, si tienes suscripciones en varios tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para más detalles.

1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresar el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```
   python agents.py
    ```

    Deberías ver una salida similar a la siguiente:

    ```output
    ------------------------------------------------------------
    01 [user]
    Customer feedback:
        I use the dashboard every day to monitor metrics, and it works well overall.
        But when I'm working late at night, the bright screen is really harsh on my eyes.
        If you added a dark mode option, it would make the experience much more comfortable.

    ------------------------------------------------------------
    02 [summarizer]
    User requests a dark mode for better nighttime usability.
    ------------------------------------------------------------
    03 [classifier]
    Feature request
    ------------------------------------------------------------
    04 [action]
    Log as enhancement request for product backlog.
    ```

1. Opcionalmente, puedes intentar ejecutar el código usando diferentes entradas de comentarios, como:

    ```output
    Uso el tablero todos los días para monitorear métricas, y funciona bien en general. Pero cuando trabajo tarde en la noche, la pantalla brillante es realmente dura para mis ojos. Si agregaran una opción de modo oscuro, haría la experiencia mucho más cómoda.
    ```
    ```output
    Me comuniqué con su servicio al cliente ayer porque no podía acceder a mi cuenta. El representante respondió casi inmediatamente, fue cortés y profesional, y solucionó el problema en minutos. Honestamente, fue una de las mejores experiencias de soporte que he tenido.
    ```

## Resumen

En este ejercicio, practicaste la orquestación secuencial con el SDK de Microsoft Agent Framework, combinando múltiples agentes en un único flujo de trabajo simplificado. ¡Excelente trabajo!

## Limpiar

Si has terminado de explorar el Servicio de Agentes de IA de Azure, deberías eliminar los recursos que has creado en este ejercicio para evitar costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o vuelve a abrir el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde desplegaste los recursos utilizados en este ejercicio.

1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.

1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

