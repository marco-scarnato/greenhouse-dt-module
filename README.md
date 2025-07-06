To test the execution:

- docker build -t greenhouse-module .

- docker save -o ./greenhouse-module.tar greenhouse-module

- docker load -i greenhouse-module.tar 

- docker run --rm -e PYTHONUNBUFFERED=1 greenhouse-module
