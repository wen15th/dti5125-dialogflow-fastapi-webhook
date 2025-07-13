# dti5125-dialogflow-fastapi-webhook
A backend service built with FastAPI to handle webhook fulfillment requests from a Dialogflow chatbot.


## Setup
### Enable virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```
### Install dependencies
```
pip install -r requirements.txt
```
If you add or update any packages, execute the following command to freeze the versions:
```
pip freeze > requirements.txt
```
### Run service
```
uvicorn app.main:app --reload
```
This will start the FastAPI server at: http://localhost:8000.

You can open the interactive API docs at: http://localhost:8000/docs
