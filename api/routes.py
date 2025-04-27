from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
def home():
    return jsonify({"Message": "Welcome to Debate Analyzer"}), 200
    
