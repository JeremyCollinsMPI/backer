docker build -t jeremycollinsmpi/backer .
docker run -it --rm -v $PWD:/src --name backer -p 8000:8000 jeremycollinsmpi/backer python api.py