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