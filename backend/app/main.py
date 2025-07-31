"""
Main FastAPI application for College Basketball Opponent Scouting Dashboard.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import teams

app = FastAPI(
    title="College Basketball Scouting API",
    description="API for college basketball opponent scouting dashboard",
    version="1.0.0"
)

# Include routers
app.include_router(teams.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Local Streamlit
        "https://*.streamlit.app",  # Streamlit Cloud
        "https://*.streamlit.io",   # Streamlit Cloud (alternative)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "College Basketball Scouting API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)