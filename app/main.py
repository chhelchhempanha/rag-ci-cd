from fastapi import FastAPI
from app.controllers.ai_controller import router as ai_router

app = FastAPI(
    title="Bitcoin RAG API",
    description="Bitcoin prediction and RAG-based Q&A system",
    version="1.0.0"
)

app.include_router(ai_router)


@app.get("/")
async def root():
    return {
        "message": "Bitcoin RAG API is running",
        "endpoints": {
            "upload_pdf": "/files/upload",
            "bitcoin_prediction": "/ai/bitcoin",
            "load_pdf": "/ai/load-pdf",
            "setup_rag": "/ai/setup-rag",
            "ask_question": "/ai/ask"
        }
    }
