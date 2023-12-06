# Dockerfile-python
FROM python:3

ENV REDIS_URL="redis://localhost:6379"

WORKDIR    /app
COPY       requirements.txt /app/
RUN        pip install -r requirements.txt

COPY *.py /app/
COPY Movie_Ratings.csv /app/

# Descargar archivo ZIP
# RUN wget -O ml-10m.zip https://files.grouplens.org/datasets/movielens/ml-10m.zip
RUN wget -O ml-25m.zip https://files.grouplens.org/datasets/movielens/ml-25m.zip

# Descomprimir archivo ZIP
RUN apt-get update && apt-get install -y unzip
# RUN unzip ml-10m.zip -d /app/
RUN unzip ml-25m.zip -d /app/
RUN rm ml-25m.zip
RUN rm /app/ml-25m/genome-scores.csv

RUN chmod a+x *.py

CMD ["python", "./main.py"]
