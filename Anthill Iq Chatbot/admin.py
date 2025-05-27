from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import jwt
from pydantic import BaseModel
from database import get_db, User, ChatHistory

# Create router
router = APIRouter(prefix="/api/admin", tags=["admin"])

# JWT Configuration
SECRET_KEY = "your-secret-key-here"  # Change this to a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

# Admin credentials (store these securely in production)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "anthilliq2024"  # Change this to a secure password

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class AdminLogin(BaseModel):
    username: str
    password: str

class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_conversations: int
    avg_response_time: float

class UserResponse(BaseModel):
    name: str
    phone: str
    created_at: datetime
    last_active: datetime
    total_chats: int

class ConversationResponse(BaseModel):
    user_name: str
    message: str
    response: str
    timestamp: datetime

# Authentication functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username != ADMIN_USERNAME:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Endpoints
@router.post("/login", response_model=Token)
async def login(form_data: AdminLogin):
    if form_data.username != ADMIN_USERNAME or form_data.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/stats", response_model=DashboardStats)
async def get_stats(current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    active_today = db.query(User).filter(
        User.last_active >= datetime.utcnow() - timedelta(days=1)
    ).count()
    total_conversations = db.query(ChatHistory).count()
    
    # Calculate average response time (dummy value for now)
    avg_response_time = 2.5  # seconds
    
    return {
        "total_users": total_users,
        "active_users": active_today,
        "total_conversations": total_conversations,
        "avg_response_time": avg_response_time
    }

@router.get("/recent-users", response_model=List[UserResponse])
async def get_recent_users(
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db),
    limit: int = 10
):
    users = db.query(User).order_by(User.created_at.desc()).limit(limit).all()
    return users

@router.get("/recent-conversations", response_model=List[ConversationResponse])
async def get_recent_conversations(
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db),
    limit: int = 20
):
    conversations = (
        db.query(
            ChatHistory,
            User.name.label("user_name")
        )
        .join(User)
        .order_by(ChatHistory.timestamp.desc())
        .limit(limit)
        .all()
    )
    
    return [
        {
            "user_name": conv.user_name,
            "message": conv.ChatHistory.message,
            "response": conv.ChatHistory.response,
            "timestamp": conv.ChatHistory.timestamp
        }
        for conv in conversations
    ] 