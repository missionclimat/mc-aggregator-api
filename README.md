<h1 align="center">log-parser</h1>

<div align="center">
  <strong>A <code>python drf</code> api.</strong>
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


### Run the app

Simply enter the command in the root directory :
```
docker-compose up
```

### Details about repository structure



    .
    ├── aggregator/              # The django app 
    ├── chart/                   # CD stuff run by Rancher
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

The api is deployed on an OVH instance https://www.ovh.com/manager/public-cloud/#/pci/projects/fc0a8049104a447dbf7de2eb0011c313/instances/74dd360c-df18-48cf-89d1-72c101b38535

There is no CI/CD for now, so to deploy a new version you must login to the vm and restart the app:
 1. Add your public ssh key to the instance using the OVH ui.
https://www.ovh.com/manager/public-cloud/#/pci/projects/fc0a8049104a447dbf7de2eb0011c313/ssh

2. Run those commands
```
ssh ubuntu@146.59.193.54
cd mc-aggregator-api/
git pull
sudo docker-compose -f docker-compose.prod.yml restart 
```

3. Pull the new version

It's possible to running several instance of a deployment of one provider side by side (e.g: if there is a lot of files to be parsed by the edgecast parser we can spawn a second instance of the edgecast parser)

Everything is deployed to Rancher and Enix is in charge of the CI/CD.