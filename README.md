# Sistema de recomendación

## Modo Producción

Para desplegar la aplicación en un entorno de producción

1. `docker compose -f docker-compose.prod.yml up -d --build`

## Backup DB

1. Descargar: https://drive.google.com/file/d/1nCymxQZtwq64KTI2wgEL4tvEkWhFP6K3/view?usp=sharing
2. Crear directorio para guardar el backup.sql `docker compose exec -it db mkdir backups`
3. Copiar backup.sql a contenedor `docker compose cp ./ruta/del/archivo/backup.sql db:/backups/backup.sql`
4. Ingresar al shell postgres `docker compose exec -it db psql -U postgres -d postgres`
5. Restaurar copia de seguridad `\i /backups/backup.sql`
6. Revisar base de datos `\c` luego `\dt`
7. Salir `exit`

## Modo Desarrollo

En un entorno de desarrollo se tiene que levantar y ejecutar las aplicaciones de NODE y REACT localmente.

# SERVIDOR EXPRESS

1. `cd app-node`
2. `npm install`
3. `npm run dev`

# APLICACION REACT

1. `cd frontend`
2. `npm install`
3. `npm start`

1. Levantar contenedores `docker compose -f docker-compose.yml up -d --build`

Se puede usar POSTMAN para hacer los llamados a las siguientes direcciones:

2. Cargar conjunto de datos 25M `curl -i http://localhost:5010/api/cargar`
3. Cargar vecino más cercano usuario 200 usando pearson `curl -i http://localhost:5010/api/knn/200/pearson`
4. Recomendar peliculas usuario 200 `curl -i http://localhost:5010/api/recommend/200/pearson/1/5`
5. Eliminar contenedores `docker-compose down`

## Web

1. Ingresar http://localhost:8080
2. En el primer cuadro ingresar el ID del usuario
3. Segundo recuadro ingresar distancia a utilizar "pearson", "manhattan", "coseno"

## Desplegar con Docker Swarm

1. Primer nodo MANAGER `docker swarm init --advertise-addr <ip>`

2. Copiar el comando mostrado a los nodos worker para que se unan al swarm

3. En el primer nodo manager `git clone https://github.com/RodrigoMejiaDiaz/sistemarec.git`

4. `cd sistemarec`

5. `docker stack deploy --compose-file docker-compose.yml stackrec`

6. Esperar a que se replique en los nodos worker

7. Escalar los servicios `docker service scale stackrec_app-python=2 stackrec_app-dotnet=2` 
