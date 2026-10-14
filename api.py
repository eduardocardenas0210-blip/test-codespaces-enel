import json

from fastapi import FastAPI
from pydantic import BaseModel

from validar_caso import validar

app = FastAPI(title="Validación Casos Enel")


class Correo(BaseModel):
    asunto: str = ""
    cuerpo: str = ""


@app.get("/")
def salud():
    return {"estado": "ok"}


@app.post("/validar")
def endpoint(c: Correo):
    return json.loads(validar(c.asunto, c.cuerpo))
