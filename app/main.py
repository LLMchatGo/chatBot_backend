from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, Optional
from config.config import Agent  # Adjust import as needed

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chatbot/chat")
async def chatbot_chat(request: ChatRequest):
    agent = Agent()
    # For now, read user_data from a file or use a dummy string
    try:
        with open("userdata.txt", "r") as f:
            user_data = f.read()
    except FileNotFoundError:
        user_data = ""
    result = agent.classify_query(request.message, user_data)
    return result  # This should already be a dict with the correct structure
