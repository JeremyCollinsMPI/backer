FROM python:latest
RUN pip install requests txtai
WORKDIR /src