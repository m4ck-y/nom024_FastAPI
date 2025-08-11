from fastapi import FastAPI, HTTPException
from app.bd import client
from app.religion import router_religion

openapi_tags = [
    {
        "name": "religiones",
        "description": """
🔗 Estructura jerárquica:
Credo → Grupo → Denominación → Religión

🔍 Funcionalidad:
- Listado por nivel jerárquico
- Filtros ascendentes (por clave del nivel padre)
- Acceso directo por clave única
"""
    }
]


app = FastAPI(
    title="API de Catálogos SIRES",
    version="1.0.0",
    description="""

Catálogos Fundamentales para SIRES basados en la [NOM-024-SSA3-2012](http://www.dgis.salud.gob.mx//contenidos/normatividad/normas_gobmx.html).

Contexto Normativo:
Los Sistemas de Información de Registro Electrónico para la Salud (SIRES) deben utilizar los catálogos definidos en la Matriz de Catálogos Fundamentales para garantizar interoperabilidad semántica y estructurada.

Objetivo:
- Facilitar el registro estandarizado y la calidad de datos.
- Permitir explotación estadística y epidemiológica.
- Asegurar actualización continua mediante descarga e integración de catálogos oficiales.

Documentación oficial y catálogos base:
[http://www.dgis.salud.gob.mx/contenidos/intercambio/iis_catalogos_gobmx.html](http://www.dgis.salud.gob.mx/contenidos/intercambio/iis_catalogos_gobmx.html)

Contacto para dudas o uso:
dgis@salud.gob.mx (Asunto: Catálogos)

Guía técnica integrada:
- Uso de FastAPI + BigQuery + Google Secret Manager + Google Cloud Run
- Consulta en tiempo real desde BigQuery
- Seguridad con manejo de credenciales dinámico
- Documentación OpenAPI interactiva con Swagger

Para más detalles técnicos, pasos de configuración y diagramas, revisa la documentación interna del proyecto o contáctanos.

API para exponer catálogos normalizados conforme NOM-024-SSA3-2012,
que permiten interoperabilidad en sistemas de salud (SIRES).
Incluye integración con BigQuery y seguridad con Google Secret Manager.
""",
    openapi_tags=openapi_tags)

app.include_router(router_religion)

# Endpoint para obtener todas las nacionalidades
@app.get("/nacionalidades")
def obtener_nacionalidades():
    query = """
        SELECT
            * 
        FROM
            `hospitaldigital-461216.nom024.cat_nacionalidades`
    """
    query_job = client.query(query)
    results = query_job.result()

    return [dict(row) for row in results]