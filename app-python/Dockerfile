# Dockerfile-python
FROM python:3

ENV REDIS_URL="redis://localhost:6379"

WORKDIR    /app
COPY       requirements.txt /app/
RUN        pip install -r requirements.txt

COPY *.py /app/
COPY Movie_Ratings.csv /app/
COPY ./ml-10M100K /app/ml-10M100K/
RUN chmod a+x *.py

CMD ["python", "./main.py"]
