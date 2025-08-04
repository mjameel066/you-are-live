from flask import Blueprint, request, jsonify, current_app
from src.models.user import db, User
from flask_cors import CORS
import traceback
import secrets
from datetime import datetime, timedelta
import re

auth_bp = Blueprint("auth", __name__)
CORS(auth_bp)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
            
        # Extract and validate input
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        phone_number = data.get("phone_number", "").strip()

        # Validate required fields
        if not all([first_name, last_name, email, password]):
            return jsonify({"message": "Missing required fields: first_name, last_name, email, password"}), 400

        # Validate email format
        if not validate_email(email):
            return jsonify({"message": "Invalid email format"}), 400

        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({"message": message}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User with this email already exists"}), 409

        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number if phone_number else None
        )
        new_user.set_password(password)
        
        # Generate verification token
        new_user.verification_token = secrets.token_urlsafe(32)
        new_user.verification_token_expires = datetime.utcnow() + timedelta(hours=24)

        db.session.add(new_user)
        db.session.commit()
        
        # Send verification email
        try:
            from flask import current_app
            email_sent = current_app.send_verification_email(new_user.email, new_user.verification_token, new_user.first_name)
        except Exception as e:
            current_app.logger.error(f"Email sending error: {str(e)}")
            email_sent = False
        
        response_data = {
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email_verified": new_user.email_verified
            },
            "email_sent": email_sent,
            "next_step": "Please check your email and click the verification link to activate your account"
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "message": "Registration failed", 
            "error": "An unexpected error occurred. Please try again."
        }), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
            
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid email or password"}), 401
            
        if not user.email_verified:
            return jsonify({
                "message": "Please verify your email address before logging in",
                "email_verified": False,
                "can_resend": True
            }), 403
            
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "message": "Login successful", 
            "user": user.to_dict(),
            "token": "jwt_token_here"  # Implement JWT tokens if needed
        }), 200
            
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({
            "message": "Login failed", 
            "error": "An unexpected error occurred"
        }), 500

@auth_bp.route("/resend-verification", methods=["POST"])
def resend_verification():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"message": "Email is required"}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        if user.email_verified:
            return jsonify({"message": "Email already verified"}), 400
        
        # Generate new verification token
        user.verification_token = secrets.token_urlsafe(32)
        user.verification_token_expires = datetime.utcnow() + timedelta(hours=24)
        
        db.session.commit()
        
        # Send verification email
        try:
            email_sent = current_app.send_verification_email(user.email, user.verification_token, user.first_name)
        except Exception as e:
            current_app.logger.error(f"Email sending error: {str(e)}")
            email_sent = False
        
        if email_sent:
            return jsonify({"message": "Verification email sent successfully"}), 200
        else:
            return jsonify({"message": "Failed to send verification email"}), 500
            
    except Exception as e:
        current_app.logger.error(f"Resend verification error: {str(e)}")
        return jsonify({"message": "An error occurred"}), 500

