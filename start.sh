#!/bin/bash

app="next08"
docker build -t ${app} .
docker run -d -p 3331:80 \
  --name=${app} \
  -v $PWD:/app ${app}


# docker run -d --name ${app} \
#   -p 80:80 -v $(pwd)/app:/app \
#   -e FLASK_APP=main.py \
#   -e FLASK_DEBUG=1 \
#   myimage flask run \
#   --host=0.0.0.0 \
#   --port=80


