---
lab:
    title: 'Desarrollar un agente de chat de IA de Azure con el SDK de Microsoft Agent Framework'
    description: 'Aprende a usar el SDK de Microsoft Agent Framework para crear y usar un agente de chat de IA de Azure.'
---

# Desarrollar un agente de chat de IA de Azure con el SDK de Microsoft Agent Framework

En este ejercicio, utilizarás el Servicio de Agentes de IA de Azure y Microsoft Agent Framework para crear un agente de IA que procesa reclamaciones de gastos.

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
1. En el panel **Configuración**, observa el nombre de tu implementación del modelo; que debería ser **gpt-4o**. Puedes confirmar esto viendo la implementación en la página **Modelos y endpoints** (solo abre esa página en el panel de navegación a la izquierda).
1. En el panel de navegación a la izquierda, selecciona **Información general** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de los detalles de un proyecto de IA de Azure en el portal de Azure AI Foundry.](./Media/ai-foundry-project.png)

## Crear una aplicación cliente del agente

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

    > **Consejo**: A medida que ingresas comandos en el cloudshell, la salida puede ocupar una gran cantidad del búfer de pantalla y el cursor en la línea actual puede quedar oculto. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Cuando el repositorio haya sido clonado, ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```
   cd ai-agents/Labfiles/04-agent-framework/python
   ls -a -l
    ```

    Los archivos proporcionados incluyen código de aplicación, un archivo para configuraciones y un archivo que contiene datos de gastos.

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install azure-identity agent-framework
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry), y el marcador de posición **your_model_deployment** con el nombre que asignaste a tu implementación del modelo gpt-4o.
1. Después de haber reemplazado los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Escribir código para una aplicación de agente

> **Consejo**: A medida que agregues código, asegúrate de mantener la indentación correcta. Usa los comentarios existentes como guía, ingresando el nuevo código al mismo nivel de indentación.

1. Ingresa el siguiente comando para editar el archivo de código del agente que se ha proporcionado:

    ```
   code agent-framework.py
    ```

1. Revisa el código en el archivo. Contiene:
    - Algunas instrucciones **import** para agregar referencias a espacios de nombres comúnmente usados
    - Una función *main* que carga un archivo que contiene datos de gastos, pregunta al usuario por instrucciones, y luego llama a...
    - Una función **process_expenses_data** en la que se debe agregar el código para crear y usar tu agente

1. En la parte superior del archivo, después de la instrucción **import** existente, encuentra el comentario **Add references**, y agrega el siguiente código para hacer referencia a los espacios de nombres en las bibliotecas que necesitarás para implementar tu agente:

    ```python
   # Add references
   from agent_framework import AgentThread, ChatAgent
   from agent_framework.azure import AzureAIAgentClient
   from azure.identity.aio import AzureCliCredential
   from pydantic import Field
   from typing import Annotated
    ```

1. Cerca del final del archivo, encuentra el comentario **Create a tool function for the email functionality**, y agrega el siguiente código para definir una función que tu agente usará para enviar correo electrónico (las herramientas son una forma de agregar funcionalidad personalizada a los agentes)

    ```python
   # Create a tool function for the email functionality
   def send_email(
    to: Annotated[str, Field(description="Who to send the email to")],
    subject: Annotated[str, Field(description="The subject of the email.")],
    body: Annotated[str, Field(description="The text body of the email.")]):
        print("\nTo:", to)
        print("Subject:", subject)
        print(body, "\n")
    ```

    > **Nota**: La función *simula* enviar un correo electrónico imprimiéndolo en la consola. ¡En una aplicación real, usarías un servicio SMTP o similar para enviar el correo electrónico realmente!

1. De vuelta arriba del código **send_email**, en la función **process_expenses_data**, encuentra el comentario **Create a chat agent**, y agrega el siguiente código para crear un objeto **ChatAgent** con las herramientas e instrucciones.

    (Asegúrate de mantener el nivel de indentación)

    ```python
   # Create a chat agent
   async with (
       AzureCliCredential() as credential,
       ChatAgent(
           chat_client=AzureAIAgentClient(async_credential=credential),
           name="expenses_agent",
           instructions="""You are an AI assistant for expense claim submission.
                           When a user submits expenses data and requests an expense claim, use the plug-in function to send an email to expenses@contoso.com with the subject 'Expense Claim`and a body that contains itemized expenses with a total.
                           Then confirm to the user that you've done so.""",
           tools=send_email,
       ) as agent,
   ):
    ```

    Observa que el objeto **AzureCliCredential** incluirá automáticamente las configuraciones del proyecto de Azure AI Foundry desde la configuración.

1. Encuentra el comentario **Use the agent to process the expenses data**, y agrega el siguiente código para crear un hilo para que tu agente se ejecute, y luego invocarlo con un mensaje de chat.

    (Asegúrate de mantener el nivel de indentación):

    ```python
   # Use the agent to process the expenses data
   try:
       # Add the input prompt to a list of messages to be submitted
       prompt_messages = [f"{prompt}: {expenses_data}"]
       # Invoke the agent for the specified thread with the messages
       response = await agent.run(prompt_messages)
       # Display the response
       print(f"\n# Agent:\n{response}")
   except Exception as e:
       # Something went wrong
       print (e)
    ```

1. Revisa que el código completado para tu agente, usando los comentarios para ayudarte a entender qué hace cada bloque de código, y luego guarda tus cambios de código (**CTRL+S**).
1. Mantén el editor de código abierto en caso de que necesites corregir algún error tipográfico en el código, pero redimensiona los paneles para que puedas ver más de la consola de línea de comandos.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de línea de comandos del cloud shell debajo del editor de código, ingresa el siguiente comando para iniciar sesión en Azure.

    ```
    az login
    ```

    **<font color="red">Debes iniciar sesión en Azure - aunque la sesión del cloud shell ya esté autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, simplemente usar *az login* será suficiente. Sin embargo, si tienes suscripciones en varios tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para más detalles.
    
1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresar el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.
1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```
   python agent-framework.py
    ```
    
    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

1. Cuando se te pregunte qué hacer con los datos de gastos, ingresa el siguiente prompt:

    ```
   Enviar una reclamación de gastos
    ```

1. Cuando la aplicación haya terminado, revisa la salida. El agente debería haber compuesto un correo electrónico para una reclamación de gastos basado en los datos que se proporcionaron.

    > **Consejo**: Si la aplicación falla porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder.

## Resumen

En este ejercicio, utilizaste el SDK de Microsoft Agent Framework para crear un agente con una herramienta personalizada.

## Limpiar

Si has terminado de explorar el Servicio de Agentes de IA de Azure, deberías eliminar los recursos que has creado en este ejercicio para evitar costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o vuelve a abrir el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde desplegaste los recursos utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

