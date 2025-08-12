from fastapi import FastAPI, HTTPException
from app.bd import client
from app.religion import router_religion, TAG_RELIGIONES
from app.nacionalidad import router_nacionalidades, TAG_NACIONALIDADES


openapi_tags = [
    TAG_NACIONALIDADES,
    TAG_RELIGIONES,
]


app = FastAPI(
    title="🏥 API de Catálogos SIRES - NOM-024-SSA3-2012",
    version="1.0.0",
    description="""
Catálogos Fundamentales para SIRES basados en la [NOM-024-SSA3-2012](http://www.dgis.salud.gob.mx//contenidos/normatividad/normas_gobmx.html).

## 📋 Contexto Normativo

Los Sistemas de Información de Registro Electrónico para la Salud (SIRES) deben utilizar los catálogos definidos en la Matriz de Catálogos Fundamentales para garantizar interoperabilidad semántica y estructurada.

### 🎯 Objetivo
- Facilitar el registro estandarizado y la calidad de datos
- Permitir explotación estadística y epidemiológica  
- Asegurar actualización continua mediante descarga e integración de catálogos oficiales

### 📚 Documentación Oficial
- **Catálogos base:** [dgis.salud.gob.mx/contenidos/intercambio/iis_catalogos_gobmx.html](http://www.dgis.salud.gob.mx/contenidos/intercambio/iis_catalogos_gobmx.html)
- **Contacto:** dgis@salud.gob.mx (Asunto: Catálogos)

---

## 🚀 Arquitectura Técnica

### Stack Tecnológico
- **FastAPI** - Framework web moderno con documentación automática
- **Google BigQuery** - Consultas masivas en tiempo real
- **Google Secret Manager** - Gestión segura de credenciales
- **Google Cloud Run** - Despliegue serverless escalable
- **Docker** - Contenedorización para portabilidad

### 🔒 Características de Seguridad
- ✅ **Sin credenciales hardcodeadas** - Gestión dinámica via Secret Manager
- ✅ **Cuenta de servicio** con permisos mínimos (principio de menor privilegio)
- ✅ **Autenticación automática** en Google Cloud Platform
- ✅ **Documentación OpenAPI** interactiva con Swagger UI

### 📊 Catálogos Disponibles
- **Nacionalidades** (`/nacionalidades`) - Catálogo de nacionalidades oficiales
- **Religiones** (`/religiones/*`) - Jerarquía completa: Credo → Grupo → Denominación → Religión

---

## 🔗 Enlaces Útiles

- **🌐 API en Producción:** [catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app](https://catalogos-nom024-fastapi-bigquery-967885369144.europe-west1.run.app)
- **💻 Código Fuente:** [github.com/m4ck-y/nom024_FastAPI](https://github.com/m4ck-y/nom024_FastAPI)
""",
    openapi_tags=openapi_tags)

app.include_router(router_nacionalidades)
app.include_router(router_religion)