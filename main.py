from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

openai.api_key = os.getenv("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")  # ✅ Your key is stored securely in Render settings

app = FastAPI()

# 🌍 Allow CORS from all domains (use your frontend domain in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://huggingface.co/spaces/Dhananjay2203/ai-chatbot"],  # 🔒 Replace with your HF URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content.strip()
        return {"response": reply}
    except Exception as e:
        return {"error": str(e)}
