#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import jsonify

import redis
import os
import json

from recommender import RecomendacionPeliculas
from recommender import hola

app = Flask(__name__)
redis_conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
r = RecomendacionPeliculas()


@app.route("/")
def index():
    return hola()


@app.route("/api/cargar")
def cargar_csv():
    try:
        archivo = "./Movie_Ratings.csv"
        # Recolectar datos si existen ya en Redis
        datos = redis_conn.get("data")
        if not datos:
            # Procesar el archivo CSV
            datos = procesar_csv(archivo)
            jsondatos = json.dumps(datos)
            # Guardar datos en Redis
            redis_conn.set("data", jsondatos)
        response = app.response_class(
            status=200, mimetype="application/json", response=datos
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo: {str(e)}"})


# Función para procesar el archivo CSV
def procesar_csv(archivo):
    r.cargar_datos_desde_csv(archivo)
    data = r.data
    return data


app.run(host="0.0.0.0", port=5000, debug=True)
