FROM python:3.8-slim-buster

WORKDIR /app

COPY src /app/src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app/src

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
