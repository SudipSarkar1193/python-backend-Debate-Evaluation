from models.pydantic_models import EvaluationResponse


response = EvaluationResponse(
    statement="Climate change is caused by human activity",
    topic="Climate change is a global crisis",
    factual_accuracy=85.0,
    relevance_score="90.0",
    explanation="Good ...",
    confidence=0.8
)
print(response.model_dump_json())
print()
print()
print()
print()



try:
    invalid = EvaluationResponse(
        statement="Climate change is caused by human activity",
        topic="Clioi",
        factual_accuracy=15.0, 
        relevance_score="900.0",
        explanation="ljk",
        confidence=0.98
    )
except Exception as e:
    print(f"Validation error: {e}")