from fastapi import Query, HTTPException
from app.bd import client
from google.cloud import bigquery
from app.codigo_postal.config import router_codigos_postales
from app.codigo_postal.models import SchemaCodigoPostal


@router_codigos_postales.get("")
def obtener_codigos_postales(codigo_postal: int) -> list[SchemaCodigoPostal]:
    """
    Recupera los registros que coincidan con el código postal recibido.

    Args:
        codigo_postal (int): Código postal a buscar.

    Returns:
        list[dict]: Lista de registros que coinciden con el código postal.
    """
    query = f"""
    SELECT
        d_codigo       AS D_CODIGO,
        d_asenta       AS D_ASENTA,
        d_tipo_asenta  AS D_TIPO_ASENTA,
        D_mnpio        AS D_MNPIO,
        d_estado       AS D_ESTADO,
        d_ciudad       AS D_CIUDAD,
        d_CP           AS D_CP,
        c_estado       AS C_ESTADO,
        c_oficina      AS C_OFICINA,
        c_CP           AS C_CP,
        c_tipo_asenta  AS C_TIPO_ASENTA,
        c_mnpio        AS C_MNPIO,
        id_asenta_cpcons AS ID_ASENTA_CPCONS,
        d_zona         AS D_ZONA,
        c_cve_ciudad   AS C_CVE_CIUDAD
    FROM
        `hospitaldigital-461216.nom024.cat_codigos_postales`
    WHERE
        d_codigo = @codigo_postal
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("codigo_postal", "INT64", codigo_postal)
        ]
    )

    query_job = client.query(query, job_config=job_config)
    results = [dict(row) for row in query_job.result()]

    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron registros para el código postal proporcionado")

    return results
