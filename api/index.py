"""
Vercel serverless function entry point.
Re-exports the FastAPI application for deployment on Vercel.
"""
from web_app.main import app
