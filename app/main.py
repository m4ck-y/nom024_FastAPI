from fastapi import FastAPI, HTTPException
from app.bd import client
from app.religion import router_religion

app = FastAPI()

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