# ASL-detector

ASL detector is a web application that uses machine learning to predict ASL sign language

### Prerequisites

Install docker and set memory allocation to 8gb.

```
docker
docker-compose
```

#### Running the backend API server

Incase you do not have the model, you can run getModel.sh to download the model.
This will download the model to /asl-api

## Installing

#### Running the backend API server

Clone this repo

```
docker-compose -f compose-dev-package.yml up --d
```

This will build the system and run the server
The endpoint will be http://localhost:5000/test/api

To stop the API server

```
docker-compose -f compose-dev-package.yml down
```
