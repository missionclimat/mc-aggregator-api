<h1 align="center">aggregator-api</h1>

<div align="center">
  <strong>A <code>python drf</code> API</strong>
</div>

<br/>

<div align="center">
  <sub>Built with ❤︎ by
  <a href="https://mission-climat.io/">Mission-Climat</a>
</div>




## Contributors

- Hugo Rochefort


### Requirements

_What you need before running the app_

1. Install **Docker Comunity edition**

  Go to the website https://docs.docker.com/get-docker/ and install the version of your OS

2. If the version of Docker doesn't come with **docker-compose** make sure to install it

  Go to the website https://docs.docker.com/compose/install/ and install the version of your OS

3. (Optional) Add docker to a sudo group 

   Follow the instruction on the website https://docs.docker.com/engine/install/linux-postinstall/

4. Ask an admin for the Secrets files

### Run the app

Simply enter the command in the root directory :
```
docker-compose up
```

Then you can access several webapp:
- Django admin interface: http://0.0.0.0:8000/admin/
- Django Rest Framework browsable API: http://0.0.0.0:8000/ 
- Redoc ui (api documentation): http://0.0.0.0:8000/redoc/
- Swagger ui (api documentation): http://0.0.0.0:8000/swagger/

### Run the tests

TODO


### Details about repository structure

    .
    ├── .github/                 # Continuous Deployment 
    ├── aggregator/              # The django app 
    ├── configurations/          # Configurations files
    ├── etc/                     # Scripts and requirements
    ├── secrets/                 # Sensible data (tokens, password etc)
    ├── .dockerignore
    ├── .gitignore
    ├── docker-compose.yml       # docker-compose file use for development environment 
    ├── docker-compose.prod.yml  # docker-compose file use for production environment
    ├── Dockerfile               # Dockerfile which generate the django image 
    ├── Dockerfile.nginx         # Dockerfile which generate the nginx image
    └── README.md

### Deployment

The api is redeployed each push to master on an OVH instance.

You can see the `.github/workflows/main.yml` file and the https://github.com/missionclimat/mc-aggregator-api/actions page for more information. 

