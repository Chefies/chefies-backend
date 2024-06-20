# Chefies Backend
Backend of Chefies Project made with Python and FastAPI. This is being made as a requirements to complete the Bangkit capstone project.

## Development Environment Installation

### Requirements
Before installing, you need python and poetry to be installed in your computer. You can follow these guidelines:
- [Python Installation](https://www.python.org/downloads/)
- [Poetry Installation](https://python-poetry.org/docs/)

### Installing Dependencies
In the project root directory where `pyproject.toml` and `poetry.lock` is located, run:
```
poetry install
```

This command will install required dependencies for running the backend application.

### Firebase Emulators
This project requires several GCP technologies such as Cloud Storage, Cloud Firestore, and Gemini API.
For Cloud Storage and Cloud Firestore, you can use firebase emulators to run them in local. Follow this 
[firebase emulators installation guideline](https://firebase.google.com/docs/emulator-suite/install_and_configure).
For Gemini API, you need to enable [Generative Language API](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)
in your GCP project and get a service account key that is capable to use the API.

To start the emulators, run the command below.
```
firebase emulators:start
```

### Running the Backend
Before running the FastAPI backend, ensure that you have included these environment variables in the `.env` file:
- `FIRESTORE_EMULATOR_HOST`: The host of firestore emulator. Using the given `firebase.json` config, the value must be `localhost:8080`
- `STORAGE_EMULATOR_HOST`: The URL of storage emulator. Using the given `firebase.json` config, the value must be `http://localhost:9199`
- `GOOGLE_APPLICATION_CREDENTIALS` or `SERVICE_ACCOUNT_PATH` (choose one): Path of the service account key. Example: `keys/credentials.json`
- `STORAGE_BUCKET`: Storage bucket name in Cloud Storage. Example: `chefies-dev.appspot.com`

Now, you can run the backend in port 8000 using this command:
```
poetry run fastapi run cefies/app.py --port 8000
```

## Deployment
We have created a `Dockerfile` for deploying the application in Docker containers. To build the image, you can use:
```
docker build -t <image-name> .
```

After building the image, you can run it by using:
```
docker run --name <container-name> -e PRODUCTION=1 -e GOOGLE_APPLICATION_CREDENTIALS=<credentials-json-path> -d --restart always -p 9000:80 <image-name>
```

Note that the env `FIRESTORE_EMULATOR_HOST` and `STORAGE_EMULATOR_HOST` is not required as you are not using firebase emulators.

## Contributors
- C010D4KY0602 – Emir Shamsuddin Fadhlurrahman – Universitas Indonesia
- C010D4KY1156 – Rendy Arya Kemal – Universitas Indonesia