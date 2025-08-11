# 📘 Documentación y Resumen del Dataset y API de Religiones

## 🗂️ Introducción al Dataset

El dataset proviene del catálogo desnormalizado de religiones, optimizado para **consultas rápidas y de alta lectura** en BigQuery. Cada registro representa una religión específica e incluye toda su jerarquía ascendente.

| Columna | Descripción | Ejemplo |
| --- | --- | --- |
| `CLAVE_CREDO` | Identificador único del credo | `1` |
| `CREDO` | Nombre del credo | `CRISTIANO` |
| `CLAVE_GRUPO` | Identificador del grupo religioso | `11` |
| `GRUPO` | Nombre del grupo religioso | `Católicos` |
| `CLAVE_DENOMINACION` | Identificador de la denominación religiosa | `1101` |
| `DENOMINACION` | Nombre de la denominación | `Católicos` |
| `CLAVE_RELIGION` | Identificador único de la religión específica | `110101` |
| `RELIGION` | Nombre completo de la religión | `Católico Apostólico Romano` |

### 📌 Ejemplo de registro:

| CLAVE_CREDO | CREDO | CLAVE_GRUPO | GRUPO | CLAVE_DENOMINACION | DENOMINACION | CLAVE_RELIGION | RELIGION |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CRISTIANO | 11 | Católicos | 1101 | Católicos | 110101 | Católico Apostólico Romano |

---

## 🔎 Análisis y Diseño de Rutas Esenciales

Dado que la base de datos es **jerárquica y desnormalizada**, se diseñaron rutas REST para facilitar el acceso y navegación **de forma descendente (de credo a religión)** y también **filtros ascendentes (desde religión hacia sus agrupadores)**.

| Nivel Jerárquico | Endpoint | Filtro | Descripción |
| --- | --- | --- | --- |
| **Credos** | `GET /religiones/credos` | – | Lista única de todos los credos disponibles |
| **Grupos** | `GET /religiones/grupos` | `?clave_credo=` | Lista de grupos religiosos. Se puede filtrar por un credo específico |
| **Denominaciones** | `GET /religiones/denominaciones` | `?clave_grupo=` | Lista de denominaciones religiosas. Se puede filtrar por grupo |
| **Religiones** | `GET /religiones` | `?clave_denominacion=` | Lista completa de religiones. Se puede filtrar por denominación |

### 🔁 Exploración jerárquica

Estos endpoints permiten **acceder en cascada** desde el nivel más general (credos) hasta el más específico (religiones):

```
Credo → Grupo → Denominación → Religión
```

Ejemplos:

- `/religiones/grupos?clave_credo=1`
- `/religiones/denominaciones?clave_grupo=11`
- `/religiones?clave_denominacion=1101`

---

## 🔍 Endpoints para Acceso Directo por Clave

Para obtener detalles de una entidad específica a partir de su clave única:

| Entidad | Endpoint | Retorna |
| --- | --- | --- |
| Credo | `GET /religiones/credo/{clave_credo}` | `CLAVE_CREDO`, `CREDO` |
| Grupo | `GET /religiones/grupo/{clave_grupo}` | `CLAVE_CREDO`, `CLAVE_GRUPO`, `GRUPO` |
| Denominación | `GET /religiones/denominacion/{clave_denominacion}` | `CLAVE_CREDO`, `CLAVE_GRUPO`, `CLAVE_DENOMINACION`, `DENOMINACION` |
| Religión | `GET /religiones/religion/{clave_religion}` | `CLAVE_CREDO`, `CLAVE_GRUPO`, `CLAVE_DENOMINACION`, `CLAVE_RELIGION`, `RELIGION` |

---

## 🧠 Regla Mental para Nuevos Diseños

> "Si una columna agrupa a otra, la API debe permitir: listar, filtrar, y obtener por clave tanto la agrupadora como la agrupada."
> 

### 📋 Checklist de Rutas para Cualquier Nivel Jerárquico

| Tipo de Ruta | Descripción |
| --- | --- |
| `GET /a` | Lista única de valores de nivel A |
| `GET /a/{a_key}` | Detalle de un elemento A por su clave |
| `GET /b` | Lista de valores B (con posibilidad de filtro por `a_key`) |
| `GET /b/{b_key}` | Detalle de un elemento B |
| `GET /a/{a_key}/b` *(opcional)* | Elementos B dentro de un A (solo si quieres hacerlo explícito) |

Esto te servirá como **plantilla de diseño** para futuras APIs con jerarquías similares (por ejemplo: países → estados → municipios → colonias).

---

## 🧪 Ejemplos de Consulta Reales

- 🔹 **Obtener todos los grupos del credo Cristiano**:
    
    ```
    GET /religiones/grupos?clave_credo=1
    ```
    
- 🔹 **Obtener todas las denominaciones del grupo 11**:
    
    ```
    GET /religiones/denominaciones?clave_grupo=11
    ```
    
- 🔹 **Religiones asociadas a la denominación 1101**:
    
    ```
    GET /religiones?clave_denominacion=1101
    ```
    
- 🔸 **Obtener detalle completo de la religión 110101**:
    
    ```
    GET /religiones/religion/110101
    ```
    

---

## ⚡ Consideraciones Técnicas

- Esta API está construida sobre un único dataset de BigQuery.
- Las consultas son todas `SELECT DISTINCT` para garantizar resultados únicos.
- No hay operaciones de escritura; es una API de lectura intensiva.
- El diseño REST es completamente stateless y jerárquico.