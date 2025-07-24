from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Allow frontend from any domain (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("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")

@app.get("/")
def read_root():
    return {"message": "OpenAI proxy backend is live 🎉"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")

    if not message:
        return JSONResponse(content={"error": "No message provided"}, status_code=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
