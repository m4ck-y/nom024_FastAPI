from pydantic import BaseModel, Field


class SchemaNacionalidad(BaseModel):
    CODIGO_PAIS: int = Field(
        ...,
        description="Código numérico del país",
        examples=[223]
    )
    PAIS: str = Field(
        ...,
        description="Nombre del país",
        examples=["MEXICANA"]
    )
    CLAVE_NACIONALIDAD: str = Field(
        ...,
        description="Clave asociada a la nacionalidad",
        examples=["MEX"]
    )