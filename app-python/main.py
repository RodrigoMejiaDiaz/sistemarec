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
        # archivo10m = "./ml-10M100K/"
        archivo25m = "./ml-25m/"
        # Recolectar datos si existen ya en Redis
        jsondatos = redis_conn.get("ratings")
        if not jsondatos:
            # Procesar 10M datos
            # datos = procesar_10M(archivo10m)

            # Procesar 25M datos
            datos = procesar_25M(archivo25m)
            jsondatos = json.dumps(datos)
            # Guardar datos en Redis
            redis_conn.set("ratings", jsondatos)

            # Cargar peliculas
            peliculas = cargar_peliculas()
            redis_conn.set("peliculas", json.dumps(peliculas))

        response = app.response_class(
            status=200, mimetype="application/json", response="Datos cargados"
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo: {str(e)}"})


@app.route("/api/knn/<usuario>/<distancia>")
def calcular_vecinos(usuario, distancia):
    try:
        jsonvecinos = redis_conn.get("knn")
        if not jsonvecinos:
            vecinos = procesar_knn(usuario, distancia)
            jsonvecinos = json.dumps(vecinos)
            jsonvecinos_redis = {usuario: vecinos}
            redis_conn.lpush("knn", json.dumps(jsonvecinos_redis))
        response = app.response_class(
            status=200, mimetype="application/json", response=jsonvecinos
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al calcular vecinos: {str(e)}"})


@app.route("/api/recommend/<usuario>/<distancia>/<int:n_kk>/<int:n_items>")
def calcular_recommend(usuario, distancia, n_kk, n_items):
    try:
        jsonrecomendaciones = redis_conn.get("rec")
        if not jsonrecomendaciones:
            recomendaciones = procesar_recommend(usuario, distancia, n_kk, n_items)
            jsonrecomendaciones = json.dumps(recomendaciones)
            jsonrecomendaciones_redis = {usuario: recomendaciones}
            redis_conn.lpush("rec", json.dumps(jsonrecomendaciones_redis))
        response = app.response_class(
            status=200, mimetype="application/json", response=jsonrecomendaciones
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al calcular recomendaciones: {str(e)}"})


@app.route("/api/promedios")
def calculas_promedio():
    try:
        jsonpromedios = redis_conn.get("promedios")
        if not jsonpromedios:
            promedios = procesar_promedio()
            jsonpromedios = json.dumps(promedios)
            redis_conn.set("promedios", jsonpromedios)
        response = app.response_class(
            status=200, mimetype="application/json", response=jsonpromedios
        )
        return response
    except Exception as e:
        return jsonify({"error": f"Error al calcular promedios: {str(e)}"})


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


# Cargar Movie lens 25M
def procesar_25M(path):
    r.cargarMovieLens25M(path)
    data = r.data
    return data


# Cargar peliculas guardadas
def cargar_peliculas():
    data = r.productid2name
    return data


# Calcular knn
def procesar_knn(usuario, distancia):
    data = r.knn(usuario, distancia)
    return data


# Calcular recommend
def procesar_recommend(usuario, distancia, n_kk, n_items):
    data = r.recommend(usuario, distancia, n_kk, n_items)
    return data


# Calcular promedios peliculas
def procesar_promedio():
    data = r.calcular_promedio_peliculas()
    return data


app.run(host="0.0.0.0", port=5010, debug=True)
