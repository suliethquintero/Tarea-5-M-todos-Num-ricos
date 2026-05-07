import math
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI(title="Sistema de Métodos Numéricos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente"}

class DatosBiseccion(BaseModel):
    a: float
    b: float
    tol: float = 0.000001


class DatosSecante(BaseModel):
    x0: float
    x1: float
    tolerancia: float = 0.000001
    max_iter: int = 100

def f_biseccion(x):
    return 4 * x**2 - 5 * x

def f_secante(x):
    return math.exp(-x) - x

@app.post("/biseccion")
def biseccion(data: DatosBiseccion):

    a = data.a
    b = data.b

    fa = f_biseccion(a)
    fb = f_biseccion(b)

    if fa * fb >= 0:
        return {
            "error": "El intervalo no contiene una raíz"
        }

    iteraciones: List[Dict] = []

    for i in range(100):

        c = (a + b) / 2

        fc = f_biseccion(c)

        error = abs(b - a) / 2

        iteraciones.append({
            "iteracion": i + 1,
            "a": round(a, 6),
            "b": round(b, 6),
            "c": round(c, 6),
            "fc": round(fc, 6),
            "error": round(error, 6)
        })

        if abs(fc) < data.tol or error < data.tol:
            return {
                "resultado_final": {
                    "raiz": round(c, 6)
                },
                "iteraciones": iteraciones,
                "status": "success"
            }

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return {
        "error": "No convergió"
    }

@app.post("/secante")
def secante(data: DatosSecante):

    x0 = data.x0
    x1 = data.x1

    historial = []

    for i in range(data.max_iter):

        fx0 = f_secante(x0)
        fx1 = f_secante(x1)

        if fx1 - fx0 == 0:
            return {
                "error": "División por cero"
            }

        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

        error = abs(x2 - x1)

        historial.append({
            "iteracion": i + 1,
            "x0": round(x0, 6),
            "x1": round(x1, 6),
            "x2": round(x2, 6),
            "error": round(error, 6)
        })

        if error < data.tolerancia:
            return {
                "resultado_final": {
                    "raiz": round(x2, 6)
                },
                "iteraciones": historial,
                "status": "success"
            }

        x0 = x1
        x1 = x2

    return {
        "resultado_final": {
            "raiz": round(x1, 6)
        },
        "iteraciones": historial,
        "status": "success"
    }
            
