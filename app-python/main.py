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
def cargar_datos():
    try:
        archivo = "./ml-10M100K/"
        # Recolectar datos si existen ya en Redis
        jsondatos = redis_conn.get("ratings")
        if not jsondatos:
            # Procesar el archivo CSV
            datos = procesar_10M(archivo)
            jsondatos = json.dumps(datos)
            # Guardar datos en Redis
            redis_conn.set("ratings", jsondatos)
        response = app.response_class(
            status=200, mimetype="application/json", response="Datos cargados"
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo: {str(e)}"})


@app.route("/api/knn/<usuario>/<distancia>")
def calcular_vecinos(usuario, distancia):
    try:
        u = "knn" + usuario
        jsonvecinos = redis_conn.get(u)
        if not jsonvecinos:
            vecinos = procesar_knn(usuario, distancia)
            jsonvecinos = json.dumps(vecinos)
            redis_conn.set(u, jsonvecinos)
        response = app.response_class(
            status=200, mimetype="application/json", response=jsonvecinos
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al calcular vecinos: {str(e)}"})


@app.route("/api/recommend/<usuario>/<distancia>/<int:n_kk>/<int:n_items>")
def calcular_recommend(usuario, distancia, n_kk, n_items):
    try:
        u = "rec" + usuario
        jsonrecomendaciones = redis_conn.get(u)
        if not jsonrecomendaciones:
            recomendaciones = procesar_recommend(usuario, distancia, n_kk, n_items)
            jsonrecomendaciones = json.dumps(recomendaciones)
            redis_conn.set(u, jsonrecomendaciones)
        response = app.response_class(
            status=200, mimetype="application/json", response=jsonrecomendaciones
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al calcular recomendaciones: {str(e)}"})


# Función para procesar el archivo CSV
def procesar_csv(archivo):
    r.cargar_datos_desde_csv(archivo)
    data = r.data
    return data


# Cargar Movie Lens 10M
def procesar_10M(path):
    r.cargarMovieLens10M(path)
    data = r.data
    return data


# Calcular knn
def procesar_knn(usuario, distancia):
    data = r.knn(usuario, distancia)
    return data


# Calcular recommend
def procesar_recommend(usuario, distancia, n_kk, n_items):
    data = r.recommend(usuario, distancia, n_kk, n_items)
    return data


app.run(host="0.0.0.0", port=5010, debug=True)
