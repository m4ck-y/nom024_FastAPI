# Módulo Nacionalidad - Documentación de Diseño

## Estructura del Módulo

```
app/nacionalidad/
├── __init__.py          # Punto de entrada y exports públicos
├── models.py           # Esquemas Pydantic (modelos de datos)
├── routes.py           # Definición de endpoints y lógica de negocio
├── config.py           # Configuración del router y metadatos
└── README.md           # Esta documentación
```

## Decisiones de Diseño

### ¿Por qué esta estructura?

**Problema inicial**: Todo el código estaba en `__init__.py`, lo cual no es una buena práctica.

**Solución adoptada**: Estructura minimalista que separa responsabilidades sin sobre-ingeniería.

### ¿Por qué no separar `services.py` y `routes.py`?

**Consideración**: Para módulos pequeños como este, separar servicios y rutas genera:
- **Redundancia** en docstrings (misma documentación en ambos archivos)
- **Complejidad innecesaria** sin beneficios claros
- **Más archivos** para mantener

**Decisión**: Mantener rutas + lógica de negocio juntas en `routes.py` para simplicidad.

### ¿Por qué `models.py` en lugar de `schema.py`?

**Razón**: `models.py` es la convención más estándar en el ecosistema Python/FastAPI para esquemas Pydantic.

## Preguntas Frecuentes

### ¿Qué hace `__all__` en `__init__.py`?

```python
__all__ = ["router_nacionalidades", "TAG_NACIONALIDADES", "SchemaNacionalidad"]
```

**Propósito**: Define qué elementos se exportan públicamente cuando alguien hace `from app.nacionalidad import *`.

**Beneficios**:
- **API limpia**: Solo expone lo que realmente debe ser público
- **Evita contaminación**: No importa dependencias internas accidentalmente
- **Documentación implícita**: Muestra claramente qué es público vs privado
- **Mejor IDE**: Los editores sugieren solo importaciones relevantes

**Sin `__all__`**:
```python
from app.nacionalidad import *  # Importa TODO (incluso imports internos como Query, HTTPException, client)
```

**Con `__all__`**:
```python
from app.nacionalidad import *  # Solo importa lo definido en __all__
```

### ¿Por qué `from app.nacionalidad import routes` en `__init__.py`?

```python
from app.nacionalidad import routes  # ¿Para qué sirve esto?
```

**Respuesta**: Es para **cargar y ejecutar** el archivo `routes.py`.

**¿Qué pasa internamente?**:
1. Se ejecuta `routes.py`
2. Se procesan los decoradores `@router_nacionalidades.get("")`
3. Se registran las rutas en el objeto `router_nacionalidades`
4. No se usa la variable `routes` para nada más

**Sin esta importación**:
- `routes.py` nunca se ejecuta
- Los decoradores nunca se procesan
- `router_nacionalidades` queda vacío (sin rutas)
- Tu API no tiene endpoints

**Con esta importación**:
- `routes.py` se ejecuta automáticamente
- Las rutas se registran
- Todo funciona correctamente

Es un "efecto secundario" útil de la importación - el archivo se carga solo para que sus decoradores hagan su trabajo.

### ¿Cuándo usar esta estructura vs una más compleja?

**Usa esta estructura cuando**:
- El módulo tiene pocas rutas (< 10 endpoints)
- La lógica de negocio es simple
- No necesitas reutilizar servicios en otros módulos
- El equipo prefiere simplicidad

**Considera estructura más compleja cuando**:
- Tienes muchos endpoints (> 10)
- Lógica de negocio compleja que se reutiliza
- Múltiples fuentes de datos
- Necesitas testing granular de servicios

## Ventajas de esta Estructura

1. **Simplicidad**: Fácil de entender y navegar
2. **Mantenibilidad**: Menos archivos que mantener
3. **Sin redundancia**: Docstrings únicos
4. **Convenciones estándar**: Sigue patrones comunes de FastAPI
5. **Escalabilidad**: Fácil de refactorizar si crece el módulo

## Ejemplo de Uso

```python
# En main.py
from app.nacionalidad import router_nacionalidades, TAG_NACIONALIDADES

app.include_router(router_nacionalidades)
```

```python
# En otros módulos
from app.nacionalidad import SchemaNacionalidad

def alguna_funcion() -> SchemaNacionalidad:
    # usar el esquema
    pass
```

## Conclusión

Esta estructura balanceada ofrece organización sin complejidad innecesaria, perfecta para módulos de tamaño pequeño a mediano que necesitan mantenerse simples y mantenibles.