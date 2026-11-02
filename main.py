from typing_extensions import Literal
from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI(title="Muro de SOINU EQUIPO 4")

class CompraNueva(BaseModel):
    nombre_entrada: Literal["Abono general", "Day Pass", "VIP", "Abono + parcela"]
    fecha: date | None = None
    cantidad: int = Field(ge=1, le=6)
    nombre: str = Field(min_length=2, max_length=50)
    apellido: str = Field(min_length=2, max_length=50)
    correo: str = Field(max_length=100, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @field_validator("nombre", "apellido", "correo", mode="before")
    @classmethod        
    def quitar_espacios(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("correo", mode="before")
    @classmethod
    def correo_en_minusculas(cls, v):
        return v.strip().lower() if isinstance(v, str) else v

    @model_validator(mode="after")
    def comprobar_fecha(self):
        if self.nombre_entrada == "Day Pass":
            entrada = buscar_entrada_por_nombre(self.nombre_entrada)
            if entrada is None:
                raise ValueError("Tipo de entrada no válido")
            inicio = date.fromisoformat(entrada["fecha_inicio"])
            fin = date.fromisoformat(entrada["fecha_fin"])
            if self.fecha is None:
                raise ValueError("Elige el día para el Day Pass")
            if not inicio <= self.fecha <= fin:
                raise ValueError("El día elegido debe estar dentro del festival")
        return self


def buscar_entrada_por_nombre(nombre):
    """Devuelve el tipo de entrada con ese nombre, o None si no existe."""
    for entrada in ENTRADAS:
        if entrada["nombre"] == nombre:
            return entrada
    return None

def siguiente_id(COMPRAS):
    return max((m["id"] for m in COMPRAS), default=0) + 1

def calcular_total(nombre_entrada, cantidad):
    entrada = buscar_entrada_por_nombre(nombre_entrada)
    if entrada is None:
        raise ValueError("Tipo de entrada no válido")
    return entrada["precio"] * cantidad

def obtener_plazas_totales(nombre_entrada):
    # Más adelante: consulta a la base de datos
    return PLAZAS_TOTALES[nombre_entrada]

def plazas_libres(entrada):
    vendidas = sum(c["cantidad"] for c in COMPRAS if c["nombre_entrada"] == entrada["nombre"])
    return obtener_plazas_totales(entrada["nombre"]) - vendidas

# ---------- API (JSON) ----------
@app.get("/api/entradas")
def obtener_entradas():
    return ENTRADAS

# 1. GET /salud → {"ok": True, "app": "Muro"}

ENTRADAS = [
    {"id": 1, "nombre": "Abono general", "descripcion": "Acceso a todos los días del festival.", "precio": 80.0, "fecha_inicio": "2026-09-01", "fecha_fin": "2026-09-15", "zonas_acceso": "General", "estado": "disponible"},
    {"id": 2, "nombre": "Day Pass", "descripcion": "Acceso a un único día del festival.", "precio": 35.0, "fecha_inicio": "2026-09-01", "fecha_fin": "2026-09-15", "zonas_acceso": "General", "estado": "disponible"},
    {"id": 3, "nombre": "VIP", "descripcion": "Acceso a todos los días con zona VIP y barra propia.", "precio": 150.0, "fecha_inicio": "2026-09-01", "fecha_fin": "2026-09-15", "zonas_acceso": "General y VIP", "estado": "disponible"},
    {"id": 4, "nombre": "Abono + parcela", "descripcion": "Abono general más parcela en la zona de acampada.", "precio": 110.0, "fecha_inicio": "2026-09-01", "fecha_fin": "2026-09-15", "zonas_acceso": "General y Acampada", "estado": "disponible"},
]
COMPRAS = []

PLAZAS_TOTALES = {
    "Abono general": 500,
    "Day Pass": 300,
    "VIP": 100,
    "Abono + parcela": 80,
}


# ---------- PRUEBA (en el Aula; en tu ordenador: python main.py) ----------
if __name__ == "__main__":
    from aula import Cliente
    c = Cliente(app)
    print(c.get("/salud").json())
