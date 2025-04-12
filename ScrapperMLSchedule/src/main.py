import os
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from browser.controller import BrowserController
from ai.processor import AIProcessor
from utils.logger import setup_logger, log_error, log_info

# Load environment variables
load_dotenv(Path("config/.env"))

# Initialize FastAPI app
app = FastAPI(title="Web Scraping & AI Analysis System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
logger = setup_logger("main")
browser = BrowserController()
ai_processor = AIProcessor(model=os.getenv("DEFAULT_MODEL", "phi3"))

class NavigateRequest(BaseModel):
    url: str

class ProcessRequest(BaseModel):
    file_path: str

@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {"status": "running"}

@app.post("/navigate")
async def navigate(request: NavigateRequest) -> Dict[str, Any]:
    """Navigate to specified URL."""
    try:
        success = await browser.navigate(request.url)
        if not success:
            raise HTTPException(status_code=500, detail="Navigation failed")
        
        log_info(logger, f"Successfully navigated to {request.url}")
        return {"status": "success", "message": f"Navigated to {request.url}"}
    
    except Exception as e:
        log_error(logger, e, "Navigation error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape")
async def scrape() -> Dict[str, Any]:
    """Trigger scraping action."""
    try:
        success = await browser.trigger_scrape()
        if not success:
            raise HTTPException(status_code=500, detail="Scraping failed")
        
        # Wait for download
        file_path = await browser.wait_for_download()
        if not file_path:
            raise HTTPException(status_code=500, detail="Download failed")
        
        log_info(logger, "Scraping completed successfully")
        return {
            "status": "success",
            "message": "Scraping completed",
            "file_path": file_path
        }
    
    except Exception as e:
        log_error(logger, e, "Scraping error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process(request: ProcessRequest) -> Dict[str, Any]:
    """Process scraped data using AI."""
    try:
        result = await ai_processor.process_data(request.file_path)
        if not result:
            raise HTTPException(status_code=500, detail="Processing failed")
        
        # Validate response format
        if not await ai_processor.validate_response(result):
            raise HTTPException(status_code=500, detail="Invalid AI response format")
        
        log_info(logger, "Data processing completed successfully")
        return {
            "status": "success",
            "message": "Processing completed",
            "data": result
        }
    
    except Exception as e:
        log_error(logger, e, "Processing error")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def status() -> Dict[str, Any]:
    """Get system status."""
    return {
        "status": "healthy",
        "browser": "connected",  # TODO: Implement actual connection check
        "ai_model": ai_processor.model
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVER_PORT", 8000))
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    
    log_info(logger, f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
