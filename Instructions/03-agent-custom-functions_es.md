---
lab:
    title: 'Usar una función personalizada en un agente de IA'
    description: 'Aprende a usar funciones para agregar capacidades personalizadas a tus agentes.'
---

# Usar una función personalizada en un agente de IA

En este ejercicio explorarás la creación de un agente que puede usar funciones personalizadas como herramienta para completar tareas. Construirás un agente simple de soporte técnico que puede recopilar detalles de un problema técnico y generar un ticket de soporte.

> **Consejo**: El código utilizado en este ejercicio está basado en el SDK de Azure AI Foundry para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas de cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos para completar.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Podrías experimentar algunos comportamientos inesperados, advertencias o errores.

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Ayuda** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./Media/ai-foundry-home.png)

1. En la página de inicio, selecciona **Crear un agente**.
1. Cuando se te solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Opciones avanzadas**.
1. Confirma las siguientes configuraciones para tu proyecto:
    - **Recurso de Azure AI Foundry**: *Un nombre válido para tu recurso de Azure AI Foundry*
    - **Suscripción**: *Tu suscripción de Azure*
    - **Grupo de recursos**: *Crea o selecciona un grupo de recursos*
    - **Región**: *Selecciona cualquiera **recomendada por AI Foundry***\*

    > \* Algunos recursos de Azure AI están limitados por cuotas de modelo regionales. En el caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Crear** y espera a que se cree tu proyecto.
1. Si se te solicita, despliega un modelo **gpt-4o** utilizando la opción de implementación *Estándar Global* o *Estándar* (dependiendo de la disponibilidad de tu cuota).

    >**Nota**: Si la cuota está disponible, un modelo base GPT-4o puede desplegarse automáticamente al crear tu Agente y proyecto.

1. Cuando se cree tu proyecto, el playground de Agentes se abrirá.

1. En el panel de navegación a la izquierda, selecciona **Información general** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de la página de información general de un proyecto de Azure AI Foundry.](./Media/ai-foundry-project.png)

1. Copia los valores del **endpoint del proyecto de Azure AI Foundry** a un bloc de notas, ya que los usarás para conectarte a tu proyecto en una aplicación cliente.

## Desarrollar un agente que usa herramientas de función

Ahora que has creado tu proyecto en AI Foundry, desarrollemos una aplicación que implemente un agente usando herramientas de función personalizadas.

### Clonar el repositorio que contiene el código de la aplicación

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

1. Ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```
   cd ai-agents/Labfiles/03-ai-agent-functions/Python
   ls -a -l
    ```

    Los archivos proporcionados incluyen código de aplicación y un archivo para configuraciones.

### Configurar los ajustes de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects
    ```

    >**Nota:** Puedes ignorar cualquier mensaje de advertencia o error mostrado durante la instalación de la biblioteca.

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Información general** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación del modelo (que debería ser *gpt-4o*).
1. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierto el panel de línea de comandos del cloud shell.

### Definir una función personalizada

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado para tu código de función:

    ```
   code user_functions.py
    ```

1. Encuentra el comentario **Create a function to submit a support ticket** y agrega el siguiente código, que genera un número de ticket y guarda un ticket de soporte como archivo de texto.

    ```python
   # Create a function to submit a support ticket
   def submit_support_ticket(email_address: str, description: str) -> str:
        script_dir = Path(__file__).parent  # Get the directory of the script
        ticket_number = str(uuid.uuid4()).replace('-', '')[:6]
        file_name = f"ticket-{ticket_number}.txt"
        file_path = script_dir / file_name
        text = f"Support ticket: {ticket_number}\nSubmitted by: {email_address}\nDescription:\n{description}"
        file_path.write_text(text)
    
        message_json = json.dumps({"message": f"Support ticket {ticket_number} submitted. The ticket file is saved as {file_name}"})
        return message_json
    ```

1. Encuentra el comentario **Define a set of callable functions** y agrega el siguiente código, que define estáticamente un conjunto de funciones invocables en este archivo de código (en este caso, solo hay una - pero en una solución real podrías tener múltiples funciones que tu agente puede llamar):

    ```python
   # Define a set of callable functions
   user_functions: Set[Callable[..., Any]] = {
        submit_support_ticket
    }
    ```
1. Guarda el archivo (*CTRL+S*).

### Escribir código para implementar un agente que puede usar tu función

1. Ingresa el siguiente comando para comenzar a editar el código del agente.

    ```
    code agent.py
    ```

    > **Consejo**: A medida que agregues código al archivo de código, asegúrate de mantener la indentación correcta.

1. Revisa el código existente, que recupera las configuraciones de la aplicación y configura un bucle en el que el usuario puede ingresar prompts para el agente. El resto del archivo incluye comentarios donde agregarás el código necesario para implementar tu agente de soporte técnico.
1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás para construir un agente de IA de Azure que usa tu código de función como herramienta:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder, MessageRole
   from user_functions import user_functions
    ```

1. Encuentra el comentario **Connect to the Agent client** y agrega el siguiente código para conectarte al proyecto de Azure AI usando las credenciales actuales de Azure.

    > **Consejo**: Ten cuidado de mantener el nivel de indentación correcto.

    ```python
   # Connect to the Agent client
   agent_client = AgentsClient(
       endpoint=project_endpoint,
       credential=DefaultAzureCredential
           (exclude_environment_credential=True,
            exclude_managed_identity_credential=True)
   )
    ```
    
1. Encuentra la sección de comentario **Define an agent that can use the custom functions**, y agrega el siguiente código para agregar tu código de función a un conjunto de herramientas, y luego crear un agente que puede usar el conjunto de herramientas y un hilo en el que ejecutar la sesión de chat.

    ```python
   # Define an agent that can use the custom functions
   with agent_client:

        functions = FunctionTool(user_functions)
        toolset = ToolSet()
        toolset.add(functions)
        agent_client.enable_auto_function_calls(toolset)
            
        agent = agent_client.create_agent(
            model=model_deployment,
            name="support-agent",
            instructions="""You are a technical support agent.
                            When a user has a technical issue, you get their email address and a description of the issue.
                            Then you use those values to submit a support ticket using the function available to you.
                            If a file is saved, tell the user the file name.
                         """,
            toolset=toolset
        )

        thread = agent_client.threads.create()
        print(f"You're chatting with: {agent.name} ({agent.id})")

    ```

1. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código para agregar el prompt del usuario como mensaje y ejecutar el hilo.

    ```python
   # Send a prompt to the agent
   message = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt
   )
   run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    ```

    > **Nota**: Usar el método **create_and_process** para ejecutar el hilo permite al agente encontrar automáticamente tus funciones y elegir usarlas según sus nombres y parámetros. Como alternativa, podrías usar el método **create_run**, en cuyo caso serías responsable de escribir código para sondear el estado de ejecución para determinar cuándo se requiere una llamada de función, llamar a la función y devolver los resultados al agente.

1. Encuentra el comentario **Check the run status for failures** y agrega el siguiente código para mostrar cualquier error que ocurra.

    ```python
   # Check the run status for failures
   if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    ```

1. Encuentra el comentario **Show the latest response from the agent** y agrega el siguiente código para recuperar los mensajes del hilo completado y mostrar el último que fue enviado por el agente.

    ```python
   # Show the latest response from the agent
   last_msg = agent_client.messages.get_last_message_text_by_role(
       thread_id=thread.id,
       role=MessageRole.AGENT,
   )
   if last_msg:
        print(f"Last Message: {last_msg.text.value}")
    ```

1. Encuentra el comentario **Get the conversation history** y agrega el siguiente código para imprimir los mensajes del hilo de conversación; ordenándolos en secuencia cronológica

    ```python
   # Get the conversation history
   print("\nConversation Log:\n")
   messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
        if message.text_messages:
           last_msg = message.text_messages[-1]
           print(f"{message.role}: {last_msg.text.value}\n")
    ```

1. Encuentra el comentario **Clean up** y agrega el siguiente código para eliminar el agente y el hilo cuando ya no sean necesarios.

    ```python
   # Clean up
   agent_client.delete_agent(agent.id)
   print("Deleted agent")
    ```

1. Revisa el código, usando los comentarios para entender cómo:
    - Agrega tu conjunto de funciones personalizadas a un conjunto de herramientas
    - Crea un agente que usa el conjunto de herramientas.
    - Ejecuta un hilo con un mensaje de prompt del usuario.
    - Verifica el estado de la ejecución en caso de que haya un fallo
    - Recupera los mensajes del hilo completado y muestra el último enviado por el agente.
    - Muestra el historial de conversación
    - Elimina el agente y el hilo cuando ya no se requieren.

1. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado. También puedes cerrar el editor de código (*CTRL+Q*); aunque es posible que desees mantenerlo abierto en caso de que necesites hacer alguna edición al código que agregaste. En cualquier caso, mantén abierto el panel de línea de comandos del cloud shell.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```
    az login
    ```

    **<font color="red">Debes iniciar sesión en Azure - aunque la sesión del cloud shell ya esté autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, simplemente usar *az login* será suficiente. Sin embargo, si tienes suscripciones en varios tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para más detalles.
    
1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresar el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.
1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```
   python agent.py
    ```
    
    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

1. Cuando se te solicite, ingresa un prompt como:

    ```
   Tengo un problema técnico
    ```

    > **Consejo**: Si la aplicación falla porque se excede el límite de velocidad. Espera unos segundos e intenta de nuevo. Si no hay cuota suficiente disponible en tu suscripción, el modelo puede no poder responder.

1. Visualiza la respuesta. El agente puede solicitar tu dirección de correo electrónico y una descripción del problema. Puedes usar cualquier dirección de correo electrónico (por ejemplo, `alex@contoso.com`) y cualquier descripción de problema (por ejemplo `mi computadora no arranca`)

    Cuando tenga suficiente información, el agente debería elegir usar tu función según sea necesario.

1. Puedes continuar la conversación si lo deseas. El hilo tiene *estado*, por lo que retiene el historial de conversación - lo que significa que el agente tiene el contexto completo para cada respuesta. Ingresa `quit` cuando hayas terminado.
1. Revisa los mensajes de conversación que fueron recuperados del hilo, y los tickets que fueron generados.
1. La herramienta debería haber guardado tickets de soporte en la carpeta de la aplicación. Puedes usar el comando `ls` para verificar, y luego usar el comando `cat` para ver el contenido del archivo, así:

    ```
   cat ticket-<ticket_num>.txt
    ```

## Limpiar

Ahora que has terminado el ejercicio, deberías eliminar los recursos en la nube que has creado para evitar el uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del grupo de recursos donde desplegaste los recursos del hub utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Eliminar grupo de recursos**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.

