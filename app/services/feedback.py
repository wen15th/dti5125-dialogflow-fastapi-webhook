import logging
import json

logger = logging.getLogger(__name__)

def handle_feedback_response(body):
    feedback_text = body["queryResult"]["queryText"]
    session_id = body.get("session", "").split("/")[-1]

    logger.info(f"[Feedback] Received: '{feedback_text}' from session: {session_id}")

    # Optionally save to file or DB
    with open("feedback_log.jsonl", "a") as f:
        f.write(json.dumps({
            "session": session_id,
            "feedback": feedback_text
        }) + "\n")

    return ["Thank you for your feedback!"]
