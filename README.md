# Catálogos

En términos de la NOM-024-SSA3-2012, sistemas de información de registro electrónico para la salud. Intercambio de información en salud, numeral 6.4.2, los SIRES deben utilizar los catálogos fundamentales establecidos en el Apéndice Normativo “A” de dicha norma "Matriz de Catálogos Fundamentales".

Es obligación de los prestadores de servicios de salud que utilicen SIRES, mantener actualizados los catálogos y cumplir sus lineamientos de acuerdo a lo publicado en la presente página electrónica.

Para garantizar el intercambio e interpretación de la información de los registros electrónicos en salud entre los diferentes SIRES dentro del sistema nacional de salud, es fundamental contar con catálogos o vocabularios estandarizados, que permitan la correcta codificación, registro y posterior explotación de información en salud.

En esta sección se presenta una recopilación de los catálogos, con el fin de facilitar su descarga e integración a SIRES. Esta recopilación es producto de un proceso continuo de armonización con el sector, por lo que será actualizada regularmente.

Cabe destacar que cada catálogo puede ser desarrollado por instituciones diferentes e independientes de la Dirección General de Información en Salud, por lo que los usuarios deberán contactar a las mismas para conocer sus condiciones de uso, derechos de autor y aclarar cualquier duda respecto de su contenido e interpretación.

Para cualquier duda o comentario sobre esta recopilación, favor de contactar en: dgis@salud.gob.mx, con el asunto: Catálogos.

# Catálogos Médicos

# Catálogos Estadísticos


# 📄 Guía completa: Crear cuenta de servicio en Google Cloud para usar BigQuery desde FastAPI

---

## 📌 ¿Qué es una cuenta de servicio?

Una **cuenta de servicio** es una identidad digital (como un “robot”) usada por aplicaciones, servicios y scripts para interactuar con los servicios de Google Cloud **de forma programática y segura**.

### ✅ ¿Por qué necesitas una?

Para que tu aplicación FastAPI (que no tiene sesión de usuario) pueda consultar datos en **BigQuery**, necesita:

- Autenticarse con Google Cloud.
- Tener permisos explícitos para acceder al proyecto y sus datos.

Esto se logra **creando una cuenta de servicio y dándole permisos específicos.**

---

## 🛠️ Paso a paso: Crear cuenta de servicio

### 1. Ingresa a Google Cloud Console

➡️ https://console.cloud.google.com

---

### 2. Selecciona o crea tu proyecto

Asegúrate de estar en el proyecto donde tienes tus datos BigQuery.

Ejemplo: `hospitaldigital-461216`

---

### 3. Ve a la sección **IAM & administración → Cuentas de servicio**

O entra directamente:

➡️ https://console.cloud.google.com/iam-admin/serviceaccounts

---

### 4. Haz clic en **"Crear cuenta de servicio"**

### Paso 1: Detalles de la cuenta

- **Nombre de la cuenta**: `api-fastapi`
- **ID de la cuenta**: se autogenera
- **Descripción**: (opcional)
    
    Ejemplo: `Cuenta usada por la API FastAPI para consultar BigQuery`
    

Haz clic en **Crear y continuar**

---

### 5. Asignar permisos (roles)

En el siguiente paso, agrega los siguientes **roles mínimos necesarios**:

| Rol | ID técnico | ¿Para qué sirve? |
| --- | --- | --- |
| **BigQuery Data Viewer** | `roles/bigquery.dataViewer` | Permite leer tablas y datasets |
| **BigQuery Job User** | `roles/bigquery.jobUser` | Permite lanzar consultas (crear jobs) |

✅ Estos roles son suficientes para consultar datos desde FastAPI.

Haz clic en **"Continuar"** y luego en **"Listo"**

---

### 6. Descargar la clave (credentials.json)

1. Busca la cuenta que acabas de crear.
2. Haz clic en los 3 puntos (`⋮`) → **"Administrar claves"**
3. Haz clic en **"Agregar clave" > "Crear nueva clave"**
4. Selecciona **JSON**
5. Haz clic en **Crear**

📥 Se descargará un archivo `.json` → **Este es tu archivo `credentials.json`**

> ⚠️ ¡Guárdalo en un lugar seguro y nunca lo subas a GitHub!
> 

---

## 📂 Cómo usar `credentials.json` en tu app FastAPI

```python
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
```

---

## ✅ Verificación

Una vez configurado todo:

1. Ejecuta tu API FastAPI.
2. Accede al endpoint `/nacionalidades`.
3. Deberías obtener datos desde BigQuery sin errores de permisos.

---

## 📌 Seguridad

- No compartas el archivo `.json`.
- No lo subas a GitHub (añádelo al `.gitignore`).
- Para producción, considera usar **Google Secret Manager** o variables de entorno.

---

## 🧩 Extras (opcional)

### Para permisos más granulares:

- Usa políticas IAM personalizadas.
- Limita la cuenta solo a ciertos datasets.





# 🔐 Guía: Conectar FastAPI a BigQuery usando Google Secret Manager (sin `credentials.json` físico)


## 🎯 Objetivo

Permitir que una API FastAPI se conecte a BigQuery **de forma segura**, **sin necesidad de guardar un archivo de credenciales `.json` en el sistema de archivos**, usando **Google Secret Manager**.

---

## 🧩 Requisitos

- Proyecto en Google Cloud (`hospitaldigital-461216`)
- Una cuenta de servicio con permisos de BigQuery
- FastAPI como backend
- Secret Manager habilitado

---

## ✅ Paso 1: Crear la cuenta de servicio (si no la tienes)

1. Ve a IAM → Cuentas de servicio
2. Haz clic en **“Crear cuenta de servicio”**
3. Nombre: `fastapi-bq-access`
4. Roles:
    - `BigQuery Data Viewer`
    - `BigQuery Job User`
5. Al finalizar, **crea una clave tipo JSON**
6. Se descargará un archivo: `credentials.json`

---

## ✅ Paso 2: Habilitar Secret Manager

1. Ve a API Library
2. Busca “Secret Manager API”
3. Haz clic en **"Habilitar"**

---

## ✅ Paso 3: Crear el secreto con las credenciales

1. Ve a Secret Manager
2. Clic en **“Crear secreto”**
3. Nombre del secreto: `fastapi-bigquery-credentials`
4. En contenido secreto: **copia y pega todo el contenido del archivo `credentials.json`**
5. Clic en **“Crear”**

---

## ✅ Paso 4: Dar permisos para acceder al secreto

Ve a IAM, busca tu **cuenta de servicio**, y edítala.

Agrega el siguiente rol:

- `Secret Manager Secret Accessor` (`roles/secretmanager.secretAccessor`)

Esto permite que FastAPI (ejecutándose bajo esa cuenta de servicio) pueda acceder al secreto.

---

## ✅ Paso 5: Instalar librerías necesarias

```bash
pip install fastapi uvicorn google-cloud-bigquery google-cloud-secret-manager
```


Ejecuta tu app:

```bash
uvicorn app.main:app --reload
```

Luego accede a:

`http://localhost:8000/nacionalidades`

Deberías ver los resultados de BigQuery sin tener un archivo `credentials.json` en el disco.

---

## 🛡️ Seguridad y buenas prácticas

| Recomendación | Razón |
| --- | --- |
| Nunca guardes el archivo `.json` local | Riesgo de filtración o exposición accidental |
| Usa Secret Manager para credenciales | Es el método recomendado por Google Cloud |
| Limita el acceso a secretos por IAM | Menor privilegio = mayor seguridad |



### Permiso "Accesor de secretos de Secret Manager"

Este rol es fundamental para cualquier aplicación o servicio que necesite **leer el valor o contenido real** de un secreto almacenado en Google Secret Manager. Sin este permiso, una entidad (como una cuenta de servicio) solo puede ver los metadatos del secreto (su nombre, versiones, políticas), pero no puede acceder a la información sensible que guarda.

### Identificador del Rol (IAM)

- **Nombre en la consola (español):** Accesor de secretos de Secret Manager
- **Nombre en la consola (inglés):** Secret Manager Secret Accessor
- **ID del rol:** `roles/secretmanager.secretAccessor`

---

### Qué Permite este Rol

Este rol otorga específicamente el permiso:

- `secretmanager.versions.access`: Este permiso permite a la entidad **acceder a la carga útil (payload) de una versión de un secreto**. En otras palabras, le permite descargar y leer el contenido cifrado del secreto, el cual luego se descifra para su uso.

---

### Cuándo es Necesario

Este permiso es indispensable en escenarios como el tuyo, donde:

- Una aplicación (como tu API de FastAPI) necesita recuperar credenciales, claves API, configuración de bases de datos o cualquier otra información sensible que se almacena en Secret Manager.
- Servicios de Google Cloud (como Cloud Functions, Cloud Run, GKE) necesitan leer secretos para funcionar correctamente.
- Cualquier script o proceso que requiera utilizar el valor de un secreto.

---

### Cómo Aplicarlo a tu Caso

Para tu aplicación, la cuenta de servicio `api-fastapi-bq@hospitaldigital-461216.iam.gserviceaccount.com` **debe tener asignado el rol "Accesor de secretos de Secret Manager"**. Esto le permitirá a tu código Python, al invocar `secret_client.access_secret_version(name=nombre_secreto)`, obtener exitosamente las credenciales de BigQuery sin recibir el error `403 Permission denied`.



### Roles Actuales en la Cuenta de Servicio `api-fastapi-bq`

La cuenta de servicio tiene los siguientes roles asignados, que son los que le otorgan permisos en el proyecto de Google Cloud:

1. **Usuario con acceso a secretos de Secret Manager**
    - **Equivalente en inglés:** `Secret Manager Secret Accessor`
    - **Descripción:** ¡Este es el rol clave! Otorga el permiso `secretmanager.versions.access`, que permite a tu aplicación **leer el contenido real (el payload) de una versión específica de un secreto** almacenado en Secret Manager. Este permiso es esencial para que tu FastAPI pueda obtener las credenciales de BigQuery.
2. **Usuario de trabajo de BigQuery**
    - **Equivalente en inglés:** `BigQuery Job User`
    - **Descripción:** Este rol permite a la cuenta de servicio ejecutar trabajos en BigQuery, como consultas (`client.query(query)`), trabajos de carga, exportación o copia. Es fundamental para interactuar con BigQuery a nivel de ejecución de operaciones.
3. **Visualizador de datos de BigQuery**
    - **Equivalente en inglés:** `BigQuery Data Viewer`
    - **Descripción:** Este rol proporciona permisos de solo lectura sobre los datos dentro de BigQuery. Permite a la cuenta de servicio **leer filas de tablas y vistas**, lo cual es necesario para obtener los resultados de tus consultas BigQuery, como en tu endpoint `/nacionalidades`.



# ANEXOS

![Cuenta de servicio](https://storage.googleapis.com/fastapi-bigquery-credentials/cuenta_servicio.png)

![IAM](https://storage.googleapis.com/fastapi-bigquery-credentials/iam.png)

![Secret Manager](https://storage.googleapis.com/fastapi-bigquery-credentials/secret_manager.png)

![Bucket](https://storage.googleapis.com/fastapi-bigquery-credentials/bucket.png)
