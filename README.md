# Sistema de recomendación

## Comandos

1. Levantar contenedores `docker-compose up -d --build`
2. Cargar conjunto de datos 10M100K `curl -i http://localhost:5010/api/cargar`
3. Abrir otro terminal, monitor redis `docker-compose exec redis redis-cli monitor`
4. Cargar vecino más cercano usuario 200 usando pearson `curl -i http://localhost:5010/api/knn/200/pearson`
5. Recomendar peliculas usuario 200 `curl -i http://localhost:5010/api/recommend/200/pearson/1/5`
6. Eliminar contenedores `docker-compose down`

## Web

1. Ingresar http://localhost:8080

## Backup DB

1. Descargar: https://drive.google.com/file/d/1nCymxQZtwq64KTI2wgEL4tvEkWhFP6K3/view?usp=sharing
2. Crear directorio para guardar el backup.sql `docker compose exec -it db mkdir backups`
3. Copiar backup.sql a contenedor `docker compose cp ./ruta/del/archivo/backup.sql db:/backups/backup.sql`
4. Ingresar al shell postgres `docker compose exec -it db psql -U postgres -d postgres`
5. Restaurar copia de seguridad `\i /backups/backup.sql`
6. Revisar base de datos `\c` luego `\dt`
7. Salir `exit`
