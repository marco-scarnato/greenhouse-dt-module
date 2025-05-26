Eseguire in successione:

- docker build -t greenhouse-module .

- docker save -o ./greenhouse-module.tar greenhouse-module

- docker load -i greenhouse-module.tar 

- docker run --rm greenhouse-module