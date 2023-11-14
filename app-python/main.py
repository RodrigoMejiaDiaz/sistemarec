#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import jsonify

from recommender import RecomendacionPeliculas
from recommender import hola

app = Flask(__name__)
r = RecomendacionPeliculas()


@app.route("/")
def index():
    return hola()


@app.route("/cargar")
def cargar_csv():
    try:
        archivo = "./Movie_Ratings.csv"
        # Procesar el archivo CSV
        datos_csv = procesar_csv(archivo)
        return jsonify(
            {"mensaje": "Archivo CSV cargado exitosamente", "datos": datos_csv}
        )
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo: {str(e)}"})


# Función para procesar el archivo CSV
def procesar_csv(archivo):
    r.cargar_datos_desde_csv(archivo)
    vecinos = r.knn("Heather", r.pearson)

    return vecinos


app.run(host="0.0.0.0", port=5000, debug=True)
