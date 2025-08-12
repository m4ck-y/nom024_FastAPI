from fastapi import APIRouter

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