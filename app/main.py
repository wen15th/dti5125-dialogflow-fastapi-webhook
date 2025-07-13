from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.services.pain_handlers import handle_clarification, handle_definition_and_goal
from app.services.fallback_handlers import handle_fallback
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI backend service is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    logger.info("Request body: %s", json.dumps(body, ensure_ascii=False))

    intent = body["queryResult"]["intent"]["displayName"]

    # Intent Map
    handlers = {
        # "Default Welcome Intent": handle_welcome,
        # "Report_Movement_Issue": handle_report_movement,
        # "confirm_yes_movement": handle_symptom_education,
        "Report_Body_Reactions_And_Pain_Issue": handle_clarification,
        "Report_Body_Reactions_And_Pain_Issue - yes": handle_definition_and_goal,
        # "Report_Sensory_Issue": handle_clarification,
        # "Report_Sensory_Issue - yes": handle_definition_and_goal
        "Default Fallback Intent": handle_fallback
    }

    try:
        handler = handlers.get(intent, handle_fallback)
        messages = handler(body)
    except Exception as e:
        logger.exception("Error occurred while handling request body: %s",str(e))
        messages = [f"Sorry, an error occurred, please try later."]

    text = ""
    message_list = []
    for message in messages:
        message_list.append({
            "text": {
                "text": [message]
            }
        })
        text = (text + "\n\n" + message).strip()

    return JSONResponse(content={
        "fulfillmentText": text,
        "fulfillmentMessages": message_list
    })