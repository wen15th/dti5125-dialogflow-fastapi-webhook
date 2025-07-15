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

    output_contexts = []

    if intent == "Report_Body_Reactions_And_Pain_Issue - yes":
        consent_text = "To help me provide the best care tips, would you be okay to answer a few more questions?"
        text = (text + "\n\n" + consent_text).strip()
        message_list.append({
            "text": {
                "text": [consent_text]
            }
        })

        # Set output context for awaiting_consent
        session_path = body.get("session") or body.get("sessionInfo", {}).get("session")
        if not session_path:
            logger.error("No session path found in webhook request!")
            session_path = "projects/YOUR_PROJECT_ID/agent/sessions/placeholder"

        output_contexts = [{
            "name": f"{session_path}/contexts/awaiting_consent",
            "lifespanCount": 1
        }]


    response = {
        "fulfillmentText": text,
        "fulfillmentMessages": message_list,
    }
    if output_contexts:
        response["outputContexts"] = output_contexts

    return JSONResponse(content=response)
