from fastapi import FastAPI
from sqlalchemy import text

from database import engine


app = FastAPI(
    title="LeaklyTex API",
    description="AI-Based Wastewater Pipeline Health and Predictive Maintenance System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "LeaklyTex",
        "message": "LeaklyTex Backend is running",
        "status": "OK"
    }


@app.get("/health")
def health():
    try:
        # Test whether the backend can connect to PostgreSQL
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }