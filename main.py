from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your Hugging Face frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API Key from Render environment variables
openai.api_key = os.getenv("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")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chatbot(req: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": req.message}],
        )
        reply = response.choices[0].message.content
        return {"response": reply}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
