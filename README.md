# dti5125-dialogflow-fastapi-webhook
A backend service built with FastAPI to handle webhook fulfillment requests from a Dialogflow chatbot.


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

## Test
### In local environment
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