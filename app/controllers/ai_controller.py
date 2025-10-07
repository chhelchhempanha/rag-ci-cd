from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI"])
ai_service = AIService()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask/stream")
async def ask_question_stream(request: QuestionRequest):
    """Stream AI answer token-by-token"""
    try:
        # Ensure Bitcoin data is available
        if not ai_service.bitcoin_data:
            ai_service.fetch_bitcoin_data()

        bitcoin_context = f"""Current Date: {ai_service.bitcoin_data['current_date']}

Bitcoin Market Analysis:
- Current Price (as of {ai_service.bitcoin_data['current_date']}): ${ai_service.bitcoin_data['current_price']:,.2f}
- 7-Day Prediction (by {ai_service.bitcoin_data['prediction_date']}): ${ai_service.bitcoin_data['predicted_price']:,.2f}
- Expected Change: {ai_service.bitcoin_data['price_change']:+.2f}%
- Trend: {ai_service.bitcoin_data['trend']}
"""

        template = """Answer the question based on the following Bitcoin market data:

""" + bitcoin_context + """

Question: {question}

Answer:"""

        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | ai_service.model | StrOutputParser()

        # Create generator for streaming output
        def generate():
            try:
                for chunk in chain.stream({"question": request.question}):
                    yield chunk
            except Exception as e:
                yield f"\n[Error]: {str(e)}"

        # Return as streaming text/plain response
        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
