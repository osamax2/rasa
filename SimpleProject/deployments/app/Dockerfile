FROM python:3.6
RUN apt-get upgrade -y
RUN apt-get update
RUN pip install --upgrade pip
ADD app/ /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python app.py
