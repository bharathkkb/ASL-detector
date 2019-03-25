# ASL-detector

ASL detector is a web application that uses machine learning to predict ASL sign language

### Prerequisites

Install docker and set memory allocation to 8gb.

```
docker
docker-compose
```

## Installing

#### Running the backend API server

Clone this repo

```
docker-compose -f compose-asl-api up --d
```

This will build the system and run the server
The endpoint will be http://localhost:5000/test/api

To stop the API server

```
docker-compose -f compose-asl-api down
```
