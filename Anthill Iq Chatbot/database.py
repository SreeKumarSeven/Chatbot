from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable (Railway PostgreSQL URL)
DATABASE_URL = os.getenv('DATABASE_URL')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    total_chats = Column(Integer, default=0)
    
    # Relationship with ChatHistory
    chat_history = relationship('ChatHistory', back_populates='user', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        Index('idx_user_phone', 'phone'),
        Index('idx_user_created_at', 'created_at'),
        Index('idx_user_last_active', 'last_active')
    )
    
    def update_chat_count(self):
        """Update total chats count"""
        self.total_chats += 1

# Define ChatHistory model
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100), nullable=False)
    message_type = Column(String(20), default='text')  # text, question, feedback, etc.
    sentiment = Column(String(20), nullable=True)  # positive, negative, neutral
    
    # Relationship with User
    user = relationship('User', back_populates='chat_history')
    
    # Indexes
    __table_args__ = (
        Index('idx_chat_user_id', 'user_id'),
        Index('idx_chat_timestamp', 'timestamp'),
        Index('idx_chat_session', 'session_id')
    )

# Create all tables
Base.metadata.create_all(engine)

# Create SessionLocal class
SessionLocal = sessionmaker(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for database operations
def create_user(db: SessionLocal, name: str, phone: str) -> User:
    """Create a new user"""
    user = User(name=name, phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_phone(db: SessionLocal, phone: str) -> User:
    """Get user by phone number"""
    return db.query(User).filter(User.phone == phone).first()

def add_chat_history(db: SessionLocal, user_id: int, message: str, response: str, session_id: str) -> ChatHistory:
    """Add a new chat history entry"""
    chat = ChatHistory(
        user_id=user_id,
        message=message,
        response=response,
        session_id=session_id
    )
    db.add(chat)
    
    # Update user's chat count
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.update_chat_count()
    
    db.commit()
    db.refresh(chat)
    return chat

def get_user_chat_history(db: SessionLocal, user_id: int, limit: int = 50) -> list:
    """Get chat history for a user"""
    return db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).order_by(ChatHistory.timestamp.desc()).limit(limit).all() 