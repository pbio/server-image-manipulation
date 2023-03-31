# syntax=docker/dockerfile:1
FROM python:3.8
 
WORKDIR /docker
COPY requirements.txt requirements.txt
 
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]