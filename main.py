from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import answer_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QARequest(BaseModel):
    video_url: str
    question: str

class QAResponse(BaseModel):
    answer: str

@app.post('/ask', response_model=QAResponse)
def ask(payload: QARequest):
    answer = answer_question('api-key-here', payload.video_url, payload.question)
    return {'answer': answer}
