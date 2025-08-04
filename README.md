# Live Location Tracker

## Project Overview

Live Location Tracker is a web application designed to provide real-time location tracking capabilities, primarily focused on family safety. It includes features for user authentication, email verification, and serving a frontend application.

## Features

*   User Registration and Authentication
*   Email Verification with secure tokens
*   Real-time Location Tracking (core functionality to be implemented/extended)
*   RESTful API for user and authentication management
*   Frontend served by Flask backend
*   Health check endpoint for deployment monitoring

## Technologies Used

**Backend:**
*   Python 3
*   Flask (Web Framework)
*   Flask-SQLAlchemy (ORM for SQLite database)
*   Flask-CORS (Handling Cross-Origin Resource Sharing)
*   Flask-Mail (Email sending)
*   Gunicorn (WSGI HTTP Server)

**Frontend:**
*   React (based on `App.jsx` and `index.html`)

**Database:**
*   SQLite (for development and small-scale deployments)

**Deployment:**
*   Railway

## Local Development Setup

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/live-location-tracker.git
    cd live-location-tracker
    ```

2.  **Create a Python Virtual Environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables:**
    Create a `.env` file in the root directory of your project (you can use `.env.example` as a template) and add the following:
    ```
    SECRET_KEY=your-super-secret-key-here
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=your_gmail_username@gmail.com
    MAIL_PASSWORD=your_gmail_app_password
    MAIL_DEFAULT_SENDER=noreply@yourdomain.com
    FLASK_ENV=development
    ```
    *Replace placeholders with your actual values. For `MAIL_PASSWORD`, use a Gmail App Password if you have 2-Factor Authentication enabled.*

5.  **Run the Application:**
    ```bash
    python main.py
    ```
    The application should now be running on `http://localhost:5000`.

## Deployment to Railway

This project is configured for easy deployment to Railway. Follow these steps:

1.  **Push your code to GitHub:**
    Ensure your project is pushed to a GitHub repository.

2.  **Connect GitHub to Railway:**
    *   Go to [railway.app](https://railway.app) and log in with your GitHub account.
    *   Click 


"New Project" and select "Deploy from GitHub repo".
    *   Choose your `live-location-tracker` repository.

3.  **Configure Environment Variables on Railway:**
    In your Railway project dashboard, go to the "Variables" tab and add the following:

    | Variable Name         | Example Value                                |
    |-----------------------|----------------------------------------------|
    | `SECRET_KEY`          | `your-super-secret-key-here`                 |
    | `MAIL_USERNAME`       | `youremail@gmail.com`                        |
    | `MAIL_PASSWORD`       | `abcd efgh ijkl mnop` (Gmail App Password)   |
    | `MAIL_DEFAULT_SENDER` | `noreply@yourdomain.com`                     |
    | `FLASK_ENV`           | `production`                                 |

4.  **Deployment:**
    Railway will automatically detect your `Procfile` and `railway.json` and deploy your application. Monitor the deployment logs in the Railway dashboard.

## Troubleshooting Deployment

*   **Healthcheck Failure:** This often indicates that your application is not starting correctly. Ensure your `Procfile` and `railway.json` correctly point to your main application file (`main:app`). I have already updated these files for you.
*   **Build Fails:** Check Railway logs for build errors. Ensure all dependencies are listed in `requirements.txt` and all necessary files are committed to your GitHub repository.
*   **Email Not Working:** Double-check your `MAIL_USERNAME` and `MAIL_PASSWORD` (Gmail App Password) in Railway environment variables. Ensure 2-Factor Authentication is enabled for your Gmail account and you are using an App Password.
*   **500 Internal Server Error:** Check Railway logs for Python traceback. This could be due to missing environment variables, database issues, or other runtime errors.

## Production Checklist

*   ✅ All necessary environment variables are configured on Railway.
*   ✅ Gmail App Password is correctly set for email functionality.
*   ✅ Database is initialized (consider using a persistent database like PostgreSQL for production).
*   ✅ HTTPS is enabled (automatic with Railway).
*   ✅ Error logging is configured.
*   ✅ Health check endpoint (`/api/health`) is working.
*   ✅ Frontend assets are served correctly.

## Support

If you encounter any issues or have questions, please refer to the `LiveLocationTracker-DeploymentGuide.md` file in this repository or open an issue on the GitHub repository.
