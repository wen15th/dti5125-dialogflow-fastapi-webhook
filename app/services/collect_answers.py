

# app/utils/assessment_helpers.py

def extract_answers_from_context(body, context_name="pain_assessment"):
    answers = {}
    for ctx in body["queryResult"].get("outputContexts", []):
        if context_name in ctx["name"]:
            for k, v in ctx.get("parameters", {}).items():
                if not k.endswith(".original"):
                    answers[k] = v
    return answers

def save_answers_jsonl(answers, filename="user_answers.jsonl"):
    import json
    with open(filename, "a") as f:
        f.write(json.dumps(answers) + "\n")


