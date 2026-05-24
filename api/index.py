"""Minimal FastAPI test for Vercel deployment."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def root():
    return JSONResponse({"status": "ok", "message": "Hello from Vercel!"})


@app.get("/{path:path}")
async def catch_all(path: str):
    return JSONResponse({"status": "ok", "path": path})
