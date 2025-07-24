from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Set your OpenAI key
openai.api_key = os.getenv("
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"))

app = FastAPI()

# Allow CORS (important for frontend to access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Message):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": data.message}
            ]
        )
        reply = completion.choices[0].message["content"]
        return {"response": reply}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "Backend is running"}
