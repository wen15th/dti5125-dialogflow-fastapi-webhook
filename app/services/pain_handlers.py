from app.config.symptom_config import symptom_config
import logging
import json

logger = logging.getLogger(__name__)

def handle_clarification(body):
    # intent = body['queryResult']['intent'].get('displayName', "").lower()
    symptom = body["queryResult"]["parameters"].get("symptom", "").lower()
    logger.info(f"func: handle_clarification, symptom: {symptom}")
    return [
        symptom_config.get(symptom, {}).get("clarifier", "Could you clarify your symptom again?")
    ]

def handle_definition_and_goal(body):
    ctx_list = body["queryResult"].get("outputContexts", [])

    symptom = ""
    for ctx in ctx_list:
        if "-followup" in ctx["name"]:
            symptom = ctx["parameters"].get("symptom", "").lower()

    logger.info(f"func: handle_definition_and_goal, symptom: {symptom}")

    if symptom in symptom_config:
        definition = symptom_config[symptom]["education"]
        goal = symptom_config[symptom]["trackingPrompt"]
        return [
            definition,
            goal
        ]
    else:
        return [
            "Sorry, I lost track of the symptom. Can you tell me again?"
        ]

def handle_submit(body):
    parameters = {}
    for ctx in body["queryResult"].get("outputContexts", []):
        if "pain_assessment" in ctx["name"]:
            parameters = ctx.get("parameters", {})
    save_answers_jsonl(parameters)
    return [f"Thank you! I will now generate the caretips based on your answers."]

def save_answers_jsonl(answers, filename="user_answers.jsonl"):
    with open(filename, "a") as f:
        f.write(json.dumps(answers) + "\n")
        