from pydantic import BaseModel, Field
from typing import Optional

class EvaluationResponse(BaseModel):
    statement: str = Field(..., description="The user's debate statement")
    topic: str = Field(..., description="The debate topic")
    factual_accuracy: float = Field(..., ge=0, le=100, description="Factual accuracy score (0-100%)")
    relevance_score: float = Field(..., ge=0, le=100, description="Relevance to topic score (0-100%)")
    explanation: Optional[str] = Field(None, description="Explanation of the evaluation")
    confidence: float = Field(..., ge=0, le=1, description="Model's confidence in the evaluation")