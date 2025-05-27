from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional, List
import os
import json
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
from chat import ChatManager
from database import (
    get_db, User, ChatHistory, 
    create_user, get_user_by_phone,
    add_chat_history, get_user_chat_history
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.staticfiles import StaticFiles
from admin import router as admin_router

# Load environment variables from .env file
load_dotenv()

# Check if OpenAI API key is available
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please check your .env file.")

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize chat manager
chat_manager = ChatManager()

# Models
class ChatRequest(BaseModel):
    message: str
    phone: str
    session_id: Optional[str] = None

class UserRegistration(BaseModel):
    name: str
    phone: str

class ChatHistoryResponse(BaseModel):
    message: str
    response: str
    timestamp: datetime
    session_id: str

class UserStatsResponse(BaseModel):
    total_chats: int
    last_active: datetime
    joined_date: datetime

@app.post("/api/register")
async def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    """Register a new user or return existing user"""
    try:
        # Check for existing user
        existing_user = get_user_by_phone(db, user_data.phone)
        if existing_user:
            return {
                "status": "success",
                "user_id": existing_user.id,
                "message": "User already registered",
                "is_new": False
            }
        
        # Create new user
        new_user = create_user(db, user_data.name, user_data.phone)
        return {
            "status": "success",
            "user_id": new_user.id,
            "message": "User registered successfully",
            "is_new": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_endpoint(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """Process chat messages and store in database"""
    if not chat_request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Get user
        user = get_user_by_phone(db, chat_request.phone)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Generate session ID if not provided
        session_id = chat_request.session_id or str(uuid.uuid4())
        
        # Process chat message
        result = await chat_manager.handle_message(
            chat_request.message,
            str(user.id)
        )
        
        # Save chat history
        add_chat_history(
            db,
            user.id,
            chat_request.message,
            result["response"],
            session_id
        )
        
        # Add session ID to response
        result["session_id"] = session_id
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat-history/{phone}")
async def get_chat_history(
    phone: str,
    limit: int = Query(default=50, le=100),
    db: Session = Depends(get_db)
):
    """Get chat history for a user"""
    try:
        user = get_user_by_phone(db, phone)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        history = get_user_chat_history(db, user.id, limit)
        
        return {
            "status": "success",
            "history": [
                ChatHistoryResponse(
                    message=chat.message,
                    response=chat.response,
                    timestamp=chat.timestamp,
                    session_id=chat.session_id
                ) for chat in history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/stats/{phone}")
async def get_user_stats(phone: str, db: Session = Depends(get_db)):
    """Get user statistics"""
    try:
        user = get_user_by_phone(db, phone)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserStatsResponse(
            total_chats=user.total_chats,
            last_active=user.last_active,
            joined_date=user.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "openai": "configured" if openai_api_key else "not_configured",
            "database": "configured" if os.getenv("DATABASE_URL") else "not_configured"
        }
    }

# Mount admin routes
app.include_router(admin_router)

# Mount static files for admin dashboard
app.mount(
    "/admin_dashboard",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "admin_dashboard"), html=True),
    name="admin_dashboard"
)

@app.get("/")
def read_root():
    return {"message": "Anthill IQ Chatbot API is running."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port) 
