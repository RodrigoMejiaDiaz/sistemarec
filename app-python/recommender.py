import codecs
import pandas as pd
import numpy as np
import math


def hola():
    h = "hola mundo"
    return h


class RecomendacionPeliculas:
    def __init__(self):
        self.data = {}
        self.datos_peliculas = {}
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}

    # Cargar datos Movie_Ratings.csv
    def cargar_datos_desde_csv(self, archivo_csv, encoding="utf-8"):
        with codecs.open(archivo_csv, "r") as archivo:
            df = pd.read_csv(archivo, index_col=0)

        df = df.T
        data = {}
        datos_peliculas = {}

        for usuario, fila in df.iterrows():
            datos_usuario = {
                pelicula: puntaje
                for pelicula, puntaje in fila.items()
                if not pd.isna(puntaje)
            }
            data[usuario] = datos_usuario

            for pelicula, puntaje in datos_usuario.items():
                if pelicula in datos_peliculas:
                    datos_peliculas[pelicula].append(puntaje)
                else:
                    datos_peliculas[pelicula] = [puntaje]

        self.data = data
        self.datos_peliculas = datos_peliculas

    def convertProductID2name(self, id):
        """Given product id number return product name"""
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    def userRatings(self, id, n):
        """Return n top ratings for user with id"""
        print("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v) for (k, v) in ratings]
        # finally sort and return
        ratings.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))

    # Cargar conjunto datos Users
    def cargar_conjunto_users(self, users):
        self.data = users

    # Cargar Movie-lens 100k
    def cargarMovieLens(self, path=""):
        """loads the Movie Lens dataset. Path is where the u files are
        located"""
        self.data = {}
        i = 0
        #
        # First load movie ratings into self.data
        #
        f = codecs.open(path + "u.data", "r", "ISO-8859-1")
        for line in f:
            i += 1
            # separate line into fields
            fields = line.split("\t")
            user = fields[0].strip('"')
            movie = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[movie] = rating
            self.data[user] = currentRatings
        f.close()
        #
        # Now load movies into self.productid2name
        # Movies contains isbn, title, and author among other fields
        #
        f = codecs.open(path + "u.item", "r", "ISO-8859-1")
        for line in f:
            i += 1
            # separate line into fields
            fields = line.split("|")
            m_id = fields[0].strip("|")
            title = fields[1].strip("|")
            # author = fields[2].strip().strip('"')
            title = title  # + ' by ' + author
            self.productid2name[m_id] = title
        f.close()
        #
        #  Now load user info into both self.userid2name and
        #  self.username2id
        #
        f = codecs.open(path + "u.user", "r", "ISO-8859-1")
        for line in f:
            i += 1
            # print(line)
            # separate line into fields
            fields = line.split("|")
            userid = fields[0].strip("|")
            age = fields[1].strip("|")
            gender = fields[2].strip("|")
            occupation = fields[3].strip("|")
            # if len(fields) > 3:
            #     age = fields[2].strip().strip('"')
            # else:
            #     age = 'NULL'
            # if age != 'NULL':
            #     value = location + '  (age: ' + age + ')'
            # else:
            #     value = location
            value = occupation + " (age: " + age + ") " + " (gender: " + gender + ")"
            self.userid2name[userid] = value
            self.username2id[age] = userid
        f.close()
        print(i)

    # Promedio puntaje de peliculas
    def calcular_promedio_peliculas(self):
        puntajes_promedio = {}
        for pelicula, puntajes in self.datos_peliculas.items():
            puntaje_promedio = sum(puntajes) / len(puntajes)
            puntajes_promedio[pelicula] = puntaje_promedio
        return puntajes_promedio

    # Distancia de Manhattan
    def manhattan(self, u1, u2):
        distancia = 0
        for pelicula in u1:
            if pelicula in u2:
                distancia += abs(u1[pelicula] - u2[pelicula])
        return distancia

    # Correlación de Pearson
    def pearson(self, u1, u2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in u1:
            if key in u2:
                n += 1
                x = u1[key]
                y = u2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(
            sum_y2 - pow(sum_y, 2) / n
        )
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    # Similitud de Coseno
    def coseno(self, u1, u2):
        puntajes_u1 = [u1.get(pelicula, 0) for pelicula in u1]
        puntajes_u2 = [
            u2.get(pelicula, 0) for pelicula in u1
        ]  # Usamos las películas de u1 para u2

        if len(puntajes_u1) == len(puntajes_u2) == 0:
            return 0.0  # Ambos usuarios no tienen puntajes

        producto_escalar = sum(
            puntajes_u1[i] * puntajes_u2[i] for i in range(len(puntajes_u1))
        )

        magnitud_u1 = np.linalg.norm(puntajes_u1)
        magnitud_u2 = np.linalg.norm(puntajes_u2)

        if magnitud_u1 * magnitud_u2 != 0:
            similitud = producto_escalar / (magnitud_u1 * magnitud_u2)
        else:
            similitud = 0.0

        return similitud

    # Función de knn
    def knn(self, usuario, distancia):
        # distancias = {}
        # for otro_usuario in self.data:
        #     if otro_usuario != usuario:
        #         dist = distancia(self.data[usuario], self.data[otro_usuario])
        #         distancias[otro_usuario] = dist

        # if distancia in (self.manhattan, self.coseno):
        #     vecinos = sorted(distancias.items(), key=lambda x: x[1])[:n]
        # else:
        #     vecinos = sorted(distancias.items(), key=lambda x: x[1], reverse=True)[:n]

        # n_vecinos = [(usuario, distancia) for usuario, distancia in vecinos]
        # return n_vecinos

        """creates a sorted list of users based on their distance to
        username"""
        distances = []
        for instance in self.data:
            if instance != usuario:
                distance = distancia(self.data[usuario], self.data[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return distances

    # Recomendación de películas
    def recomendar_peliculas(self, usuario_k, distancia, n_kk, n_items, umbral):
        # Vecinos más cercanos
        usuarios_cercanos = self.knn(usuario_k, distancia)

        # Recomienda películas no vistas con puntajes más altos
        peliculas_vistas_por_usuario_k = set(self.data.get(usuario_k, {}).keys())

        peliculas_recomendadas = []
        for usuario_vecino in usuarios_cercanos:
            for pelicula, puntaje in self.data.get(usuario_vecino[0], {}).items():
                if pelicula not in peliculas_vistas_por_usuario_k and puntaje >= umbral:
                    peliculas_recomendadas.append(
                        (usuario_vecino[0], pelicula, puntaje)
                    )

        # Ordena las películas por puntaje en orden descendente
        peliculas_recomendadas = sorted(
            peliculas_recomendadas, key=lambda x: x[2], reverse=True
        )

        # Toma las primeras 'n_items' películas
        peliculas_recomendadas = peliculas_recomendadas[:n_items]

        return peliculas_recomendadas

    def recommend(self, usuario_k, distancia, n_kk, n_items):
        """Give list of recommendations"""
        recommendations = {}
        # first get list of usuario_ks  ordered by nearness
        nearest = self.knn(usuario_k, distancia)
        #
        # now get the ratings for the user
        #
        userRatings = self.data[usuario_k]
        #
        # determine the total distance
        totalDistance = 0.0
        for i in range(n_kk):
            totalDistance += nearest[i][1]
        # now iterate through the k nearest neighbors
        # accumulating their ratings
        for i in range(n_kk):
            # compute slice of pie
            weight = nearest[i][1] / totalDistance
            # get the name of the person
            name = nearest[i][0]
            # get the ratings for this person
            neighborRatings = self.data[name]
            # get the name of the person
            # now find bands neighbor rated that usuario_k didn't
            for movie in neighborRatings:
                if not movie in userRatings:
                    if movie not in recommendations:
                        recommendations[movie] = neighborRatings[movie] * weight
                    else:
                        recommendations[movie] = (
                            recommendations[movie] + neighborRatings[movie] * weight
                        )
        # now make list from dictionary
        recommendations = list(recommendations.items())
        recommendations = [
            (self.convertProductID2name(k), v) for (k, v) in recommendations
        ]
        # finally sort and return
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        # Return the first n items
        return recommendations[:n_items]
