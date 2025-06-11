# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import create_access_token
# from werkzeug.security import check_password_hash
# from models import User, db
# from shared.schemas.user_schema import user_schema

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     validation = user_schema.safe_parse(data)
#     if not validation.success:
#         return jsonify({"error": "Invalid data"}), 400

#     if User.query.filter_by(username=data['username']).first():
#         return jsonify({"error": "Username already exists"}), 400

#     user = User(
#         username=data['username'],
#         role=data['role']
#     )
#     user.set_password(data['password'])
#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"message": "User created"}), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(username=data['username']).first()
    
#     if not user or not check_password_hash(user.password_hash, data['password']):
#         return jsonify({"error": "Invalid credentials"}), 401

#     access_token = create_access_token(identity=user.to_dict())
#     return jsonify(access_token=access_token), 


from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import User, db
from shared.schemas.user_schema import UserCreateSchema, UserLoginSchema
from pydantic import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/hello', methods=['GET'])
def helloWorld():
    return jsonify({"message": "Hello World"}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        validated = UserCreateSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if User.query.filter_by(username=validated.username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=validated.username,
        role=validated.role
    )
    user.set_password(validated.password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        validated = UserLoginSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    user = User.query.filter_by(username=validated.username).first()

    if not user or not check_password_hash(user.password_hash, validated.password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.to_dict())
    return jsonify(access_token=access_token), 200
