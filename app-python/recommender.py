import codecs
import csv

# import pandas as pd
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

    # Promedio puntaje de peliculas retorna nombre
    # def calcular_promedio_peliculas(self):
    #     puntajes_promedio = {}
    #     for movie, rating in self.datos_peliculas.items():
    #         puntaje_promedio = sum(rating) / len(rating)
    #         puntajes_promedio[movie] = puntaje_promedio
    #     puntajes_promedio = list(puntajes_promedio.items())
    #     puntajes_promedio = [(self.convertProductID2name(k), v)
    #                         for (k, v) in puntajes_promedio]
    #     # finally sort and return
    #     puntajes_promedio.sort(key=lambda artistTuple: artistTuple[1],
    #                  reverse = True)
    #     return puntajes_promedio

    # Promedio puntaje de peliculas retorna [id_movie: rating]
    def calcular_promedio_peliculas(self):
        puntajes_promedio = {}
        for pelicula, puntajes in self.datos_peliculas.items():
            puntaje_promedio = sum(puntajes) / len(puntajes)
            puntajes_promedio[pelicula] = puntaje_promedio
        return puntajes_promedio

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

    # Cargar Movie-lens 10M
    def cargarMovieLens10M(self, path=""):
        """loads the Movie Lens dataset. Path is where the u files are
        located"""
        self.data = {}
        self.userTags = {}
        datos_peliculas = {}
        i = 0
        #
        # First load movie ratings into self.data
        #
        f = codecs.open(path + "ratings.dat", "r", "utf-8")
        for line in f:
            i += 1
            # separate line into fields
            fields = line.split("::")
            user = fields[0].strip('"')
            movie = fields[1].strip('"')
            rating = float(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}

            if movie in datos_peliculas:
                datos_peliculas[movie].append(rating)
            else:
                datos_peliculas[movie] = [rating]

            currentRatings[movie] = rating
            self.data[user] = currentRatings
            self.userid2name[user] = user
            self.datos_peliculas = datos_peliculas
        f.close()
        #
        # Now load movies into self.productid2name
        # Movies contains isbn, title, and author among other fields
        #
        f = codecs.open(path + "movies.dat", "r", "utf-8")
        for line in f:
            i += 1
            # separate line into fields
            fields = line.split("::")
            m_id = fields[0].strip('"')
            title = fields[1].strip('"')
            # author = fields[2].strip().strip('"')
            title = title  # + ' by ' + author
            self.productid2name[m_id] = title
        f.close()
        #
        # Load users movie's tags into userTags
        #
        f = codecs.open(path + "tags.dat", "r", "utf-8")
        for line in f:
            i += 1
            # separate line into fields
            fields = line.split("::")
            user = fields[0].strip('"')
            movie = fields[1].strip('"')
            tag = str(fields[2].strip().strip('"'))
            if user in self.userTags:
                movieTags = self.userTags[user]
            else:
                movieTags = {}
            movieTags[movie] = tag
            self.userTags[user] = movieTags
        f.close()
        print(i)

    # Cargar Movie-lens 25M
    def cargarMovieLens25M(self, path=""):
        """loads the Movie Lens dataset. Path is where the u files are
        located"""
        self.data = {}
        self.userTags = {}
        datos_peliculas = {}
        i = 0
        #
        # First load movie ratings into self.data
        #

        with open(path + "ratings.csv", newline="", encoding="utf-8") as archivo:
            f = csv.reader(archivo)
            next(f)
            for line in f:
                i += 1
                # separate line into fields
                try:
                    user = line[0]
                    movie = line[1]
                    rating = float(line[2])
                except ValueError as e:
                    print("Error en linea", line, "error", e)

                if user in self.data:
                    currentRatings = self.data[user]
                else:
                    currentRatings = {}

                if movie in datos_peliculas:
                    datos_peliculas[movie].append(rating)
                else:
                    datos_peliculas[movie] = [rating]

                currentRatings[movie] = rating
                self.data[user] = currentRatings
                self.userid2name[user] = user
                self.datos_peliculas = datos_peliculas
            #
            # Now load movies into self.productid2name
            # Movies contains isbn, title, and author among other fields
            #
        with open(path + "movies.csv", newline="", encoding="utf-8") as archivo:
            f = csv.reader(archivo)
            next(f)
            for line in f:
                i += 1
                m_id = line[0]
                title = line[1]
                # author = fields[2].strip().strip('"')
                title = title  # + ' by ' + author
                self.productid2name[m_id] = title
        #
        # Load users movie's tags into userTags
        #
        with open(path + "tags.csv", newline="", encoding="utf-8") as archivo:
            f = csv.reader(archivo)
            next(f)
            for line in f:
                i += 1
                user = line[0]
                movie = line[1]
                tag = str(line[2])
                if user in self.userTags:
                    movieTags = self.userTags[user]
                else:
                    movieTags = {}
                movieTags[movie] = tag
                self.userTags[user] = movieTags
        print(i)

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

        if distancia == "manhattan":
            distancia = self.manhattan
        if distancia == "pearson":
            distancia = self.pearson
        if distancia == "coseno":
            distancia = self.coseno

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
