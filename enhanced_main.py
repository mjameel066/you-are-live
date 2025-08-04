from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
import secrets
import logging
from logging.handlers import RotatingFileHandler

# Import models and blueprints
from models.user import db, User
from auth import auth_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database/app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@locationtracker.com')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:3000", "https://your-frontend-domain.com"])
    mail = Mail(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Create database tables
    with app.app_context():
        os.makedirs('database', exist_ok=True)
        db.create_all()
    
    # Email verification function
    def send_verification_email(email, token, user_name):
        try:
            verification_url = url_for('verify_email', token=token, _external=True)
            
            msg = Message(
                subject='Verify Your Email - Live Location Tracker',
                recipients=[email],
                html=render_template('email_verification.html', 
                                   user_name=user_name, 
                                   verification_url=verification_url),
                body=f"""
                Hi {user_name},
                
                Thank you for registering with Live Location Tracker!
                
                Please verify your email by clicking this link:
                {verification_url}
                
                This link will expire in 24 hours.
                
                If you didn't create an account, please ignore this email.
                
                Best regards,
                Live Location Tracker Team
                """
            )
            
            mail.send(msg)
            app.logger.info(f"Verification email sent to {email}")
            return True
            
        except Exception as e:
            app.logger.error(f"Failed to send verification email to {email}: {str(e)}")
            return False
    
    # Make function available to other modules
    app.send_verification_email = send_verification_email
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/verify-email/<token>')
    def verify_email(token):
        try:
            user = User.query.filter_by(verification_token=token).first()
            
            if not user:
                return render_template('verification_result.html', 
                                     success=False, 
                                     message="Invalid verification token")
            
            if user.verification_token_expires < datetime.utcnow():
                return render_template('verification_result.html', 
                                     success=False, 
                                     message="Verification token has expired")
            
            if user.email_verified:
                return render_template('verification_result.html', 
                                     success=True, 
                                     message="Email already verified")
            
            # Verify the user
            user.email_verified = True
            user.verified_at = datetime.utcnow()
            user.verification_token = None
            user.verification_token_expires = None
            
            db.session.commit()
            
            return render_template('verification_result.html', 
                                 success=True, 
                                 message="Email verified successfully! You can now log in.")
            
        except Exception as e:
            app.logger.error(f"Email verification error: {str(e)}")
            return render_template('verification_result.html', 
                                 success=False, 
                                 message="An error occurred during verification")
    
    @app.route('/api/auth/resend-verification', methods=['POST'])
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
            email_sent = send_verification_email(user.email, user.verification_token, user.first_name)
            
            if email_sent:
                return jsonify({"message": "Verification email sent successfully"}), 200
            else:
                return jsonify({"message": "Failed to send verification email"}), 500
                
        except Exception as e:
            app.logger.error(f"Resend verification error: {str(e)}")
            return jsonify({"message": "An error occurred"}), 500
    
    @app.route('/api/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500
    
    # Logging configuration
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Live Location Tracker startup')
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

