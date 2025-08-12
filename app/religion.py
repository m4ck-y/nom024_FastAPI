# routers/religiones.py

from typing import Optional
from fastapi import APIRouter, Query
from app.bd import client
from google.cloud import bigquery

MODULE_NAME = "religiones"

# Se define el enrutador para las rutas relacionadas con la jerarquía religiosa.
router_religion = APIRouter(prefix=f"/{MODULE_NAME}", tags=[MODULE_NAME])

TAG_RELIGIONES = {
        "name": MODULE_NAME,
        "description": """
🔗 Estructura jerárquica:
Credo → Grupo → Denominación → Religión

🔍 Funcionalidad:
- Listado por nivel jerárquico
- Filtros ascendentes (por clave del nivel padre)
- Acceso directo por clave única
"""
    }


@router_religion.get("/credos")
def obtener_credos() -> list[dict]:
    """
    Recupera la lista única de credos registrados en la base de datos.

    Returns:
        list: Lista de diccionarios que contienen claves y nombres de credos únicos.
    """
    query = """
        SELECT DISTINCT
            CLAVE_CREDO,
            CREDO
        FROM
            `hospitaldigital-461216.nom024.cat_religiones`
    """
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]


@router_religion.get("/credo/{clave_credo}")
def obtener_credo_por_clave(clave_credo: int) -> dict:
    """
    Recupera la información de un credo específico según su clave única.

    Args:
        clave_credo (int): **Identificador único** del credo a consultar.

    Returns:
        dict: Diccionario con la clave y el nombre del credo, o un diccionario vacío si no se encuentra.
    """
    query = """
        SELECT DISTINCT
            CLAVE_CREDO,
            CREDO
        FROM
            `hospitaldigital-461216.nom024.cat_religiones`
        WHERE
            CLAVE_CREDO = @param
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("param", "INT64", clave_credo)]
    )
    query_job = client.query(query, job_config=job_config)
    result = list(query_job.result())
    return dict(result[0]) if result else {}


@router_religion.get("/grupos")
def obtener_grupos(clave_credo: Optional[int] = Query(None)) -> list[dict]:
    """
    Recupera la lista de grupos religiosos. Si se proporciona una clave de credo, filtra los resultados.

    Args:
        clave_credo (Optional[int]): **Clave opcional del credo** utilizada para filtrar los grupos correspondientes.

    Returns:
        list: Lista de diccionarios con claves y nombres de grupos religiosos.
    """
    if clave_credo is not None:
        query = """
            SELECT DISTINCT
                CLAVE_CREDO,
                CLAVE_GRUPO,
                GRUPO
            FROM
                `hospitaldigital-461216.nom024.cat_religiones`
            WHERE
                CLAVE_CREDO = @param
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("param", "INT64", clave_credo)]
        )
    else:
        query = """
            SELECT DISTINCT
                CLAVE_CREDO,
                CLAVE_GRUPO,
                GRUPO
            FROM
                `hospitaldigital-461216.nom024.cat_religiones`
        """
        job_config = None

    query_job = client.query(query, job_config=job_config)
    return [dict(row) for row in query_job.result()]


@router_religion.get("/grupo/{clave_grupo}")
def obtener_grupo_por_clave(clave_grupo: int) -> dict:
    """
    Recupera la información de un grupo religioso específico según su clave única.

    Args:
        clave_grupo (int): **Identificador único** del grupo religioso a consultar.

    Returns:
        dict: Diccionario con información del grupo, o un diccionario vacío si no se encuentra.
    """
    query = """
        SELECT DISTINCT
            CLAVE_CREDO,
            CLAVE_GRUPO,
            GRUPO
        FROM
            `hospitaldigital-461216.nom024.cat_religiones`
        WHERE
            CLAVE_GRUPO = @param
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("param", "INT64", clave_grupo)]
    )
    query_job = client.query(query, job_config=job_config)
    result = list(query_job.result())
    return dict(result[0]) if result else {}


@router_religion.get("/denominaciones")
def obtener_denominaciones(clave_grupo: Optional[int] = Query(None)) -> list[dict]:
    """
    Recupera la lista de denominaciones religiosas. Si se proporciona una clave de grupo, filtra los resultados.

    Args:
        clave_grupo (Optional[int]): **Clave opcional del grupo religioso** utilizada para filtrar las denominaciones correspondientes.

    Returns:
        list: Lista de diccionarios con claves y nombres de denominaciones religiosas.
    """
    if clave_grupo is not None:
        query = """
            SELECT DISTINCT
                CLAVE_GRUPO,
                CLAVE_DENOMINACION,
                DENOMINACION
            FROM
                `hospitaldigital-461216.nom024.cat_religiones`
            WHERE
                CLAVE_GRUPO = @param
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("param", "INT64", clave_grupo)]
        )
    else:
        query = """
            SELECT DISTINCT
                CLAVE_GRUPO,
                CLAVE_DENOMINACION,
                DENOMINACION
            FROM
                `hospitaldigital-461216.nom024.cat_religiones`
        """
        job_config = None

    query_job = client.query(query, job_config=job_config)
    return [dict(row) for row in query_job.result()]


@router_religion.get("/denominacion/{clave_denominacion}")
def obtener_denominacion_por_clave(clave_denominacion: int) -> dict:
    """
    Recupera la información de una denominación religiosa específica según su clave única.

    Args:
        clave_denominacion (int): **Identificador único** de la denominación religiosa.

    Returns:
        dict: Diccionario con la información jerárquica de la denominación, o un diccionario vacío si no se encuentra.
    """
    query = """
        SELECT DISTINCT
            CLAVE_CREDO,
            CLAVE_GRUPO,
            CLAVE_DENOMINACION,
            DENOMINACION
        FROM
            `hospitaldigital-461216.nom024.cat_religiones`
        WHERE
            CLAVE_DENOMINACION = @param
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("param", "INT64", clave_denominacion)]
    )
    query_job = client.query(query, job_config=job_config)
    result = list(query_job.result())
    return dict(result[0]) if result else {}


@router_religion.get("")
def obtener_religiones(clave_denominacion: Optional[int] = Query(None)) -> list[dict]:
    """
    Recupera la lista de religiones. Si se proporciona una clave de denominación, filtra por dicha clave.

    Args:
        clave_denominacion (Optional[int]): **Clave opcional de denominación religiosa** utilizada para filtrar los resultados.

    Returns:
        list: Lista de diccionarios con información jerárquica completa de las religiones.
    """
    if clave_denominacion is not None:
        query = """
            SELECT
                CLAVE_CREDO,
                CLAVE_GRUPO,
                CLAVE_DENOMINACION,
                CLAVE_RELIGION,
                RELIGION
            FROM
                `hospitaldigital-461216.nom024.cat_religiones`
            WHERE
                CLAVE_DENOMINACION = @param
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("param", "INT64", clave_denominacion)
            ]
        )
    else:
        query = """
            SELECT
                CLAVE_CREDO,
                CLAVE_GRUPO,
                CLAVE_DENOMINACION,
                CLAVE_RELIGION,
                RELIGION
            FROM
                `hospitaldigital-461216.nom024.cat_religiones`
        """
        job_config = None

    query_job = client.query(query, job_config=job_config)
    return [dict(row) for row in query_job.result()]


@router_religion.get("/religion/{clave_religion}")
def obtener_religion_por_clave(clave_religion: int) -> dict:
    """
    Recupera la información jerárquica completa de una religión específica según su clave única.

    Args:
        clave_religion (int): **Identificador único** de la religión a consultar.

    Returns:
        dict: Diccionario con clave y nombre de la religión, o un diccionario vacío si no se encuentra.
    """
    query = """
        SELECT DISTINCT
            CLAVE_CREDO,
            CLAVE_GRUPO,
            CLAVE_DENOMINACION,
            CLAVE_RELIGION,
            RELIGION
        FROM
            `hospitaldigital-461216.nom024.cat_religiones`
        WHERE
            CLAVE_RELIGION = @param
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("param", "INT64", clave_religion)]
    )
    query_job = client.query(query, job_config=job_config)
    result = list(query_job.result())
    return dict(result[0]) if result else {}
