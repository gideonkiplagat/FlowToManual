# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import SessionRecording, db
# from shared.schemas.session_schema import SessionSchema
# import json

# session_bp = Blueprint('sessions', __name__)

# @session_bp.route('/sessions', methods=['POST'])
# @jwt_required()
# def save_session():
#     data = request.get_json()
#     validation = session_schema.safe_parse(data)
#     if not validation.success:
#         return jsonify({"error": "Invalid data"}), 400

#     current_user = get_jwt_identity()
    
#     try:
#         session = SessionRecording(
#             user_id=current_user['id'],
#             name=data.get('name', 'Unnamed Session'),
#             events=json.dumps(data['events']).encode('utf-8')
#         )
#         db.session.add(session)
#         db.session.commit()
#         return jsonify({"message": "Session saved", "id": session.id}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @session_bp.route('/sessions/<int:session_id>', methods=['GET'])
# @jwt_required()
# def get_session(session_id):
#     session = SessionRecording.query.get_or_404(session_id)
#     return jsonify({
#         "id": session.id,
#         "name": session.name,
#         "events": json.loads(session.events.decode('utf-8'))
#     })


from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import SessionRecording, db
from shared.schemas.session_schema import SessionSchema
import json

session_bp = Blueprint('sessions', __name__)

@session_bp.route('/sessions', methods=['POST'])
@jwt_required()
def save_session():
    try:
        # Validate request data using Pydantic
        data = request.get_json()
        session_data = SessionSchema(**data)
    except Exception as e:
        return jsonify({"error": f"Invalid data: {str(e)}"}), 400

    current_user = get_jwt_identity()

    try:
        session = SessionRecording(
            user_id=current_user['id'],
            name=session_data.name or 'Unnamed Session',
            events=json.dumps(session_data.events).encode('utf-8')
        )
        db.session.add(session)
        db.session.commit()
        return jsonify({"message": "Session saved", "id": session.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@session_bp.route('/sessions/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    session = SessionRecording.query.get_or_404(session_id)
    return jsonify({
        "id": session.id,
        "name": session.name,
        "events": json.loads(session.events.decode('utf-8'))
    })
