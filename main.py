import json
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Enable CORS for website embedding
# Using regex to allow all http and https origins with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAQ data
with open("faq_data.json", "r") as f:
    faq_data = json.load(f)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# Initialize the model
# 'all-MiniLM-L6-v2' is a small, fast model suitable for this task
print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded.")

# Pre-compute embeddings for FAQ questions
question_embeddings = model.encode(questions)

class Query(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    confidence: float

@app.post("/ask", response_model=Response)
async def ask_question(query: Query):
    user_question = query.question
    
    # Encode the user's question
    user_embedding = model.encode([user_question])
    
    # Calculate cosine similarities
    # (a . b) / (|a| * |b|)
    # Since SentenceTransformer embeddings are normalized, we can just do dot product
    similarities = np.dot(question_embeddings, user_embedding.T).flatten()
    
    # Find the index of the highest similarity
    best_match_index = np.argmax(similarities)
    best_similarity = float(similarities[best_match_index])
    
    # Threshold for a valid match (adjust as needed)
    threshold = 0.5
    
    if best_similarity < threshold:
        return Response(answer="I'm sorry, I don't have an answer for that. Please contact support.", confidence=best_similarity)
    
    return Response(answer=answers[best_match_index], confidence=best_similarity)

@app.get("/")
def read_root():
    return {"message": "FAQ Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"Server failed to start: {e}")
