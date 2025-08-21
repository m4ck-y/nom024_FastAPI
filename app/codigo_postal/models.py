from pydantic import BaseModel, Field
from typing import Optional

class SchemaCodigoPostal(BaseModel):
    D_CODIGO: str = Field(
        ...,
        description="Código Postal asentamiento",
        examples=["03023"]
    )
    D_ASENTA: str = Field(
        ...,
        description="Nombre asentamiento",
        examples=["Colonia Centro"]
    )
    D_TIPO_ASENTA: str = Field(
        ...,
        description="Tipo de asentamiento (Catálogo SEPOMEX)",
        examples=["Colonia"]
    )
    D_MNPIO: str = Field(
        ...,
        description="Nombre Municipio (INEGI, Marzo 2013)",
        examples=["Tulancingo"]
    )
    D_ESTADO: str = Field(
        ...,
        description="Nombre Entidad (INEGI, Marzo 2013)",
        examples=["Hidalgo"]
    )
    D_CIUDAD: Optional[str] = Field(
        None,
        description="Nombre Ciudad (Catálogo SEPOMEX)",
        examples=["Tulancingo"]
    )
    D_CP: int = Field(
        ...,
        description="Código Postal de la Administración Postal que reparte al asentamiento",
        examples=[43007]
    )
    C_ESTADO: str = Field(
        ...,
        description="Clave Entidad (INEGI, Marzo 2013)",
        examples=["13"]
    )
    C_OFICINA: str = Field(
        ...,
        description="Código Postal de la oficina postal que reparte al asentamiento",
        examples=["03023"]
    )
    C_CP: Optional[int] = Field(
        None,
        description="Campo vacío o reservado",
        examples=[None]
    )
    C_TIPO_ASENTA: str = Field(
        ...,
        description="Clave Tipo de asentamiento (Catálogo SEPOMEX)",
        examples=["29"]
    )
    C_MNPIO: str = Field(
        ...,
        description="Clave Municipio (INEGI, Marzo 2013)",
        examples=["28"]
    )
    ID_ASENTA_CPCONS: str = Field(
        ...,
        description="Identificador único del asentamiento (nivel municipal)",
        examples=["12345"]
    )
    D_ZONA: str = Field(
        ...,
        description="Zona en la que se ubica el asentamiento (Urbano/Rural)",
        examples=["Urbano"]
    )
    C_CVE_CIUDAD: Optional[str] = Field(
        None,
        description="Clave Ciudad (Catálogo SEPOMEX)",
        examples=["0101"]
    )
