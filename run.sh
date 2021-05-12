docker build -t jeremycollinsmpi/backer .
docker run -it --rm -v $PWD:/src --name backer -p 8080:8080 jeremycollinsmpi/backer python api.py