from models.pydantic_models import EvaluationResponse

class DebateEvaluator:
    def __init__(self):
        pass

    def evaluate_statement(self, topic: str, statement: str, user_id: int, memory) -> EvaluationResponse:
        return {"Msg":"Evaluator not implemented yet"}