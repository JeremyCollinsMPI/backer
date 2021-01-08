FROM python:latest
RUN pip install requests txtai
RUN pip install flask
WORKDIR /src