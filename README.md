# College Basketball Opponent Scouting Dashboard

A lightweight, interactive scouting dashboard to help college coaching staffs prepare for upcoming opponents using publicly available statistics.

## Features

- **Data Sources**: BartTorvik (T-Rank), KenPom, Sports Reference
- **Database**: Supabase for caching and querying
- **Frontend**: Streamlit dashboard
- **Backend**: FastAPI for data processing
- **AI Integration**: OpenAI for automated scouting reports

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   └── services/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── streamlit_app.py
│   ├── pages/
│   ├── components/
│   └── requirements.txt
├── data/
│   └── scripts/
├── .env.example
└── README.md
```

## Setup

1. Clone the repository
2. Set up virtual environment
3. Install dependencies
4. Configure environment variables
5. Run the application

## Data Sources

- **BartTorvik**: Primary source - offers free CSV/JSON downloads
- **Sports Reference**: Backup source for additional metrics
- **KenPom**: Premium source (subscription required)

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```