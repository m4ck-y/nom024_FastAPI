from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Ruta con parámetro en la URL: /items/123
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "message": f"Item ID recibido: {item_id}"}

# Ruta con query parameter: /search?query=algo
@app.get("/search")
def search_items(query: Optional[str] = None):
    if query:
        return {"query": query, "message": f"Búsqueda realizada con: {query}"}
    else:
        return {"message": "No se proporcionó parámetro de búsqueda"}
