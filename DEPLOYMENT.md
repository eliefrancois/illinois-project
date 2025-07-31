# 🚀 Deployment Guide
## Illinois Basketball Analytics Project

This guide covers deploying the Illinois Basketball Analytics Project to production environments.

---

## 📋 Deployment Options

### **Option 1: Streamlit Cloud (Frontend) + Railway/Render (Backend)**
- **Frontend**: Deploy to Streamlit Cloud (free tier available)
- **Backend**: Deploy to Railway, Render, or Heroku
- **Database**: Use Supabase or similar

### **Option 2: Full Cloud Deployment**
- **Frontend**: Deploy to AWS, GCP, or Azure
- **Backend**: Deploy to same cloud provider
- **Database**: Cloud database service

---

## 🎯 Streamlit Cloud Deployment

### **1. Frontend Deployment (Streamlit Cloud)**

#### **Step 1: Prepare Your Repository**
```bash
# Ensure your repository is on GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### **Step 2: Deploy to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and main branch
5. Set the path to your Streamlit app: `frontend/streamlit_app.py`
6. Click "Deploy"

#### **Step 3: Configure Environment Variables**
In Streamlit Cloud dashboard:
1. Go to your app settings
2. Add environment variable:
   - **Key**: `API_BASE_URL`
   - **Value**: Your backend API URL (e.g., `https://your-backend.railway.app`)

---

## 🔧 Backend Deployment

### **Option A: Railway Deployment (Recommended)**

#### **Step 1: Prepare Backend**
```bash
# Create a Procfile for Railway
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile
```

#### **Step 2: Deploy to Railway**
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Set the root directory to `backend`
7. Railway will auto-detect Python and deploy

#### **Step 3: Get Your API URL**
- Railway will provide a URL like: `https://your-app-name.railway.app`
- Use this URL as your `API_BASE_URL` in Streamlit Cloud

### **Option B: Render Deployment**

#### **Step 1: Create render.yaml**
```yaml
# render.yaml
services:
  - type: web
    name: illinois-basketball-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    rootDir: backend
```

#### **Step 2: Deploy to Render**
1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New Web Service"
4. Connect your repository
5. Render will auto-detect the configuration

### **Option C: Heroku Deployment**

#### **Step 1: Prepare for Heroku**
```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile

# Create runtime.txt
echo "python-3.12.0" > backend/runtime.txt
```

#### **Step 2: Deploy to Heroku**
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Deploy
git subtree push --prefix backend heroku main
```

---

## 🔐 Environment Variables

### **Backend Environment Variables**
Set these in your backend deployment platform:

```env
# API Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Data Sources (Optional)
BARTTORVIK_BASE_URL=https://barttorvik.com

# Security
SECRET_KEY=your-secret-key-here
```

### **Frontend Environment Variables**
Set these in Streamlit Cloud:

```env
# API Configuration
API_BASE_URL=https://your-backend-url.com

# Optional: Additional configuration
ENVIRONMENT=production
```

---

## 🧪 Testing Your Deployment

### **1. Test Backend API**
```bash
# Test health endpoint
curl https://your-backend-url.com/health

# Test team search
curl "https://your-backend-url.com/teams/search?query=Illinois"
```

### **2. Test Frontend**
- Visit your Streamlit Cloud URL
- Check if the dashboard loads
- Test team search functionality
- Verify API connection status

### **3. Common Issues**

#### **CORS Errors**
If you get CORS errors, update your backend CORS settings:

```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Connection Refused**
- Ensure your backend is running
- Check the API_BASE_URL is correct
- Verify the backend URL is accessible

#### **Environment Variables Not Loading**
- Restart your Streamlit app after setting environment variables
- Check variable names are correct
- Ensure no extra spaces in values

---

## 📊 Production Considerations

### **Performance**
- **Caching**: Consider adding Redis for data caching
- **CDN**: Use a CDN for static assets
- **Database**: Add Supabase for data persistence

### **Security**
- **HTTPS**: Ensure all URLs use HTTPS
- **API Keys**: Secure any API keys in environment variables
- **CORS**: Configure CORS properly for production

### **Monitoring**
- **Logs**: Monitor application logs
- **Metrics**: Track API response times
- **Errors**: Set up error alerting

---

## 🔄 Continuous Deployment

### **GitHub Actions (Optional)**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        # Add Railway deployment steps
```

---

## 📞 Troubleshooting

### **Common Deployment Issues**

1. **ModuleNotFoundError**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

2. **Port Issues**
   - Use `$PORT` environment variable
   - Ensure host is set to `0.0.0.0`

3. **Environment Variables**
   - Double-check variable names
   - Restart services after changes

4. **API Connection**
   - Test backend URL directly
   - Check CORS settings
   - Verify SSL certificates

### **Getting Help**
1. Check the [LOCAL_SETUP.md](LOCAL_SETUP.md) for local troubleshooting
2. Review platform-specific documentation
3. Check application logs for error details
4. Test API endpoints directly

---

## 🎉 Success Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed on Streamlit Cloud
- [ ] Environment variables configured
- [ ] API endpoints responding correctly
- [ ] Frontend connecting to backend
- [ ] Team search functionality working
- [ ] Scouting reports generating
- [ ] All pages loading properly

---

*Happy deploying! 🚀* 