
# Microservices Architecture with Docker  🐳 🐳 🐳

![](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExemg0ZGIwOGRkdXRvcnFqbG40ZnFmbDV0emdva2d0dTd1Zjd3MGo2NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FBeSx3itXlUQw/giphy.gif)

HELLLO THERE !!!

## Project Overview

This project implements a microservices architecture utilizing Docker and Docker Compose. It aims to deepen understanding of containerization concepts while creating a robust application ecosystem. The architecture includes multiple services, each encapsulated within its own Docker container, facilitating independent deployment and scaling.

### Objectives

- Understand key container concepts and tools.
- Create a microservices architecture with Docker.
- Gain practical experience with Dockerfile, Docker images, Docker networks, Docker volumes, and Docker Compose.

## Architecture Diagram

![Architecture Diagram](/assets/play-with-containers-py.png)

## 🛠️ Project Structure

Here's a breakdown of the project structure:

```
.
├── README.md
├── config.yaml
├── .env
├── scripts
│   └── [...]
├── srcs
│   ├── api-gateway
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   └── ...             
│   │   ├── requirements.txt
│   │   └── server.js
|   |   |── DOCKERFILE
|   |   
│   ├── billing-app
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   └── ...             
│   │   ├── requirements.txt
│   │   └── server.js
|   |   |── DOCKERFILE
│   └── inventory-app
│       ├── app
│       │   ├── __init__.py
│       │   └── ...             
│       ├── requirements.txt
|       |── DOCKERFILE
│       └── server.py
└── Vagrantfile
|__ docker-compose.yaml
```

## Services

The architecture comprises the following services:

1. **inventory-db**: A SQL database server for inventory data, accessible via port 5432.
2. **billing-db**: A SQL database server for billing data, accessible via port 5432.
3. **inventory-app**: A server for the inventory application, connected to the inventory database, accessible via port 8080.
4. **billing-app**: A server for the billing application, connected to the billing database and consuming messages from RabbitMQ, accessible via port 8080.
5. **rabbit-queue**: A RabbitMQ server for message queuing.
6. **api-gateway-app**: An API gateway that forwards requests to other services, accessible via port 3000.

## Prerequisites

- Vagrant
- VirtualBox
- Docker
- Docker Compose

## Setup

### Clone the Repository

```bash
git clone https://learn.zone01dakar.sn/git/djibsow/play-with-containers.git
cd play-with-containers
```

### Start Vagrant

Run the following command to start your Vagrant environment:

```bash
vagrant up
```

This will provision your VM and install Docker.

### Connect to the VM

You mush connect to the VM with the following command:
```bash
vagrant ssh 
```

### Build and Run the Docker Containers

Navigate to the directory containing your `docker-compose.yml` file and execute:

```bash
cd opt/ &&
docker-compose up --build
```

This command will build the Docker images and start the containers as defined in your `docker-compose.yml`.

### Access the Services

**API Gateway**: Access your API Gateway at `http://{GATEWAY_IP}:3000/api/...`.


### Restarting Containers on Failure

All containers are configured to restart on failure. This is managed within the `docker-compose.yml` file by specifying the `restart` policy.


## Documentation

All relevant documentation and instructions can be found within this `README.md`. For detailed information on Docker and its components, refer to the [official Docker documentation](https://docs.docker.com/).


## Conclusion

This project serves as a practical introduction to containerization and microservices. By following this guide, you should be able to set up your environment and run the services effectively.

---

### Acknowledgements

Special thanks to the community resources and official documentation that made this project possible.
