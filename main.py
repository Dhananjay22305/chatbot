# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# ✅ HARD CODE THE API KEY (ensure no space or newline)
client = OpenAI(api_key="
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")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow everything just to test
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Backend is working"}

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



print("✅ Using API Key:", repr("sk-proj-PASTE-YOUR-REAL-KEY-HERE"))
