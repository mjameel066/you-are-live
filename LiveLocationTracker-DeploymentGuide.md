# Live Location Tracker - Deployment Guide

## Step-by-Step Deployment to Railway

### Prerequisites
- GitHub account (already created ✅)
- Railway account (already created ✅)
- Gmail account for email functionality

### Step 1: Prepare Gmail for Email Sending

1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Security → 2-Step Verification → Turn On

2. **Generate App Password**
   - Go to Google Account → Security
   - 2-Step Verification → App passwords
   - Select "Mail" and generate password
   - **Save this password** - you'll need it for Railway

### Step 2: Push to GitHub

1. **Create new repository on GitHub**
   - Go to github.com
   - Click "New repository"
   - Name: `live-location-tracker`
   - Make it public or private
   - Don't initialize with README (we have one)

2. **Push code to GitHub**
   ```bash
   cd location-tracker-backend
   git add .
   git commit -m "Initial deployment - Live Location Tracker"
   git remote add origin https://github.com/YOUR_USERNAME/live-location-tracker.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Railway

1. **Connect GitHub to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Login" and use GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `live-location-tracker` repository

2. **Configure Environment Variables**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add these variables:

   | Variable Name | Value | Example |
   |---------------|-------|---------|
   | `SECRET_KEY` | Generate a secure random string | `your-super-secret-key-here` |
   | `MAIL_USERNAME` | Your Gmail address | `youremail@gmail.com` |
   | `MAIL_PASSWORD` | Gmail App Password from Step 1 | `abcd efgh ijkl mnop` |
   | `MAIL_DEFAULT_SENDER` | Your sender email | `noreply@yourdomain.com` |
   | `FLASK_ENV` | `production` | `production` |

3. **Deploy**
   - Railway will automatically deploy
   - Wait for build to complete (2-3 minutes)
   - You'll get a public URL like `https://your-app.railway.app`

### Step 4: Test Your Deployment

1. **Visit your Railway URL**
   - Click the generated URL in Railway dashboard
   - You should see the Live Location Tracker login page

2. **Test Registration**
   - Click "Sign up"
   - Fill in test details with a real email address
   - Click "Create Account"
   - Check your email for verification link

3. **Test Email Verification**
   - Click the verification link in your email
   - Should see "Email Verified Successfully" page

4. **Test Login**
   - Go back to main page
   - Login with verified credentials
   - Should see the dashboard

### Step 5: Custom Domain (Optional)

1. **Add Custom Domain in Railway**
   - Go to Settings → Domains
   - Add your domain
   - Update DNS records as instructed

### Troubleshooting

#### Build Fails
- Check Railway logs in dashboard
- Ensure all files are committed to GitHub
- Verify requirements.txt is complete

#### Email Not Working
- Double-check Gmail App Password
- Ensure 2FA is enabled on Gmail
- Verify MAIL_USERNAME and MAIL_PASSWORD in Railway variables

#### 500 Internal Server Error
- Check Railway logs for Python errors
- Verify all environment variables are set
- Check database permissions

#### CORS Issues
- Ensure frontend is built and in static/ directory
- Check API calls are using relative URLs

### Production Checklist

- ✅ Environment variables configured
- ✅ Gmail App Password working
- ✅ Database initialized
- ✅ HTTPS enabled (automatic with Railway)
- ✅ Error logging configured
- ✅ Health check endpoint working
- ✅ Frontend assets served correctly

### Monitoring

- **Health Check**: `https://your-app.railway.app/api/health`
- **Railway Logs**: Available in Railway dashboard
- **Uptime**: Railway provides automatic monitoring

### Updates

To update your deployment:
1. Make changes to your code
2. Commit and push to GitHub
3. Railway will automatically redeploy

### Security Notes

- Never commit `.env` files to GitHub
- Use strong SECRET_KEY in production
- Gmail App Passwords are safer than regular passwords
- Railway provides HTTPS automatically
- Database is SQLite (consider PostgreSQL for production scale)

### Support

If you encounter issues:
1. Check Railway deployment logs
2. Verify all environment variables
3. Test email configuration with a simple test
4. Check GitHub repository has all files

Your Live Location Tracker should now be live and accessible worldwide! 🚀

