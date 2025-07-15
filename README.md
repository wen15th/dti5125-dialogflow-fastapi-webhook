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
There are two ways to set up the development environment: using Docker or setting it up locally.
### 1️⃣ Docker

You can simply set it up using `Docker`, this is the simpler option.  
- First, install Docker from https://www.docker.com/.
- Download Docker Desktop based on your operating system.
- Once installed, run the following two commands to start the service.
  
```bash
   docker build -t dti5125-dialogflow-fastapi-webhook .
   docker run -d -p 8080:8080 dti5125-dialogflow-fastapi-webhook
```
This will start the FastAPI server at: http://localhost:8080.  
That’s it — you’re all set!

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

## API Testing
### Postman
Postman is a tool that lets you easily send requests to your APIs and inspect the responses — perfect for testing endpoints during development.  
You can download it here: https://www.postman.com/  

Here’s a sample request that Dialogflow sends to the webhook. You can copy the code below and import it into your Postman.
- To import: open Postman Desktop, click on `Import` (top left), then paste the cURL code — and you're good to go.
- You can replace https://fastapi-service-945640963381.us-central1.run.app/ with your local address, such as http://localhost:8080 or http://localhost:8000.
- You can also modify fields like `queryText`, `intent`, `outputContexts`, and `parameters` based on the specific Dialogflow request you want to simulate.
Feel free to adjust the port number based on your local setup.
```curl
curl --location 'https://fastapi-service-945640963381.us-central1.run.app/webhook' \
--header 'Content-Type: application/json' \
--data '{
  "queryResult": {
    "queryText": "yes",
    "parameters": {},
    "outputContexts": [
      {
        "name": "projects/dti-5125-chatbot-464822/agent/sessions/a3392205-3a1e-45ab-176b-08f8df34cd13/contexts/report_body_reactions_and_pain_issue-followup",
        "lifespanCount": 1,
        "parameters": {
          "symptom": "pain",
          "symptom.original": "pain"
        }
      },
      {
        "name": "projects/dti-5125-chatbot-464822/agent/sessions/a3392205-3a1e-45ab-176b-08f8df34cd13/contexts/__system_counters__",
        "parameters": {
          "no-input": 0,
          "no-match": 0
        }
      }
    ],
    "intent": {
      "name": "projects/dti-5125-chatbot-464822/agent/intents/a3d0200f-473e-455d-be09-2de3688e317f",
      "displayName": "Report_Body_Reactions_And_Pain_Issue - yes"
    }
  }
}'
```

Or you can simply import this link to access our publid Postman workspace:
[🔗 GNG5125 Chatbot Backend – Postman Collection](https://www.postman.com/wen15th/workspace/gng5125-chatbot-backend/collection/24514734-185cd47e-61ba-4362-9979-c1c27ff41039?action=share&creator=24514734&active-environment=24514734-5acff4cf-2c33-467b-8ef0-7ce32a567217)
To use it:
1. Open Postman Desktop.
2. Click on `Import` (top left).
3. Copy and paste the link, then click Continue and Import.  

The collection will be added to your workspace and you can start testing endpoints directly.  

💡 **Tips**  
You can switch environments using the dropdown menu in the top right corner. The following environments are currently configured:
- local_env: http://127.0.0.1:8000
- docker: http://127.0.0.1:8080
- ngrok: Since this is a temporary URL, you'll need to replace it with your own if you're using ngrok
- Render: https://dti5125-dialogflow-fastapi-webhook.onrender.com
- Google Cloud Run: https://fastapi-service-945640963381.us-central1.run.app  

The first three are for local development and testing, while the last two are public URLs.

## Integration Testing
### 1️⃣ Local Testing with Ngrok
Since local services (like `http://localhost:8000`) can’t be accessed from the internet, we need a tool to generate a temporary public link for them — that’s why we use `ngrok`.
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
    - The `https://ab12cd34.ngrok.io` is the temporary url generated by ngrok.
    - Add your endpoint (e.g. /webhook) to the URL, for example: https://ab12cd34.ngrok.io/webhook
    - Copy and paste it into your Dialogflow Webhook URL field, make sure to click Save after updating.

This way, your local changes can directly reflect in Dialogflow, which makes debugging and testing more intuitive.  

_**Note**_: The link generated by ngrok is different every time. So whenever you restart ngrok, you’ll need to update the webhook URL in Dialogflow with the newly generated address.

### 2️⃣ Testing via Public Deployment (Render / Google Cloud Run)
This project is currently configured to support automated deployments to two platforms for demonstration purposes and public access:
1. **_Render_** is a cloud platform that offers simple, zero‑configuration deployment for web services and APIs. In this project, deployment to Render is automatically triggered whenever commits are pushed to the `main` branch.  
   _Webhook URL_: https://dti5125-dialogflow-fastapi-webhook.onrender.com/webhook
2. **_Google Cloud Run_** is a fully managed serverless platform that automatically scales containerized applications in response to HTTP requests.  A GitHub Actions workflow is defined in `.github/workflows/deploy.yml`, which automatically deploys to Google Cloud Run on every push to the `main` branch.  
   _Webhook URL_: https://fastapi-service-945640963381.us-central1.run.app/webhook
