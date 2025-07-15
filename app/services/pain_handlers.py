from app.config.symptom_config import symptom_config
import logging

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
    # Now parameters contains everything the user provided in the flow!
    # e.g., parameters.get("pain_type"), parameters.get("pain_location"), etc.
    return [f"Thank you! Here’s what we collected: {json.dumps(parameters)}"]