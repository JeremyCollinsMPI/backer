FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN git clone https://github.com/huggingface/transformers.git
WORKDIR transformers
RUN pip install -e .
RUN pip install requests 
RUN pip install flask
RUN pip install flask-cors
RUN pip install Werkzeug
RUN pip install pandas
WORKDIR /src