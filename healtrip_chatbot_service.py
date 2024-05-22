import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from healtrip_chatbot_rag import run_healtrip_chatbot
from healtrip_chatbot_rag import start_vector_store

class Chat(BaseModel):
    user_input: str


app = FastAPI()


@app.post("/healtrip_assistant/")
async def doctor_chatbot(chat: Chat):
    vector_db = start_vector_store("dhh_db")
    response = run_healtrip_chatbot(chat.user_input, vector_db)
    return response


if __name__ == "__main__":
    uvicorn.run("healtrip_chatbot_service:app", port=8000, workers=1)