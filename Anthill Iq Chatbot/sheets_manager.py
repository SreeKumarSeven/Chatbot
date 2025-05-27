import os
from datetime import datetime
from typing import Dict, List, Optional

class GoogleSheetsManager:
    """
    Mock implementation of GoogleSheetsManager that doesn't interact with Google Sheets.
    This class maintains the same interface but logs data to console instead of Google Sheets.
    """
    def __init__(self):
        print(f"Initializing Mock GoogleSheetsManager (Google Sheets integration disabled)")
        self.client = None
        self.sheet_id = None
    
    def _init_sheets(self):
        """Initialize the sheets if they don't exist - Mock implementation"""
        print("Mock: _init_sheets called (no action taken)")
        return

    def log_conversation(self, user_message: str, bot_response: str, source: str, user_id: Optional[str] = None, session_id: Optional[str] = None) -> bool:
        """Log a conversation to console instead of Google Sheets"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"MOCK LOG - CONVERSATION: timestamp={timestamp}, user_id={user_id or 'anonymous'}, session_id={session_id or ''}")
        print(f"User: {user_message}")
        print(f"Bot: {bot_response}")
        print(f"Source: {source}")
        return True
    
    def get_faqs(self) -> List[Dict[str, str]]:
        """Get all FAQs - Mock implementation returns default FAQs"""
        print("MOCK: get_faqs called")
        return [
            {"Question": "What is Anthill IQ?", "Answer": "Anthill IQ is a premium workspace provider with three locations in Bangalore, offering private offices, coworking spaces, dedicated desks, meeting rooms, event spaces, and training rooms."},
            {"Question": "What services do you offer?", "Answer": "We offer comprehensive workspace solutions including private office space, coworking space, dedicated desks, meeting rooms, event spaces, and training rooms at all our three locations in Bangalore."},
            {"Question": "Where are your locations?", "Answer": "We have three strategic locations in Bangalore: Koramangala, Indiranagar, and Whitefield."}
        ]
    
    def log_booking(self, booking_data: Dict) -> bool:
        """Log a booking to console instead of Google Sheets"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"MOCK LOG - BOOKING: timestamp={timestamp}")
        print(f"Name: {booking_data.get('name', '')}")
        print(f"Email: {booking_data.get('email', '')}")
        print(f"Phone: {booking_data.get('phone', '')}")
        print(f"Service: {booking_data.get('service', '')}")
        print(f"Location: {booking_data.get('location', '')}")
        print(f"Message: {booking_data.get('message', '')}")
        return True
            
    def save_booking(self, name: str, email: str, phone: str, datetime_str: str, user_id: Optional[str] = None, location: Optional[str] = None, service: Optional[str] = None) -> bool:
        """Save booking details to console instead of Google Sheets"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"MOCK SAVE - BOOKING: timestamp={timestamp}")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Service: {service or ''}")
        print(f"Location: {location or ''}")
        print(f"Message/DateTime: {datetime_str}")
        return True
     
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations - Mock implementation returns empty list"""
        print(f"MOCK: get_recent_conversations called with limit={limit}")
        return []
    
    def get_recent_bookings(self, limit: int = 10) -> List[Dict]:
        """Get recent bookings - Mock implementation returns empty list"""
        print(f"MOCK: get_recent_bookings called with limit={limit}")
        return [] 