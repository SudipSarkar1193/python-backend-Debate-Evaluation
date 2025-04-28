from flask import Blueprint, request, jsonify
from services.model import DebateEvaluator
from services.memory import MemoryManager
from models.pydantic_models import EvaluationResponse

api_bp = Blueprint("api", __name__)
evaluator = DebateEvaluator()
memory_manager = MemoryManager(k=5)

print("memory_manager.k ", memory_manager.k)

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


    print(session_id,"  ",user_id,"  ",statement)

    if not all([session_id, user_id, statement]):
        return jsonify({"error": "session_id, user_id, and statement are required"}), 400

    try:
        # Get topic and memory
        topic = memory_manager.get_topic(session_id)
        memory = memory_manager.get_memory(session_id)

        print("topic",topic)
        print("memory",memory)

        # Evaluate statement
        evaluation = evaluator.evaluate_statement(topic, statement, user_id, memory,memory_manager.session_store,session_id)

        return jsonify({
            "evaluation": evaluation.model_dump()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500