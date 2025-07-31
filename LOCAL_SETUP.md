# 🏀 Local Setup Guide
## Illinois Basketball Analytics Project

This guide will walk you through setting up and running the College Basketball Opponent Scouting Dashboard locally on your machine.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.11)
- **Git** (for cloning the repository)
- **pip** (Python package manager)
- **Virtual environment tool** (venv, conda, or pipenv)

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

---

## 🚀 Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd illinois-project
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
pip install -r requirements.txt

# Return to project root
cd ..
```

### 4. Run the Application

#### Option A: Run Both Services (Recommended)
Open **two terminal windows** and run:

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
streamlit run streamlit_app.py --server.port 8501
```

#### Option B: Run Demo Version (Simpler)
```bash
# Run the demo application directly
python demo_final.py
```

### 5. Access the Application
- **Frontend Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🔧 Detailed Setup

### Environment Configuration

Create a `.env` file in the project root:

```bash
# Create environment file
touch .env
```

Add the following configuration to your `.env` file:

```env
# API Configuration
API_BASE_URL=http://localhost:8000
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key

# External API Keys (Optional for basic functionality)
OPENAI_API_KEY=your-openai-api-key
BARTTORVIK_API_KEY=your-barttorvik-api-key

# Database Configuration
DATABASE_URL=your-database-connection-string

# Application Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key-here
```

### Optional: API Keys Setup

For full functionality, you may want to set up these API keys:

1. **OpenAI API Key** (for AI-generated reports):
   - Visit: https://platform.openai.com/api-keys
   - Create a new API key
   - Add to your `.env` file

2. **Supabase** (for data caching):
   - Visit: https://supabase.com
   - Create a new project
   - Get your URL and anon key
   - Add to your `.env` file

---

## 🏃‍♂️ Running Different Components

### Backend Only (FastAPI)
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Available Endpoints:**
- `GET /` - Health check
- `GET /health` - API status
- `GET /teams/search` - Search teams
- `GET /teams/list` - List all teams
- `GET /teams/{team_name}` - Get team stats
- `GET /teams/compare/{team1}/{team2}` - Compare teams

### Frontend Only (Streamlit)
```bash
cd frontend
streamlit run streamlit_app.py --server.port 8501
```

### Demo Applications
```bash
# Full demo with data
python demo_final.py

# Basic demo
python demo_app.py

# Fixed demo version
python demo_app_fixed.py
```

---

## 🧪 Testing the Setup

### 1. Test Backend API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test team search
curl "http://localhost:8000/teams/search?query=Illinois"
```

### 2. Test Frontend
- Open http://localhost:8501 in your browser
- Navigate through different pages
- Check if API connection is working

### 3. Test Data Sources
- Go to "Data Sources" page in the frontend
- Verify BartTorvik data is accessible
- Check if team search functionality works

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
lsof -i :8000
lsof -i :8501

# Kill the process or use different ports
uvicorn app.main:app --reload --port 8001
streamlit run streamlit_app.py --server.port 8502
```

#### 2. Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. API Connection Issues
- Check if backend is running on port 8000
- Verify API_BASE_URL in frontend configuration
- Check CORS settings in backend

#### 4. Data Loading Issues
- BartTorvik data is publicly available, no API key required
- Check internet connection
- Verify the service is accessible

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug
streamlit run streamlit_app.py --logger.level debug
```

---

## 📁 Project Structure

```
illinois-project/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main application
│   │   ├── routers/        # API routes
│   │   └── services/       # Data services
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Streamlit frontend
│   ├── streamlit_app.py   # Main dashboard
│   ├── pages/             # Additional pages
│   ├── components/        # Reusable components
│   └── requirements.txt   # Frontend dependencies
├── data/                  # Data scripts and files
├── demo_*.py             # Demo applications
├── requirements.txt      # Root dependencies
└── README.md            # Project documentation
```

---

## 🚀 Next Steps

Once you have the application running locally:

1. **Explore the Dashboard**: Navigate through different pages and features
2. **Test Team Analysis**: Search for teams and view their statistics
3. **Try Comparisons**: Compare different teams' performance metrics
4. **Review API Documentation**: Visit http://localhost:8000/docs
5. **Check Data Sources**: Verify all data sources are working correctly

### Development Workflow
```bash
# Make changes to code
# Backend will auto-reload with --reload flag
# Frontend will auto-reload with Streamlit

# Test changes
# Commit and push to repository
```

---

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the API documentation at http://localhost:8000/docs
3. Check the console logs for error messages
4. Verify all dependencies are installed correctly

---

*Happy coding! 🏀* 