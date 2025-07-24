from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Load your OpenAI API key
openai.api_key = os.getenv("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
")

# Define request format
class ChatRequest(BaseModel):
    message: str
    chat_history: list  # [{"user": "...", "bot": "..."}, ...]

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Prepare messages in OpenAI format
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for turn in request.chat_history:
            messages.append({"role": "user", "content": turn["user"]})
            messages.append({"role": "assistant", "content": turn["bot"]})
        messages.append({"role": "user", "content": request.message})

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4
            messages=messages,
            temperature=0.7
        )

        answer = response.choices[0].message.content
        return {"response": answer}

    except Exception as e:
        return {"response": f"Error: {str(e)}"}
