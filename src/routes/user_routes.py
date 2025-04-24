from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models import AuthMethodEnum, UserRoleEnum, User

user_bp = Blueprint("user_bp", __name__)

@user_bp.get('/getby/user_id')
def get_user_by_id():
    try:
        data = request.get_json()
        user = User.query.get(data.get("user_id"))

        if user is None:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({
            'message': 'User fetched successfully',
            'payload': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)})

@user_bp.post('/create')
def create_user():
    try:
        data = request.get_json()

        try:
            data['auth_method'] = AuthMethodEnum[data['auth_method'].upper()]
            data['role'] = UserRoleEnum[data['role'].upper()]
        except KeyError as e:
            return jsonify({"message": f"Invalid value for {str(e)}"}), 400

        new_user = User(**data)
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "payload": new_user.to_dict(include_password=False)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)})
    
@user_bp.post('/login')
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            return jsonify({'message': 'Invalid email or password'}), 401

        return jsonify({
            'message': 'Login successful',
            'payload': user.to_dict(include_password=False)
        })

    except Exception as e:
        return jsonify({'error': str(e)})