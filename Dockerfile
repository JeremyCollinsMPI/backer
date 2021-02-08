FROM python:latest
RUN pip install requests txtai
RUN pip install flask
RUN pip install flask-cors
WORKDIR /src