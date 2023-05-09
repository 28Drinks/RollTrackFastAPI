# Backend Project for the Module

FastAPI application, React frontend, MongoDB database and hosted on DigitalOcean.

python 3.10.4

## Project Demo live at: 167.172.166.15
Hosted on DigitalOcean


# Build

## Docker
navigate into the directory of the docker compose file.
```
docker compose up --build
```
Backend running on localhost:8000
Frontend running on localhost:80

***

## without Docker
To run this project locally, create a local enviroment and use uvicorn to run the app.

1. ## Create Local Enviroment & Install Dependencies
```
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

2. ## Start Local Server
```
cd api

python main.py
```
3. ## Start Frontend
```
cd app

npm run start
```


# Danger
The env file is included with the mongoDb connection details.
(for the examiner)
