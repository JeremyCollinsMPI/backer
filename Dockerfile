FROM python:latest
RUN pip install requests 
RUN pip install flask
RUN pip install flask-cors
RUN pip install Werkzeug
RUN pip install pandas
WORKDIR /src