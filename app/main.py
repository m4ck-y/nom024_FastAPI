from fastapi import FastAPI
from google.cloud import bigquery
import os

app = FastAPI()

# Ruta al archivo de credenciales de tu cuenta de servicio de GCP
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Inicializa el cliente de BigQuery
client = bigquery.Client()

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

    datos = [dict(row) for row in results]
    return datos