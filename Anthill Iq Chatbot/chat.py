from openai import OpenAI
import os
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv
import re
import json

# Load environment variables from .env file
load_dotenv()

class ChatManager:
    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please check your .env file.")
        
        self.client = OpenAI(api_key=openai_api_key)
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        
        print(f"Using OpenAI model: {self.model_name}")
        
        # Store company data in memory
        self.company_data = {
            "name": "Anthill IQ",
            "welcome_message": "Hello! 👋 I'm the Anthill IQ Assistant. How can I help you today?",
            "locations": [
                {
                    "name": "Cunningham Road",
                    "area": "Central Bangalore (Vasanth Nagar area)",
                    "address": "1st Floor, Anthill IQ, 20, Cunningham Rd, Vasanth Nagar, Bengaluru, Karnataka 560052"
                },
                {
                    "name": "Arekere",
                    "area": "South Bangalore",
                    "address": "224, Bannerghatta Rd, near Arekere Gate, Arekere, Bengaluru, Karnataka 560076"
                },
                {
                    "name": "Hulimavu",
                    "area": "South Bangalore",
                    "address": "75/B Windsor F4, Bannerghatta Rd, opp. Christ University, Hulimavu, Bengaluru, Karnataka 560076"
                },
                {
                    "name": "Hebbal",
                    "area": "North Bangalore",
                    "address": "AnthillIQ Workspaces, 44/2A, Kodigehalli gate, Sahakarnagar post, Hebbal, Bengaluru, Karnataka 560092"
                }
            ],
            "services": [
                {
                    "name": "Private Office Space",
                    "description": "Fully furnished private offices with secure, dedicated workspace, customizable to your team size, with 24/7 access, high-speed internet, and complimentary beverages."
                },
                {
                    "name": "Coworking Space",
                    "description": "Flexible hot desks in a vibrant community atmosphere with high-speed internet, access to common areas, networking opportunities, and complimentary beverages."
                },
                {
                    "name": "Dedicated Desk",
                    "description": "Your personal fixed desk with ergonomic chair, storage space, 24/7 access, high-speed internet, and business address usage."
                },
                {
                    "name": "Meeting Room",
                    "description": "Professional meeting spaces with HD video conferencing, whiteboard and projector, catering options available, various room sizes."
                },
                {
                    "name": "Event Space",
                    "description": "Versatile event venues with AV equipment, flexible seating arrangements, catering services, perfect for workshops & seminars, and professional event support."
                },
                {
                    "name": "Training Room",
                    "description": "Classroom-style setup with interactive presentation tools, breakout areas, catering options, technical support, and flexible configurations."
                }
            ],
            "contact": {
                "phone": "+91 9119739119",
                "email": "connect@anthilliq.com",
                "website": "www.anthilliq.com"
            },
            "pricing_message": "For detailed pricing information specific to your needs, please contact our team."
        }

    def generate_locations_info(self) -> str:
        """Generate formatted location information for the OpenAI prompt"""
        locations_text = "Anthill IQ has the following locations:\n\n"
        
        for i, location in enumerate(self.company_data["locations"], 1):
            locations_text += f"{i}. {location['name']} branch in {location['area']}\n"
            locations_text += f"   Address: {location['address']}\n\n"
        
        return locations_text

    def generate_services_info(self) -> str:
        """Generate formatted service information for the OpenAI prompt"""
        services_text = "Anthill IQ offers the following services:\n\n"
        
        for i, service in enumerate(self.company_data["services"], 1):
            services_text += f"{i}. {service['name']}\n"
            services_text += f"   {service['description']}\n\n"
        
        return services_text

    def handle_welcome_message(self) -> Dict:
        """Handle the welcome message"""
        welcome_message = self.company_data["welcome_message"]
        return {
            "response": welcome_message,
            "source": "welcome",
            "confidence": 1.0
        }

    async def handle_message(self, message: str, user_id: Optional[str] = None) -> Dict:
        """Handle user messages and generate responses using OpenAI"""
        
        # Handle welcome message
        if message.lower() == "welcome":
            result = self.handle_welcome_message()
            return result
        
        # Prepare system prompt with company data
        system_prompt = f"""You are an AI assistant for Anthill IQ, a premium workspace provider in Bangalore, India. You are friendly, empathetic, and conversational.

Location Information:
{self.generate_locations_info()}

Services Information:
{self.generate_services_info()}

Contact Information:
Phone: {self.company_data["contact"]["phone"]}
Email: {self.company_data["contact"]["email"]}
Website: {self.company_data["contact"]["website"]}

Pricing Information:
{self.company_data["pricing_message"]}

Conversation Guidelines:
1. Keep responses brief and focused - only answer what was specifically asked
2. Do not provide all company information at once unless explicitly requested
3. Use natural language and avoid templated or robotic responses
4. Avoid keyword matching - understand the context of questions
5. Use emojis thoughtfully to make the conversation more engaging 😊
6. For pricing inquiries, provide contact information
7. Treat each question uniquely - avoid generic responses
8. NEVER mention or suggest booking - this is an information-only chatbot
9. If users ask about booking, politely direct them to contact the team via phone or email

Examples of Good Responses:
User: "Tell me about your training room"
Assistant: "Our training rooms feature interactive presentation tools and flexible configurations for various group sizes. They come with technical support and catering options. For specific details and pricing, please contact us at +91 9119739119 or connect@anthilliq.com 📞"

User: "What are your locations?"
Assistant: "We have four locations across Bangalore - Cunningham Road (Central), Arekere (South), Hulimavu (South), and Hebbal (North). Which area interests you?"

Remember to:
- Keep responses conversational and natural
- Avoid templated or repetitive responses
- Provide relevant information without overwhelming
- Focus on informing rather than selling
- Never suggest or process bookings
- Direct booking inquiries to contact the team directly
"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Get response from OpenAI
            response = completion.choices[0].message.content
            
            result = {
                "response": response,
                "source": "openai",
                "confidence": 0.9
            }
            
            return result
            
        except Exception as e:
            error_message = f"Error generating response: {str(e)}"
            print(error_message)
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again or contact us directly at +91 9119739119 or connect@anthilliq.com",
                "source": "error",
                "confidence": 0.0
        } 