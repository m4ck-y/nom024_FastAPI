# Catálogos Fundamentales para SIRES

http://www.dgis.salud.gob.mx/contenidos/intercambio/iis_catalogos_gobmx.html

## Contexto Normativo

De acuerdo con la [NOM-024-SSA3-2012](http://www.dgis.salud.gob.mx//contenidos/normatividad/normas_gobmx.html), los Sistemas de Información de Registro Electrónico para la Salud (SIRES) deben utilizar los catálogos definidos en el Apéndice Normativo “A” - **Matriz de Catálogos Fundamentales**.

### Objetivo de los Catálogos

Permitir un **intercambio interoperable, semántico y estructurado** de la información en salud, mediante vocabularios normalizados que:

- Faciliten el registro estandarizado
- Mejoren la calidad de los datos
- Permitan su explotación posterior (estadísticas, epidemiología, etc.)

### Actualización y uso

Los catálogos están sujetos a procesos continuos de armonización con el sector salud y pueden ser modificados por diferentes instituciones. Es responsabilidad del prestador:

- Descargar e integrar los catálogos actualizados
- Cumplir con los lineamientos establecidos
- Contactar a la institución fuente para conocer condiciones de uso

Contacto: [dgis@salud.gob.mx](mailto:dgis@salud.gob.mx) | Asunto: Catálogos

### Catálogos Médicos

### Catálogos Estadísticos

 - [Nacionalidades](http://www.dgis.salud.gob.mx/contenidos/intercambio/nacionalidades_gobmx.html)

# Guía Técnica: Integrar Catálogos NOM-024 con FastAPI + BigQuery + Google Secret Manager + Google Run

## Objetivo
Desarrollar e implementar una API REST escalable y segura en FastAPI que:

- Exponga catálogos médicos estandarizados según la NOM-024-SSA3-2012
- Consulte datos directamente desde BigQuery para garantizar consistencia y actualización en tiempo real
- Gestione credenciales de forma segura mediante Google Secret Manager (sin hardcodear en el código)
- Se despliegue automáticamente en Google Cloud Run bajo un modelo serverless
- Garantice interoperabilidad mediante:
    - JSON Schema para respuestas normalizadas
    - Autenticación JWT/OAuth2 (opcional para endpoints sensibles)
    - Documentación OpenAPI/Swagger integrada

[Diagrama de flujo](https://www.plantuml.com/plantuml/png/NLFRKjim47tNL-oG5t0dgHio3UIXWtFXqZO4OifBmuCYRro1BHbTwD1EFwRVm2VmOrtPIIOqBrdjsJrdzyWwiOuRvyk2sGUfAcvu2Kik7dAZlSf6kj06MgVrRwT2wBBI2fLBtNE1GErTvgIZC36FNZeKpXiE6HQGIkkm336Ck7lzM-XSMxYSJTjnjxTGKNJAhKkkBk0T36L-xT4yKvYYCEXWoXNFqKGHOnKDHJ7idMcT5qHMQ9_jmMy6yFrjzHrm2-aqZ9t4_IGKR9XhQ7WDhTx7e-wm5w2BP5fdwJzqZFjn7D8rFSozgi7H75f7_T7aD65_TaP9ga8ABkJhYrfF4XPPBrGtXdFhE9vCZjUiaan32-StDrTrGPC9h1btVCajqOufikXs_DeBfUEKg0xxyNZOQ2bIreeNCkCPshkGGkjuffkuz4eAMKaw1lf62DgVwfa6S3QvWVTlAHWXL43U4VwX0xEbenu4CZT39IGlq2xKlgtTBXkpEqzeB77O3XS2hJrWrBqL-PpEBY55yoG5GYA4zifjLCXmgkXsuBRMXmfDAQssZ032wPe8FYGOZLoHpM0qwGyMgWrBcJ-6w-m4psub_aJp9dslbzyi6aOKH4I-3Q3NWSaz2kyu29hM5nIarryPWHkjEOPqYYxqRLUWoz0Mb3ObZVcBtDtQr3YwsTAWhOWOORyRnp3xSi2OqWx1oFo70xqYLnb053NVgXv44HrNt3fUoVRoiTsOxCXaIy0-RMt3TmL2hWpF-053bK5WNFCMkAffnsbDEx7E-FhLRTvMez264I-h_pS8-JaMzUsZXKmBNv8uwJJOkRJkzSL8eI534BnSIcrt9gWTy5KmOHuyejt9ZDmZe5gexTjX9zJYo-8V)


# 1. Crear Dataset y Cargar Catálogo CSV en BigQuery

Configuración inicial de BigQuery para Catálogos SIRES

## Objetivo

Este paso se centra en la **configuración de BigQuery para albergar el catálogo de Nacionalidades** requerido por la NOM-024-SSA3-2012. El proceso clave implica:

- **Crear un Dataset principal** (`nom024`) para la organización lógica de los catálogos.
- **Importar manualmente el archivo CSV** del catálogo de Nacionalidades a una tabla específica (`cat_nacionalidades`).

**Este proceso de carga para el catálogo de Nacionalidades sirve como ejemplo.** Deberás replicar estos pasos, utilizando el mismo dataset `nom024`, para importar los demás catálogos en formato CSV, creando una nueva tabla para cada uno. Esta configuración es esencial para que la aplicación FastAPI pueda consultar estos datos de manera eficiente.

### **Pasos Clave:**

1. **Crear el Dataset `nom024`:**
    - Accede a la [Consola de Google Cloud](https://console.cloud.google.com/) y selecciona el proyecto (`hospitaldigital-461216`).
    - En la barra de búsqueda, escribe "BigQuery" y selecciona **BigQuery Studio**.
    - En el panel **"Explorer"** (izquierda), bajo el proyecto, haz clic en **"Crear dataset"**.
    - Nombra el dataset: `nom024`.
    - Selecciona la ubicación de los datos (ej. `europe-west1`).
    - Haz clic en **"Crear dataset"**.
2. **Crear la Tabla `cat_nacionalidades` e Importar CSV:**
    - Dentro del dataset `nom024`, haz clic en **"Crear tabla"**.
    - En "Crear tabla desde", selecciona **"Subida"**.
    - Sube el archivo CSV de Nacionalidades que se descargó de http://www.dgis.salud.gob.mx/contenidos/intercambio/nacionalidades_gobmx.html.
    - Nombra la tabla: `cat_nacionalidades`.
    - Asegúrate de que el formato de archivo sea "CSV" y marca **"Detectar automáticamente el esquema"** y **"Detectar automáticamente los valores de encabezado"**.
    - Haz clic en **"Crear tabla"**.

Una vez completado, el catálogo de Nacionalidades estará disponible en la tabla `cat_nacionalidades` dentro del dataset `nom024` del proyecto `hospitaldigital-461216`.

![Captura de pantalla, BigQuery](https://storage.googleapis.com/fastapi-bigquery-credentials/1_bigquery.png)

# 📄 2. Configuración de Cuenta de Servicio para Pruebas Locales con FastAPI y BigQuery

Este paso te guía en la creación de una **Cuenta de Servicio** en Google Cloud. Necesitarás esta cuenta y un archivo de credenciales (`credentials.json`) para **probar tu aplicación FastAPI localmente**, aunque el despliegue final en Cloud Run usará un método más seguro (Secret Manager).

---

## 📌 ¿Por qué una Cuenta de Servicio?

Una **Cuenta de Servicio** es una identidad digital que tu aplicación usa para interactuar de forma segura y programática con los servicios de Google Cloud. Para que FastAPI consulte BigQuery, necesita autenticarse y tener permisos específicos.

---

## 🛠️ Pasos para Configurar la Cuenta de Servicio

### 2.1. Accede a Google Cloud Console

Ve a [https://console.cloud.google.com](https://console.cloud.google.com/) y selecciona tu proyecto (`hospitaldigital-461216`).

### 2.2. Crea la Cuenta de Servicio

1. Navega a **"IAM y Administración"** → **"Cuentas de servicio"** (o usa el buscador).
2. Haz clic en **"Crear cuenta de servicio"**.
    - **Nombre de la cuenta**: `api_fastapi_bq`
    - **ID generado por GCP**: `api-fastapi-bq@hospitaldigital-461216.iam.gserviceaccount.com`
    - **Descripción (Opcional)**: `Cuenta usada por API FastAPI para consultar BigQuery`.
3. Haz clic en **"Crear y continuar"**.

### 2.3. Asigna Permisos (Roles)

Concede los roles mínimos para que la aplicación lea BigQuery:

| Rol | ID técnico | Propósito |
| --- | --- | --- |
| **BigQuery Data Viewer** | `roles/bigquery.dataViewer` | Permite leer datos y esquemas de tablas. |
| **BigQuery Job User** | `roles/bigquery.jobUser` | Permite ejecutar consultas en BigQuery. |

Exportar a Hojas de cálculo

Haz clic en **"Continuar"** y luego en **"Listo"**.

### 2.4. Descarga la Clave (`credentials.json`)

Para las pruebas locales, necesitas un archivo con las credenciales de esta cuenta.

1. En la lista de cuentas de servicio, busca `api-fastapi-bq@hospitaldigital-461216.iam.gserviceaccount.com`.
2. Haz clic en los tres puntos (`⋮`) → **"Administrar claves"**.
3. Haz clic en **"Agregar clave" > "Crear nueva clave"**.
4. Selecciona **JSON** y haz clic en **"Crear"**.
5. Se descargará `credentials.json`. **Guárdalo en un lugar seguro.**

> ⚠️ ¡ADVERTENCIA DE SEGURIDAD CRÍTICA!
Este archivo credentials.json es una credencial altamente sensible, equivalente a la contraseña maestra de tu proyecto. NUNCA lo subas a ningún repositorio de código (GitHub, GitLab, etc.). Su exposición podría comprometer gravemente tus datos y generar costos inesperados.
> 

---

## Uso Local y Protección de `credentials.json`

### Configura la Variable de Entorno para Pruebas Locales

Para que tu FastAPI encuentre las credenciales, establece esta variable en tu terminal **antes de iniciar la aplicación**:

Bash

`export GOOGLE_APPLICATION_CREDENTIALS="./credentials.json"`

Las librerías de Google Cloud buscarán automáticamente este archivo para autenticarse.

### Protege con `.gitignore`

Para evitar que `credentials.json` se suba accidentalmente a tu repositorio, añádelo a tu archivo `.gitignore`:

```matlab
# .gitignore
credentials.json
```

## ✅ Verificación Local

Una vez que tu API FastAPI esté ejecutándose con esta configuración local:

1. Accede al endpoint `/nacionalidades`.
2. Deberías ver los datos de Nacionalidades desde BigQuery, confirmando que la autenticación local funciona.

---

## 📌 Importante: Transición a Producción

El uso de `credentials.json` es **solo para desarrollo y pruebas locales**. Para entornos de producción (como Google Cloud Run), es esencial **evitar archivos `.json` físicos** y usar métodos más seguros como **Google Secret Manager** (ver siguiente guía) o las Credenciales por Defecto de la Aplicación (ADC), donde Google Cloud gestiona la autenticación automáticamente.

![Captura de pantalla, configracion de Service Account](https://storage.googleapis.com/fastapi-bigquery-credentials/2_cuenta_servicio.png)

# 🔐 3. Conectar FastAPI a BigQuery usando Google Secret Manager (Sin `credentials.json` Físico)

Este paso detalla cómo conectar una API FastAPI a BigQuery de forma segura utilizando **Google Secret Manager**. El objetivo principal es **evitar el almacenamiento directo de archivos de credenciales (`credentials.json`)** en el sistema de archivos o en el entorno de despliegue, lo que mejora significativamente la seguridad.

## 🎯 Objetivo

Permitir que una API FastAPI se conecte a BigQuery de forma segura, **sin guardar archivos `.json` sensibles en disco**, mediante la recuperación dinámica de credenciales desde Google Secret Manager en tiempo de ejecución.


## 🛠️ Pasos para la Configuración

### 3.1. Cuenta de Servicio (`api-fastapi-bq`)

Reutilice la cuenta de servicio `api-fastapi-bq@hospitaldigital-461216.iam.gserviceaccount.com` creada en la Sección 2.

**Importante:** Para este paso, necesitará el **contenido JSON de una clave de esta cuenta de servicio**. Si ya descargó un `credentials.json` para pruebas locales, utilice su contenido. En caso contrario, puede generar una clave JSON temporalmente para copiar su contenido, pero **no la almacene permanentemente en disco**; su único propósito es obtener el texto para Secret Manager.

### 3.2. Habilitar la API de Secret Manager

Asegúrese de que el servicio de Secret Manager esté activo en su proyecto (`hospitaldigital-461216`).

1. Vaya a la **Biblioteca de API** en Google Cloud Console.
2. Busque “Secret Manager API”.
3. Haga clic en **"Habilitar"** si aún no está activado.

### 3.3. Crear el Secreto con las Credenciales

Este paso almacena de forma segura el contenido JSON de las credenciales de la cuenta de servicio.

1. Vaya a **Secret Manager** en Google Cloud Console.
2. Haga clic en **“Crear secreto”**.
3. **Nombre del secreto**: Asigne un nombre claro y único, por ejemplo, `fastapi-bigquery-credentials`.
4. En el campo **"Contenido secreto"**: **Copie y pegue TODO el contenido del archivo JSON** de la clave de su cuenta de servicio (el que comienza con `{ "type": "service_account", ... }`).
5. Haga clic en **"Crear"**.

### 3.4. Asignar Permisos a la Cuenta de Servicio para Acceder al Secreto(`secretAccessor`)

Para permitir que la aplicación, ejecutándose bajo la cuenta de servicio `api-fastapi-bq`, pueda leer el secreto creado, se debe otorgar un permiso específico.

1. Vaya a **IAM y Administración** → **IAM**.
2. Busque la cuenta de servicio `api-fastapi-bq@hospitaldigital-461216.iam.gserviceaccount.com`.
3. Haga clic en el icono de **"Editar"** (el lápiz) junto a la cuenta de servicio.
4. Haga clic en **"Añadir otro rol"**.
5. Busque y seleccione el rol: **`Secret Manager Secret Accessor`** (`roles/secretmanager.secretAccessor`).
6. Haga clic en **"Guardar"**.

Este rol (`secretmanager.versions.access`) es fundamental para que la aplicación pueda acceder y leer el contenido del secreto. Sin él, se obtendría un error de "Permission denied".

---

## 3.5. Librerías Necesarias para la Integración

Para que FastAPI pueda interactuar con Google Secret Manager y BigQuery, asegúrese de que las siguientes librerías Python estén instaladas. Estas son adicionales a las ya mencionadas en pasos anteriores:

```python
pip install google-cloud-secret-manager google-cloud-bigquery
```

---

## 🛡️ Seguridad y Buenas Prácticas con Secret Manager

| Recomendación | Razón |
| --- | --- |
| **Nunca guarde el archivo `.json`** | Evita la filtración de credenciales sensibles en el sistema o en el control de versiones. |
| **Use Secret Manager** | Es el método recomendado por Google Cloud para gestionar secretos de forma centralizada y segura. |
| **Limite el acceso por IAM** | Otorgue solo los permisos (`Secret Manager Secret Accessor`) a las cuentas de servicio que realmente necesiten leer secretos específicos. |
| **Control de versiones de secretos** | Secret Manager permite gestionar versiones de los secretos, facilitando la reversión en caso de un problema. |


![Captura de pantalla, Secret Manager](https://storage.googleapis.com/fastapi-bigquery-credentials/3_secret_manager.png)

# 🚀 4. Despliegue de FastAPI en Google Cloud Run con Docker

Este paso detalla cómo desplegar tu aplicación FastAPI en Google Cloud Run utilizando un contenedor Docker. Cloud Run es un servicio completamente gestionado que escala automáticamente tu aplicación, ideal para APIs y servicios web.

## 🎯 Objetivo

Desplegar la API FastAPI en Google Cloud Run, permitiendo que sea accesible públicamente y utilice la cuenta de servicio previamente configurada para interactuar de forma segura con BigQuery y Secret Manager.


## 🛠️ Pasos para el Despliegue

### 4.1. Conectar a un Repositorio (GitHub)

Google Cloud Run puede construir y desplegar automáticamente tu contenedor cada vez que hay cambios en tu repositorio.

1. En la consola de Google Cloud, busca **"Cloud Run"**.
2. Haz clic en **"Crear servicio"** o **"Crear una nueva revisión"** si ya tienes un servicio.
3. Selecciona **"Desplegar continuamente desde un repositorio (código fuente o función)"**.
4. **Conecta con tu proveedor de repositorio**: Elige **GitHub**. Se te pedirá que autorices la conexión con tu cuenta de GitHub.
5. **Selecciona el repositorio**: Elige el repositorio de GitHub que contiene el código de tu proyecto FastAPI.
6. **Configura la rama**: Selecciona la rama de la que deseas desplegar (ej., `main` o `master`).

### 4.2. Configuración del Servicio Cloud Run

Define los ajustes básicos de tu servicio Cloud Run.

1. **Nombre del servicio**: Asigna un nombre descriptivo a tu servicio, por ejemplo: `catalogos-nom024-fastapi-bigquery`.
2. **Permitir conexiones no autenticadas**: Marca esta opción para que tu API sea accesible públicamente sin requerir autenticación de usuarios de Google. Esto es común para APIs que luego se consumirán por otras aplicaciones o sitios web.
3. **Puerto**: Configura el puerto en `8000`. Este es el puerto que tu aplicación FastAPI está configurada para escuchar dentro del contenedor Docker. Asegúrate de que tu `Dockerfile` y tu código FastAPI estén configurados para usar este puerto.

### 4.3. Configuración de Seguridad y Permisos

Es crucial configurar correctamente la cuenta de servicio para que tu aplicación tenga los permisos adecuados en Google Cloud.

1. En la sección de **"Seguridad"** (o "Cuenta de servicio"), selecciona la opción **"Cuenta de servicio"**.
2. Elige la cuenta de servicio que creaste anteriormente: **`api_fastapi_bq`** (identificada como `api-fastapi-bq@hospitaldigital-461216.iam.gserviceaccount.com`).
    - **Razón**: Al asignar esta cuenta de servicio, Cloud Run ejecuta tu contenedor con las identidades y permisos de `api_fastapi_bq`. Esto significa que tu aplicación tendrá automáticamente acceso a BigQuery y Secret Manager (gracias a los roles `BigQuery Data Viewer`, `BigQuery Job User` y `Secret Manager Secret Accessor` que le asignaste en el paso anterior) sin necesidad de archivos `credentials.json` o variables de entorno locales.

### 4.4. Crear y Desplegar el Servicio

Una vez configurados todos los parámetros:

1. Haz clic en **"Crear"** o **"Desplegar"**.
2. Google Cloud Build tomará el `Dockerfile` de tu repositorio, construirá la imagen de contenedor, la almacenará en Google Container Registry (GCR) o Artifact Registry, y luego desplegará esta imagen en Cloud Run.
    - **Nota sobre el `Dockerfile`**: Cloud Run se basa en tu `Dockerfile` para construir el entorno de tu aplicación. Este archivo debe contener todas las instrucciones para instalar dependencias, copiar tu código y definir cómo se inicia tu aplicación (por ejemplo, `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`).

## ✅ Verificación del Despliegue

Una vez que el despliegue haya finalizado (puede tardar unos minutos):

1. Cloud Run te proporcionará una **URL** pública para tu servicio.
2. Accede a esa URL seguida de tu endpoint (ej., [https://catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app](https://catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app/)).
3. Deberías ver los datos de Nacionalidades, confirmando que tu API está desplegada y funcionando correctamente en la nube, conectándose a BigQuery a través de Secret Manager.


![Captura de pantalla, GCP Run + Service Account](https://storage.googleapis.com/fastapi-bigquery-credentials/4_cloud_run_security_service_account)

# 5. Validación Local de la API

Este paso describe los métodos para verificar el correcto funcionamiento de la API FastAPI en un entorno de desarrollo local, utilizando tanto la ejecución directa con Uvicorn como la simulación de un entorno de producción con Docker.

## 🎯 Objetivo

Verificar el correcto funcionamiento de la API FastAPI en un entorno de desarrollo local, utilizando tanto la ejecución directa con Uvicorn como la simulación de un entorno de producción con Docker.

## 🛠️ Métodos de Verificación

### 5.1. Pruebas con Uvicorn (sin Docker)

- **Propósito:** Este método permite probar rápidamente el código Python de la API directamente en la máquina local, sin la capa de contenedorización. Es útil para el desarrollo iterativo y la depuración del código fuente.
- **Comando de Ejecución:**
    
    ```
    uvicorn app.main:app --reload
    ```
    
    - **Nota:** Asegúrese de que la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` esté configurada correctamente para que la aplicación local pueda autenticarse con BigQuery y Secret Manager, según lo documentado en la Sección 2.

### 5.2. Pruebas con Docker (Construcción y Ejecución de Contenedor)

- **Propósito:** Este método simula el entorno de despliegue en la nube (como Cloud Run) al empaquetar la aplicación en un contenedor Docker. Permite verificar que la aplicación se construye y ejecuta correctamente dentro de un entorno aislado, tal como lo haría en producción.
- **Construcción de la Imagen Docker:**
    - Para construir la imagen Docker de la aplicación, ejecute el siguiente comando en el directorio raíz del proyecto, donde se encuentra el `Dockerfile`:
        
        ```
        docker build -t nom024_fastapi_bigquery .
        ```
        
        - **`nom024_fastapi_bigquery`**: Es el nombre asignado a la imagen Docker.
        - **`.`**: Indica que el contexto de construcción es el directorio actual.
- **Ejecución del Contenedor Docker:**
    - Una vez que la imagen ha sido construida, se puede ejecutar un contenedor a partir de ella, mapeando el puerto 8000 del contenedor al puerto 8000 de la máquina local y asignándole un nombre:
        
        ```
        docker run -d -p 8000:8000 --name fastapi-catalogos nom024_fastapi_bigquery:latest
        ```
        
        - **`d`**: Ejecuta el contenedor en modo "detached" (en segundo plano).
        - **`p 8000:8000`**: Mapea el puerto 8000 del host al puerto 8000 del contenedor.
        - **`-name fastapi-catalogos`**: Asigna un nombre específico al contenedor para facilitar su gestión.
        - **`nom024_fastapi_bigquery:latest`**: Especifica el nombre y la etiqueta de la imagen Docker a utilizar.
    - **Nota:** Para acceder a la API, utilice `http://localhost:8000/nacionalidades`. Para detener el contenedor, use `docker stop fastapi-catalogos`. Para eliminarlo, `docker rm fastapi-catalogos`.

# 6. Endpoints y Documentación OpenAPI

Este paso describe cómo acceder a los endpoints de la API desplegada en Google Cloud Run y cómo visualizar su documentación interactiva a través de Swagger UI.

## 🎯 Objetivo

Proporcionar las instrucciones para acceder a la URL base de la API desplegada y a su documentación OpenAPI (Swagger UI), permitiendo la exploración de todos los endpoints disponibles y sus detalles.

## 🛠️ Pasos Clave

### 6.1. Acceso a la URL Base de la API

Una vez que el servicio FastAPI ha sido desplegado exitosamente en Google Cloud Run (como se detalla en la Sección 4), Cloud Run genera una URL pública para el servicio. Esta URL sirve como la base para acceder a todos los endpoints de la API.

- **URL Base de la API Desplegada:**`https://catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app`

### 6.2. Acceso a la Documentación OpenAPI (Swagger UI)

FastAPI genera automáticamente documentación interactiva de la API utilizando Swagger UI. Esta documentación es accesible a través de un endpoint específico del servicio desplegado.

- **URL de la Documentación OpenAPI (Swagger UI):**
Para acceder a la documentación completa de la API y explorar todos los endpoints disponibles (incluyendo sus métodos HTTP, parámetros, y modelos de respuesta), se debe acceder a la siguiente URL:
`https://catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app/docs`
    
    Esta interfaz permite interactuar con la API directamente desde el navegador, facilitando las pruebas y la comprensión de su funcionamiento.

# ANEXOS

### REFERENCIAS
[Secret Manager Quickstart (python)](https://cloud.google.com/secret-manager/docs/create-secret-quickstart?hl=es-419#secretmanager-quickstart-python)

### Enpoints
- Catalogos Estadisticos

    - https://catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app/nacionalidades

### Documentación OpenAPI (Swagger UI)
- https://catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app/docs

### Capturas
Las siguientes imágenes se encuentran almacenadas en un bucket de Google Cloud Storage y se utilizan como referencia visual a lo largo de esta documentación.

![Bucket](https://storage.googleapis.com/fastapi-bigquery-credentials/bucket.png)

### Roles en la Cuenta de Servicio `api-fastapi-bq`

La cuenta de servicio tiene los siguientes roles asignados, que son los que le otorgan permisos en el proyecto de Google Cloud:

| Rol | ID | Justificación |
|-----|----|---------------|
| `BigQuery Data Viewer` | `roles/bigquery.dataViewer` | Permite leer tablas de catálogos |
| `BigQuery Job User` | `roles/bigquery.jobUser` | Ejecutar queries a BigQuery |
| `Secret Manager Secret Accessor` | `roles/secretmanager.secretAccessor` | Leer credenciales desde Secret Manager |

1. **Usuario con acceso a secretos de Secret Manager**
    - **Equivalente en inglés:** `Secret Manager Secret Accessor`
    - **Descripción:** ¡Este es el rol clave! Otorga el permiso `secretmanager.versions.access`, que permite a tu aplicación **leer el contenido real (el payload) de una versión específica de un secreto** almacenado en Secret Manager. Este permiso es esencial para que tu FastAPI pueda obtener las credenciales de BigQuery.
2. **Usuario de trabajo de BigQuery**
    - **Equivalente en inglés:** `BigQuery Job User`
    - **Descripción:** Este rol permite a la cuenta de servicio ejecutar trabajos en BigQuery, como consultas (`client.query(query)`), trabajos de carga, exportación o copia. Es fundamental para interactuar con BigQuery a nivel de ejecución de operaciones.
3. **Visualizador de datos de BigQuery**
    - **Equivalente en inglés:** `BigQuery Data Viewer`
    - **Descripción:** Este rol proporciona permisos de solo lectura sobre los datos dentro de BigQuery. Permite a la cuenta de servicio **leer filas de tablas y vistas**, lo cual es necesario para obtener los resultados de tus consultas BigQuery, como en tu endpoint `/nacionalidades`.

![IAM](https://storage.googleapis.com/fastapi-bigquery-credentials/iam.png)