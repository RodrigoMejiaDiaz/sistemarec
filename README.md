# Sistema de recomendación

## Comandos

1. Levantar contenedores `docker-compose up -d --build`
2. Cargar conjunto de datos 10M100K `curl -i http://localhost:5010/api/cargar`
3. Abrir otro terminal, monitor redis `docker-compose exec redis redis-cli monitor`
4. Cargar vecino más cercano usuario 200 usando pearson `curl -i http://localhost:5010/api/knn/200/pearson`
5. Recomendar peliculas usuario 200 `curl -i http://localhost:5010/api/recommend/200/pearson/1/5`
6. Eliminar contenedores `docker-compose down -v`

## Web

1. Ingresar `www://localhost:8080`
