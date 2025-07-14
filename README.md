# dti5125-dialogflow-fastapi-webhook
A backend service built with FastAPI to handle webhook fulfillment requests from a Dialogflow chatbot.  

🗂 Project Directory Structure:
```
dti5125-dialogflow-fastapi-webhook/
├── app/
│   ├── main.py                 # webhook entry point
├── services/
│   ├── pain_handlers.py        # handle logic of pain intent & symptoms
│   ├── fallback_handlers.py    # handle logic of fallback
│   ├── rag/                    # RAG-related logic
│   │   ├── store.py            # webpage crawling and text preprocessing
│   │   ├── vectorstore.py      # vector store construction and loading
│   │   ├── prompt.py           # custom prompt templates
│   │   └── chain.py            # Langchain chain construction
├── data/                       
│   ├── chroma/                 # persisted Chroma vectorstore files
│   │   ├── ...  
└── requirements.txt            # project dependencies
```

## Setup
### 1️⃣ Docker
You can simply set it up using `Docker`:
```bash
   docker build -t dti5125-dialogflow-fastapi-webhook .
   docker run -d -p 8080:8080 dti5125-dialogflow-fastapi-webhook
```
This will start the FastAPI server at: http://localhost:8080  

To stop Docker, run:
```bash
  # Check the running containers and find the container ID
  docker ps
  # Stop the container using its ID
  docker stop <container_id>
```

### 2️⃣ Local env
#### Enable virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```
#### Install dependencies
```
pip install -r requirements.txt
```
If you add or update any packages, execute the following command to freeze the versions:
```
pip freeze > requirements.txt
```
#### Run service
```
uvicorn app.main:app --reload
```
This will start the FastAPI server at: http://localhost:8000.

You can open the interactive API docs at: http://localhost:8000/docs

## Integration Testing
### 1️⃣ Local Testing with Ngrok
1. Install `ngrok`, download from: https://ngrok.com/download
2. Connect your account:
    ```
    ngrok config add-authtoken <your ngrok token>
    ```
   You can find your auth token here: https://dashboard.ngrok.com/get-started/setup

3. Start `ngrok`:  
   Run the following command to expose your local FastAPI service:  
    ```
    ngrok http 8000
    ```
   _**Note**_: If you're using Docker, make sure to change the port number to 8080, or another port that suits your setup.  
    If successful, you'll see something like:
    ```
    Forwarding  https://ab12cd34.ngrok.io -> http://localhost:8000
    ```
    Add your endpoint to the URL, for example: https://ab12cd34.ngrok.io/webhook  
   Copy and paste it into your Dialogflow Webhook URL field, make sure to click Save after updating.

### 2️⃣ Testing via Public Deployment (Render / Google Cloud Run)
This project is currently configured to support automated deployments to two platforms for demonstration purposes and public access:
1. **_Render_** is a cloud platform that offers simple, zero‑configuration deployment for web services and APIs. In this project, deployment to Render is automatically triggered whenever commits are pushed to the `main` branch.  
   _Webhook URL_: https://dti5125-dialogflow-fastapi-webhook.onrender.com/webhook
2. **_Google Cloud Run_** is a fully managed serverless platform that automatically scales containerized applications in response to HTTP requests.  A GitHub Actions workflow is defined in `.github/workflows/deploy.yml`, which automatically deploys to Google Cloud Run on every push to the `main` branch.  
   _Webhook URL_: https://fastapi-service-945640963381.us-central1.run.app/webhook