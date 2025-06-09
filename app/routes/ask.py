from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.core.embedder import embed_texts
from app.core.pinecone_client import index
import openai
from typing import List

router = APIRouter()

class AskRequest(BaseModel):
    user_id: str
    question: str
    top_k: int = 3

class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse)
async def ask_question(req: AskRequest):
    query_vec = embed_texts([req.question])[0]
    results = index.query(
        vector=query_vec,
        top_k=req.top_k,
        include_metadata=True,
        filter={"user_id": {"$eq": req.user_id}},
    )
    matches = results["matches"]
    top_chunks = [m["metadata"]["chunk"] for m in matches if "metadata" in m and "chunk" in m["metadata"]]
    if not top_chunks:
        raise HTTPException(status_code=404, detail="No relevant document chunks found for this user. Upload a PDF first.")
    prompt = (
        "You are a helpful assistant. Use the following report excerpts to answer the question.\n"
        "If the question is not about health and fitness, just say you are not used for such purposes."
        f"Context:\n{chr(10).join(top_chunks)}\n\nQuestion: {req.question}\nAnswer:"
    )
    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
)
    answer = response.choices[0].message.content.strip()

    return AskResponse(answer=answer, relevant_chunks=top_chunks)
