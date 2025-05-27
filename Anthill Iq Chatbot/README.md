# Anthill IQ Chatbot

A modern, conversational AI chatbot for Anthill IQ built with FastAPI, SQLAlchemy, and OpenAI.

## Recent Updates

### Database Integration (Railway)
- Integrated PostgreSQL database hosted on Railway
- Added database connection configuration via environment variables
- Implemented database models for users and chat history
- Added session management and user persistence

### User Management
- Implemented user registration and recognition system
- Users are identified by phone number
- Chat history is preserved between sessions
- Added user statistics tracking (total chats, last active, join date)

### Location Updates
- Added new Hebbal location:
  ```
  AnthillIQ Workspaces
  44/2A, Kodigehalli gate
  Sahakarnagar post, Hebbal
  Bengaluru, Karnataka 560092
  ```
- Simplified location display format
- Removed map URLs for cleaner responses

### Chatbot Improvements
- Removed booking forms and form-based data collection
- Enhanced conversational flow
- Added multi-user support with session management
- Improved response handling and context management

### File Structure Cleanup
- Removed unnecessary files:
  - test_connection.py
  - simple_proxy.py
  - wix-widget/* files
  - wix-integration/* files

## Environment Setup

1. Create a `.env` file in the project root with:
```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Railway Database Configuration
DATABASE_URL=your_railway_postgresql_url_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies
```
fastapi>=0.103.1
uvicorn>=0.23.2
pydantic>=2.3.0
openai>=1.3.0
faiss-cpu>=1.7.4
numpy>=1.24.0
python-dotenv>=1.0.0
httpx>=0.24.1
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.9
alembic>=1.12.0
```

## Database Schema

### Users Table
- id (Primary Key)
- name
- phone (Unique)
- created_at
- last_active
- is_active
- total_chats

### Chat History Table
- id (Primary Key)
- user_id (Foreign Key)
- message
- response
- timestamp
- session_id
- message_type
- sentiment

## API Endpoints

### User Management
- POST `/api/register` - Register new user or get existing user
- GET `/api/user/stats/{phone}` - Get user statistics

### Chat Operations
- POST `/api/chat` - Process chat messages
- GET `/api/chat-history/{phone}` - Get user chat history
- GET `/api/health` - Check API health

## Frontend Widget

The chatbot widget (`anthill_chatbot_widget.html`) provides:
- Modern, responsive design
- User registration interface
- Chat interface with message history
- Session management

## Testing

To test database connection:
```python
python test_db.py
```

## Running the Server

Start the FastAPI server:
```bash
python run_server.py
```

The server will run on `http://localhost:8000` by default.

## Notes
- User registration is required for first-time users
- Phone number is used as the unique identifier
- Chat history is preserved between sessions
- The system recognizes returning users by their phone number

## Google Sheets Setup

1. Create a new Google Sheet
2. Share it with the service account email: `anthill-chatbot-service@anthill-iq-chatot.iam.gserviceaccount.com`
3. Give it "Editor" access
4. Make sure your sheet has these worksheets:
   - Conversations
   - Bookings
   - FAQ

## Integration with Your Website

### For Wix:
1. In your Wix editor, add a new "Custom Element" or "HTML Embed" component
2. Copy the contents of the `anthill_chatbot_widget.html` file
3. Update the `API_URL` in the CONFIG section to point to your deployed backend
4. Publish your Wix site

### For Other Websites:
Add the chatbot widget to your site by including the HTML file or copying its code into your page.

## Troubleshooting

- If the chatbot can't connect to the Google Sheet, ensure you've shared it with the correct email address
- If you get OpenAI API errors, check your API key and quota
- For server connection issues, make sure the server is running on the correct port (8000)

For more detailed information, refer to the `QUICK_START.md` file. 