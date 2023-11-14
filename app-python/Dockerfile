# Dockerfile-python
FROM python:3

WORKDIR    /app
COPY       requirements.txt /app/
RUN        pip install -r requirements.txt

COPY *.py /app/
COPY Movie_Ratings.csv /app/
RUN chmod a+x *.py

CMD ["python", "./main.py"]
