from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI backend service is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    intent = body["queryResult"]["intent"]["displayName"]

    if intent == "Welcome Intent":
        reply = "Hello from FastAPI!"
    else:
        reply = "Sorry, I don't understand."

    return JSONResponse(content={"fulfillmentText": reply})