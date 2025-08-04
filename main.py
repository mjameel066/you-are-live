import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request, render_template_string
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import secrets
import logging
from logging.handlers import RotatingFileHandler

from src.models.user import db, User
from src.routes.user import user_bp
from src.routes.auth import auth_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'location-tracker-secret-key-change-in-production')

# CORS configuration
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "*"])

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@locationtracker.com')

# Initialize Mail
mail = Mail(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Email verification function
def send_verification_email(email, token, user_name):
    try:
        verification_url = f"{request.host_url}verify-email/{token}"
        
        email_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Verify Your Email - Live Location Tracker</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #2563eb; color: white; padding: 20px; text-align: center; }
                .content { padding: 30px 20px; background: #f9fafb; }
                .button { display: inline-block; padding: 12px 30px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .footer { padding: 20px; text-align: center; color: #666; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛡️ Live Location Tracker</h1>
                </div>
                <div class="content">
                    <h2>Welcome, {{ user_name }}!</h2>
                    <p>Thank you for registering with Live Location Tracker. To complete your registration and start using our family safety features, please verify your email address.</p>
                    
                    <p style="text-align: center;">
                        <a href="{{ verification_url }}" class="button">Verify Email Address</a>
                    </p>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; background: #e5e7eb; padding: 10px; border-radius: 5px;">{{ verification_url }}</p>
                    
                    <p><strong>This link will expire in 24 hours.</strong></p>
                    
                    <p>If you didn't create an account with us, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Live Location Tracker. All rights reserved.</p>
                    <p>Keep your family safe with real-time location tracking.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject='Verify Your Email - Live Location Tracker',
            recipients=[email],
            html=render_template_string(email_template, user_name=user_name, verification_url=verification_url),
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

@app.route('/verify-email/<token>')
def verify_email(token):
    try:
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            return """
            <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #dc2626;">❌ Invalid Verification Token</h2>
            <p>The verification link is invalid or has been used already.</p>
            <a href="/" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to App</a>
            </body></html>
            """
        
        if user.verification_token_expires and user.verification_token_expires < datetime.utcnow():
            return """
            <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #dc2626;">⏰ Token Expired</h2>
            <p>The verification link has expired. Please request a new verification email.</p>
            <a href="/" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to App</a>
            </body></html>
            """
        
        if user.email_verified:
            return """
            <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #16a34a;">✅ Already Verified</h2>
            <p>Your email has already been verified. You can now log in to your account.</p>
            <a href="/" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to App</a>
            </body></html>
            """
        
        # Verify the user
        user.email_verified = True
        user.verified_at = datetime.utcnow()
        user.verification_token = None
        user.verification_token_expires = None
        
        db.session.commit()
        
        return """
        <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h2 style="color: #16a34a;">🎉 Email Verified Successfully!</h2>
        <p>Your email has been verified. You can now log in to your Live Location Tracker account.</p>
        <a href="/" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to App</a>
        </body></html>
        """
        
    except Exception as e:
        app.logger.error(f"Email verification error: {str(e)}")
        return """
        <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h2 style="color: #dc2626;">❌ Verification Error</h2>
        <p>An error occurred during verification. Please try again or contact support.</p>
        <a href="/" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to App</a>
        </body></html>
        """

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "Live Location Tracker API"
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
