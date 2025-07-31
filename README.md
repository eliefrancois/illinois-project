# College Basketball Opponent Scouting Dashboard

A comprehensive, interactive scouting dashboard to help college coaching staffs prepare for upcoming opponents using advanced basketball analytics and AI-powered insights.

## 🏀 Current Features (Implemented)

### **Data Sources & Analytics**
- ✅ **BartTorvik (T-Rank)**: Primary data source with real-time team statistics
- ✅ **Advanced Metrics**: AdjOE, AdjDE, Barthag ratings, SOS, WAB, and more
- ✅ **364 Teams**: Complete Division I coverage for the 2025 season
- ✅ **Real-time Data**: Live updates from BartTorvik API

### **Dashboard & Analytics**
- ✅ **Interactive Dashboard**: Real-time metrics and connection status
- ✅ **Team Search & Analysis**: Comprehensive team statistics and rankings
- ✅ **Head-to-Head Comparisons**: Detailed team matchup analysis
- ✅ **Conference Analysis**: Team positioning within conferences

### **Scouting & Game Preparation**
- ✅ **Automated Scouting Reports**: AI-generated opponent analysis
- ✅ **Strengths & Weaknesses**: Detailed offensive/defensive breakdown
- ✅ **Game Plan Suggestions**: Strategic recommendations based on opponent data
- ✅ **Tempo Analysis**: Playing style and pace recommendations
- ✅ **Matchup Analysis**: Head-to-head comparisons with your team

### **Technical Architecture**
- ✅ **FastAPI Backend**: High-performance API with real-time data processing
- ✅ **Streamlit Frontend**: Interactive web dashboard with modern UI
- ✅ **Robust Data Pipeline**: Manual CSV parsing for reliable data extraction
- ✅ **Error Handling**: Comprehensive error management and fallback mechanisms

## 🚀 Future Enhancements (Planned)

### **Phase 2: Enhanced Analytics (Q2 2024)**
- 🔄 **Player-Level Analysis**: Individual player statistics and LLM-generated insights
- 🔄 **Advanced Data Sources**: Synergy Sports, SportVU, and additional APIs
- 🔄 **Mobile Optimization**: Responsive design for coaching staff access
- 🔄 **Workflow Integration**: Custom dashboards based on coaching feedback

### **Phase 3: AI-Powered Intelligence (Q3 2024)**
- 🔄 **Predictive Modeling**: Win probability and performance forecasting
- 🔄 **Real-time Integration**: Live game data and instant analysis
- 🔄 **Video Analytics**: Statistical insights linked to game film
- 🔄 **Collaborative Platform**: Multi-user access with role-based permissions

### **Phase 4: Advanced Features (Q4 2024)**
- 🔄 **Recruitment Analytics**: Data-driven player evaluation tools
- 🔄 **Social Media Integration**: Sentiment analysis and psychological insights
- 🔄 **Advanced ML Models**: Deep learning for pattern recognition
- 🔄 **Enterprise Integration**: API connections with existing team systems

## 📁 Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main application
│   │   ├── routers/        # API routes (teams, etc.)
│   │   └── services/       # Data services (BartTorvik)
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Streamlit frontend
│   ├── streamlit_app.py   # Main dashboard
│   ├── pages/             # Additional pages
│   ├── components/        # Reusable components
│   └── requirements.txt   # Frontend dependencies
├── data/                  # Data scripts and files
├── demo_*.py             # Demo applications
├── requirements.txt      # Root dependencies
├── LOCAL_SETUP.md       # Local setup guide
├── PROJECT_PRESENTATION.md # Project presentation
└── README.md            # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (recommended: Python 3.11)
- Git
- Virtual environment tool (venv, conda, or pipenv)

### Installation

1. **Clone and Setup**
```bash
git clone <your-repository-url>
cd illinois-project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install -r requirements.txt
```

3. **Run the Application**
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
streamlit run streamlit_app.py --server.port 8501
```

4. **Access the Application**
- **Frontend Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📊 Data Sources

### **Current Implementation**
- ✅ **BartTorvik (T-Rank)**: Primary source with real-time team statistics
- ✅ **364 Teams**: Complete Division I coverage for 2025 season
- ✅ **Advanced Metrics**: AdjOE, AdjDE, Barthag, SOS, WAB, and more

### **Planned Integrations**
- 🔄 **KenPom**: Premium analytics (subscription required)
- 🔄 **Sports Reference**: Historical data and additional metrics
- 🔄 **Synergy Sports**: Advanced player tracking
- 🔄 **SportVU**: Player movement and positioning data

## 🔌 API Endpoints

### **Team Management**
- `GET /teams/search?query={team_name}` - Search for teams by name
- `GET /teams/{team_name}` - Get detailed statistics for a specific team
- `GET /teams/compare/{team1}/{team2}` - Compare two teams
- `GET /teams/list` - Get list of all available teams

### **Example Usage**
```bash
# Search for Illinois
curl "http://localhost:8000/teams/search?query=Illinois"

# Get Illinois statistics
curl "http://localhost:8000/teams/Illinois"

# Compare Illinois vs Duke
curl "http://localhost:8000/teams/compare/Illinois/Duke"

# Get all teams
curl "http://localhost:8000/teams/list"
```

## 🎯 Key Features

### **Dashboard Analytics**
- Real-time team statistics and rankings
- Conference analysis and team positioning
- Live data connection status

### **Scouting Reports**
- Automated opponent analysis
- Strengths and weaknesses identification
- Game plan suggestions
- Tempo and playing style analysis

### **Team Comparisons**
- Head-to-head matchup analysis
- Statistical advantage identification
- Performance benchmarking

## 📈 Performance Metrics

The application currently provides:
- **364 Teams**: Complete Division I coverage
- **Real-time Data**: Live updates from BartTorvik
- **Advanced Analytics**: 14+ key performance indicators per team
- **Fast Response**: Sub-second API response times

## 📚 Documentation

- **[LOCAL_SETUP.md](LOCAL_SETUP.md)**: Detailed local setup guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Production deployment guide
- **[PROJECT_PRESENTATION.md](PROJECT_PRESENTATION.md)**: Comprehensive project overview
- **[API Documentation](http://localhost:8000/docs)**: Interactive API docs (when running)

## 🛠️ Development

### **Tech Stack**
- **Backend**: FastAPI, Python 3.12, Pandas, Requests
- **Frontend**: Streamlit, Plotly, React components
- **Data**: BartTorvik API, Manual CSV parsing
- **Architecture**: RESTful API with modern web interface

### **Contributing**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🎯 Use Cases

### **For Coaching Staffs**
- Quick opponent analysis and scouting
- Game plan development and strategy
- Team performance tracking
- Conference and national context

### **For Analysts**
- Advanced statistical analysis
- Team comparison and benchmarking
- Data-driven insights
- Performance trend analysis

## 📞 Support

For questions or issues:
1. Check the [LOCAL_SETUP.md](LOCAL_SETUP.md) for troubleshooting
2. Review the API documentation at http://localhost:8000/docs
3. Check console logs for error messages
4. Verify all dependencies are installed correctly

---

*Built for Illinois Basketball by Illinois Basketball* 🏀