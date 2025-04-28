from flask import Blueprint, request, jsonify
from services.model import DebateEvaluator
from services.memory import MemoryManager
from models.pydantic_models import EvaluationResponse

api_bp = Blueprint("api", __name__)
evaluator = DebateEvaluator()
memory_manager = MemoryManager(k=5)


@api_bp.route("/", methods=["GET"])
def home():
    return jsonify({"Message": "Welcome to Debate Analyzer"}), 200

@api_bp.route("/start_session", methods=["POST"])
def start_session():
    try:
        data = request.get_json()
        topic = data.get("topic")
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
    
        session_id = memory_manager.create_session(topic)
        return jsonify({"session_id": session_id}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create session: {str(e)}"}), 500


@api_bp.route("/evaluate", methods=["POST"])
def evaluate_statement():
    data = request.get_json()
    session_id = data.get("session_id")
    user_id = data.get("user_id")
    statement = data.get("statement")
    in_favour = data.get("in_favour")

    print(session_id,"  ",user_id,"  ",statement)

    if not all([session_id, user_id, statement, in_favour is not None]):
        return jsonify({"error": "session_id, user_id, statement, and in_favour are required"}), 400

    try:
        # Converting boolean to string for the prompt
        in_favour_string = "in favor" if in_favour else "against"

        # Get topic and memory
        topic = memory_manager.get_topic(session_id)
        memory = memory_manager.get_memory(session_id)

        # Evaluate statement
        evaluation = evaluator.evaluate_statement(topic, statement, user_id, memory, in_favour_string)

        # Get conversation history
        history = [
            {"type": msg.__class__.__name__, "content": msg.content}
            for msg in memory.load_memory_variables({})["history"]
        ]

        return jsonify({
            "evaluation": evaluation.model_dump(),
            "history": history
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500