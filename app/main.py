from fastapi import FastAPI, HTTPException
from google.cloud import bigquery, secretmanager
from google.oauth2 import service_account
import json

app = FastAPI()

project_id = "hospitaldigital-461216"
secret_id = "fastapi-bigquery-credentials"
version_id = "1"

def obtener_credenciales_desde_secret():
    #cliente de Secret Manager
    secret_client = secretmanager.SecretManagerServiceClient()

    #nombre_secreto = "projects/967885369144/secrets/fastapi-bigquery-credentials/versions/latest"
    nombre_secreto = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    # Accede al secreto
    response = secret_client.access_secret_version(name=nombre_secreto)
    print("mi response", response.name)

    secreto = response.payload.data.decode("UTF-8")
    return json.loads(secreto)
        

# Intenta cargar las credenciales al iniciar
try:
    credenciales_dict = obtener_credenciales_desde_secret()
    credenciales = service_account.Credentials.from_service_account_info(credenciales_dict)
    client = bigquery.Client(credentials=credenciales, project=credenciales.project_id)
except Exception as e:
    print(f"Error inicializando BigQuery: {str(e)}")
    client = None

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