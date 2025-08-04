# Live Location Tracker

A secure family safety application with real-time location tracking, email verification, and user management.

## Features

- ✅ User Registration with Email Verification
- ✅ Secure Login System
- ✅ Password Strength Validation
- ✅ Responsive React Frontend
- ✅ Flask REST API Backend
- ✅ SQLite Database
- ✅ Email Notifications
- ✅ Modern UI with Tailwind CSS
- ✅ Mobile-Responsive Design

## Tech Stack

**Frontend:**
- React 18
- Tailwind CSS
- Lucide Icons
- Vite Build System

**Backend:**
- Flask (Python)
- SQLAlchemy ORM
- Flask-Mail for Email
- Flask-CORS for Cross-Origin Requests
- Werkzeug for Password Security

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd location-tracker-backend
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your email credentials
   ```

4. **Run the application**
   ```bash
   python src/main.py
   ```

5. **Access the application**
   - Open http://localhost:5000 in your browser

### Railway Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [Railway.app](https://railway.app)
   - Connect your GitHub repository
   - Add environment variables:
     - `SECRET_KEY`: Your secret key
     - `MAIL_USERNAME`: Your email address
     - `MAIL_PASSWORD`: Your app password
     - `MAIL_DEFAULT_SENDER`: Your sender email

3. **Configure Email (Gmail)**
   - Enable 2-Factor Authentication
   - Generate App Password
   - Use App Password in `MAIL_PASSWORD`

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `MAIL_USERNAME` | Email username | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Email app password | `your-app-password` |
| `MAIL_DEFAULT_SENDER` | Default sender email | `noreply@yourdomain.com` |
| `DATABASE_URL` | Database URL (optional) | `sqlite:///database/app.db` |

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/resend-verification` - Resend verification email

### System
- `GET /api/health` - Health check
- `GET /verify-email/<token>` - Email verification

## Security Features

- Password strength validation (8+ chars, letters + numbers)
- Email verification required for login
- Secure password hashing with Werkzeug
- CORS protection
- SQL injection prevention
- Input validation and sanitization

## Database Schema

### Users Table
- `id` - Primary key
- `email` - Unique email address
- `password_hash` - Hashed password
- `first_name` - User's first name
- `last_name` - User's last name
- `phone_number` - Optional phone number
- `email_verified` - Email verification status
- `verification_token` - Email verification token
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp

## Development

### Project Structure
```
location-tracker-backend/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── models/
│   │   └── user.py          # User model and database schema
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   └── user.py          # User management routes
│   ├── static/              # Built React frontend files
│   └── database/            # SQLite database files
├── requirements.txt         # Python dependencies
├── Procfile                # Railway deployment configuration
├── railway.json            # Railway service configuration
└── README.md               # This file
```

### Adding New Features

1. **Database Changes**
   - Modify models in `src/models/`
   - Update database schema

2. **API Endpoints**
   - Add routes in `src/routes/`
   - Register blueprints in `src/main.py`

3. **Frontend Updates**
   - Frontend is built separately and copied to `src/static/`
   - Update React components and rebuild

## Troubleshooting

### Email Not Sending
- Check Gmail App Password is correct
- Verify 2FA is enabled on Gmail account
- Check MAIL_USERNAME and MAIL_PASSWORD variables

### Database Issues
- Delete `src/database/app.db` to reset database
- Check file permissions in database directory

### CORS Errors
- Verify CORS configuration in `src/main.py`
- Check frontend API base URL configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email support@locationtracker.com or create an issue on GitHub.

