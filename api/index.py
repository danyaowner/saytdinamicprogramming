"""
Vercel serverless function entry point.
Adds web_app directory to Python path and re-exports the FastAPI app.
"""
import sys
import os

# Add web_app directory to sys.path so main.py can import dp_solver
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web_app")))

from main import app
