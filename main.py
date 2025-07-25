from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# ✅ Option 1: Use environment variable (Render recommended)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Option 2 (for testing only): Hardcode key if ENV doesn't work
# client = OpenAI(api_key="sk-proj-...")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://huggingface.co/spaces/Dhananjay2203/ai-chatbot"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Backend is live"}

@app.post("/chat")
async def chat(msg: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg.message}]
        )
        return {"response": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
