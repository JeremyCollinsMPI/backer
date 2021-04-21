docker build -t jeremycollinsmpi/backer .
# backer_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' backer)
# docker run -it --rm -v $PWD:/src --name backer_test -e backer_ip=$backer_ip jeremycollinsmpi/backer python bart_demo.py
# docker run -it --rm -v $PWD:/src --name backer_test jeremycollinsmpi/backer python bart_demo.py
docker run -it --rm -v $PWD:/src --name backer_test jeremycollinsmpi/backer python test.py
