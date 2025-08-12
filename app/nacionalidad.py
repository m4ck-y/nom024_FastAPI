# routers/nacionalidades.py

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.bd import client
from google.cloud import bigquery
from pydantic import BaseModel, Field

MODULE_NAME = "nacionalidades"

router_nacionalidades = APIRouter(prefix=f"/{MODULE_NAME}", tags=[MODULE_NAME])

TAG_NACIONALIDADES = {
    "name": MODULE_NAME,
    "description": """
🌍 Estructura del dataset:
Código de País → País → Clave Nacionalidad

🔍 Funcionalidad:
- Listado completo de nacionalidades
- Consulta por código de país
- Consulta por clave de nacionalidad
"""
}

class SchemaNacionalidad(BaseModel):
    CODIGO_PAIS: int = Field(
        ...,
        description="Código numérico del país",
        examples=[223]
    )
    PAIS: str = Field(
        ...,
        description="Nombre del país",
        examples=["MEXICANA"]
    )
    CLAVE_NACIONALIDAD: str = Field(
        ...,
        description="Clave asociada a la nacionalidad",
        examples=["MEX"]
    )

@router_nacionalidades.get("")
def obtener_nacionalidades() -> list[SchemaNacionalidad]:
    """
    Recupera la lista completa de nacionalidades registradas en el catálogo.

    Args:
        No recibe parámetros.

    Returns:
        list[SchemaNacionalidad]: Lista de diccionarios con código de país, nombre del país y clave de nacionalidad.
    """
    query = """
        SELECT
            `codigo pais` AS CODIGO_PAIS,
            `pais` AS PAIS,
            `clave nacionalidad` AS CLAVE_NACIONALIDAD
        FROM
            `hospitaldigital-461216.nom024.cat_nacionalidades`
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job.result()]


@router_nacionalidades.get("/pais")
def obtener_pais_por_clave_nacionalidad(clave_nacionalidad: str = Query(...)) -> SchemaNacionalidad:
    """
    Recupera el país y su código asociados a una nacionalidad específica.

    Args:
        clave_nacionalidad (str): **Clave única de la nacionalidad** que se utilizará para consultar el país correspondiente.

    Returns:
        SchemaNacionalidad: Diccionario con código de país, nombre del país y clave de nacionalidad. Lanza 404 si no se encuentra.
    """
    query = """
        SELECT
            `codigo pais` AS CODIGO_PAIS,
            `pais` AS PAIS,
            `clave nacionalidad` AS CLAVE_NACIONALIDAD
        FROM
            `hospitaldigital-461216.nom024.cat_nacionalidades`
        WHERE
            `clave nacionalidad` = @param
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("param", "STRING", clave_nacionalidad)
        ]
    )
    query_job = client.query(query, job_config=job_config)
    result = list(query_job.result())
    if not result:
        raise HTTPException(status_code=404, detail="Nacionalidad no encontrada")
    return dict(result[0])


@router_nacionalidades.get("/codigo_pais")
def obtener_nacionalidades_de_pais(value: int = Query(...)) -> list[SchemaNacionalidad]:
    """
    Recupera las nacionalidades correspondientes a un país específico mediante su código.

    Args:
        value (int): **Código del país** utilizado como filtro para obtener las nacionalidades asociadas.

    Returns:
        list[SchemaNacionalidad]: Lista de diccionarios con código de país, nombre del país y clave de nacionalidad.
    """
    query = """
        SELECT
            `codigo pais` AS CODIGO_PAIS,
            `pais` AS PAIS,
            `clave nacionalidad` AS CLAVE_NACIONALIDAD
        FROM
            `hospitaldigital-461216.nom024.cat_nacionalidades`
        WHERE
            `codigo pais` = @param
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("param", "INT64", value)
        ]
    )
    query_job = client.query(query, job_config=job_config)
    results = list(query_job.result())
    if not results:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return [dict(row) for row in results]
