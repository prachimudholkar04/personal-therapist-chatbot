from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

client = InferenceClient("tiiuae/falcon-7b-instruct", token=HF_TOKEN)

class ChatRequest(BaseModel):
    message: str
    tone: str  # Add tone input

@app.post("/chat")
async def chat_with_bot(req: ChatRequest):
    try:
        # Build a focused, single-turn response prompt
        prompt = f"""You are a therapist with a {req.tone} personality. 
Respond in 1–3 compassionate sentences. Do not continue the conversation. 
Only reply to the message below, and do not repeat the user's text.

User says: "{req.message}"

Therapist:"""

        response = client.text_generation(
            prompt=prompt,
            max_new_tokens=200,
            temperature=0.7,
            stop_sequences=["User:", "Message from user:", "\nUser", "\n\nUser"]
        )

        return {"response": response.strip()}

    except Exception as e:
        return {"response": f"⚠️ Internal error: {str(e)}"}
