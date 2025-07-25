from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("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")

app = FastAPI()

# Add CORS for Hugging Face frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://huggingface.co/spaces/Dhananjay2203/ai-chatbot"],  # Replace * with your HF app URL for security
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
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg.message}]
        )
        reply = response.choices[0].message.content.strip()
        return {"response": reply}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
