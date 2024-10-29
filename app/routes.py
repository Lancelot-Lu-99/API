from flask import Blueprint, request, jsonify, session
from .models import db, User
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

main = Blueprint('main', __name__)

@main.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = hash_password(data.get('password'))
    
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    new_user = User(username=username, email=email, password=password, stars=0)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@main.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and verify_password(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@main.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "Logout successful"}), 200

@main.route('/api/delete_account', methods=['DELETE'])
@jwt_required()
def delete_account():
    
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "Account deleted successfully"}), 200

@main.route('/api/change_password', methods=['POST'])
@jwt_required()
def change_password():

    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({"error": "Both old and new passwords are required"}), 400
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not verify_password(user.password, old_password):
        return jsonify({"error": "Old password is incorrect"}), 403

    user.password = hash_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password changed successfully"}), 200


@main.route('/api/load_stars', methods=['GET'])
@jwt_required()
def load_stars():
    user_id = get_jwt_identity()  
    print(f"User ID: {user_id}")  # Debugging
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"stars": 0}), 200
    
    print(f"Stars: {user.stars}")  # Debugging
    return jsonify({"stars": user.stars}), 200

@main.route('/api/save_stars', methods=['POST'])
@jwt_required()
def save_stars():
    user_id = get_jwt_identity() 
    data = request.get_json() 
    new_stars = data.get('stars', 0)  

    if new_stars == 0:
        return jsonify({"message": "No stars to add"}), 400

    
    user = User.query.get(user_id)

    if user:
        user.stars += new_stars
        db.session.commit()
        return jsonify({"message": f"{new_stars} stars added successfully!"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@main.route('/api/get_user_data', methods=['GET'])
@jwt_required()
def get_user_data():
    user_id = get_jwt_identity() 

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "stars": user.stars
    }), 200


# Function to hash passwords
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Function to verify passwords
def verify_password(stored_password, provided_password):
    return pbkdf2_sha256.verify(provided_password, stored_password)