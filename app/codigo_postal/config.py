from fastapi import APIRouter

MODULE_NAME = "codigos_postales"

router_codigos_postales = APIRouter(prefix=f"/{MODULE_NAME}", tags=[MODULE_NAME])

TAG_CODIGOS_POSTALES = {
    "name": MODULE_NAME,
    "description": """
📮 Estructura del dataset:
Código Postal → Asentamiento → Tipo de Asentamiento → Municipio → Estado → Ciudad → Zona

🔍 Funcionalidad:
- Listado de códigos postales por código exacto
- Consulta de asentamientos asociados a un código postal
- Información detallada de zona, municipio y ciudad según código postal
"""
}