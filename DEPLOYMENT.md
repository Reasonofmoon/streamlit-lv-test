# Deployment Guide

## Overview
This guide covers deploying the Streamlit CEFR Test Platform to GitHub and Vercel.

## Prerequisites
- GitHub account with repository access
- Vercel account
- Python 3.8+ (for local development)

## Local Development

### 1. Clone the repository
```bash
git clone https://github.com/Reasonofmoon/streamlit-lv-test.git
cd streamlit-lv-test
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Or use Streamlit secrets for local development
```

### 4. Run the application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## GitHub Deployment

### 1. Push to GitHub
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### 2. Repository Settings
- Ensure `.streamlit/secrets.toml` is in `.gitignore`
- Use GitHub Secrets for sensitive data
- Add `STREAMLIT_USERS` as a repository secret (optional)

## Vercel Deployment

### 1. Connect Vercel to GitHub
1. Go to [Vercel](https://vercel.com)
2. Click "Add New Project"
3. Select your GitHub repository
4. Click "Import"

### 2. Configure Project

#### Framework Preset
- **Framework Preset**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: `.`
- **Install Command**: `pip install -r requirements.txt`

#### Environment Variables
Add the following environment variables in Vercel:

```bash
STREAMLIT_USERS='{"darlbit": {"password": "darlbit123", "role": "student"}, "darlbitt": {"password": "darlbitt123", "role": "teacher"}}'
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

To add environment variables in Vercel:
1. Go to Settings → Environment Variables
2. Click "Add New"
3. Enter the key and value
4. Select all environments (Production, Preview, Development)
5. Click "Save"

### 3. Deploy
1. Click "Deploy"
2. Vercel will build and deploy your application
3. The URL will be: `https://your-project-name.vercel.app`

### 4. Streamlit Configuration
Streamlit requires specific configuration for Vercel deployment. The `vercel.json` file handles this automatically.

## Authentication Configuration

### Local Development
Edit `.streamlit/secrets.toml`:
```toml
[users]
[users.username]
password = "your_password"
role = "student"
```

### Production (Vercel)
Use environment variables:
```bash
STREAMLITSERS='{"username": {"password": "your_password", "role": "student"}}'
```

## User Management

### Adding Users
For local development, edit `.streamlit/secrets.toml`:

```toml
[users]
[users.new_user]
password = "secure_password"
role = "teacher"
name = "Full Name"
school = "School Name"
grade = "1"
class = "A"
```

For production, update the `STREAMLIT_USERS` environment variable.

### User Roles
- **student**: Can take tests
- **teacher**: Can view results and analytics

## Database

### Local
The SQLite database is located at `data/cefr_test.db`

### Production
For production use, consider migrating to a cloud database:
1. Set up a cloud database (PostgreSQL, MySQL, etc.)
2. Update the database connection in `utils/db_manager.py`
3. Add database credentials to environment variables

## Troubleshooting

### Vercel Deployment Issues

**Issue: Build fails**
- Check that `requirements.txt` is complete
- Ensure all dependencies are compatible with Vercel's Python version

**Issue: App doesn't start**
- Verify environment variables are set correctly
- Check Vercel logs for specific error messages

**Issue: Authentication not working**
- Ensure `STREAMLIT_USERS` is properly formatted JSON
- Check that the environment variable is set in all environments

### Local Development Issues

**Issue: Import errors**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Issue: Streamlit secrets not loading**
- Verify `.streamlit/secrets.toml` exists
- Restart Streamlit

## Continuous Deployment

Vercel provides automatic deployment:
- Every push to the `main` branch triggers a deployment
- Pull requests create preview deployments
- Configure deployment hooks in Vercel settings for custom workflows

## Security Best Practices

1. **Never commit secrets** - Always use environment variables or secrets
2. **Use strong passwords** - Secure authentication credentials
3. **Enable HTTPS** - Vercel provides automatic SSL certificates
4. **Regular updates** - Keep dependencies updated
5. **Access control** - Limit Vercel project access

## Monitoring

### Vercel Analytics
- Monitor application performance
- Track user engagement
- Set up alerts for errors

### Logs
- View real-time logs in Vercel dashboard
- Streamlit logs are available in the deployment console

## Support

For issues or questions:
- GitHub Issues: https://github.com/Reasonofmoon/streamlit-lv-test/issues
- Streamlit Docs: https://docs.streamlit.io
- Vercel Docs: https://vercel.com/docs
