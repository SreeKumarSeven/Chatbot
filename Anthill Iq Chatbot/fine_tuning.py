from openai import OpenAI
import os
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FineTuningManager:
    """Manager class for working with fine-tuned models"""
    
    def __init__(self):
        """Initialize the fine-tuning manager"""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please check your .env file.")
        
        self.client = OpenAI(api_key=openai_api_key)
        
        # Get the fine-tuned model ID from environment variables
        self.fine_tuned_model_id = os.getenv("FINE_TUNED_MODEL_ID")
        if not self.fine_tuned_model_id:
            print("WARNING: FINE_TUNED_MODEL_ID environment variable is not set. Falling back to default model.")
            self.fine_tuned_model_id = "gpt-3.5-turbo"  # Fallback to standard model
        
    def use_fine_tuned_model(self, message: str) -> str:
        """
        Use the fine-tuned model to generate a response to the user's message
        
        Args:
            message: The user's message
            
        Returns:
            The model's response as a string
        """
        try:
            # Create system message for Anthill IQ context with explicit location information
            system_message = """You are the voice assistant for Anthill IQ, a premium coworking space brand in Bangalore. 
            Your personality is friendly, professional, and helpful, reflecting Anthill IQ's welcoming and modern brand. 
            Always provide clear, accurate information about Anthill IQ's workspaces, amenities, locations, and policies.
            
            ANTHILL IQ SERVICES:
            Anthill IQ offers the following services at all three locations:
            1. Private Office Space - Dedicated private offices for teams
            2. Coworking Space - Flexible shared workspace for professionals
            3. Dedicated Desk - Reserved desk in a shared environment
            4. Meeting Rooms - Professional spaces for client meetings and team discussions
            5. Event Spaces - Versatile venues for hosting corporate and networking events
            6. Training Rooms - Equipped spaces for workshops and training sessions
            
            IMPORTANT LOCATION INFORMATION: Anthill IQ has ONLY THREE locations in Bangalore:
            1. Cunningham Road branch in Central Bangalore (Vasanth Nagar area)
               Address: 1st Floor, Anthill IQ, 20, Cunningham Rd, Vasanth Nagar, Bengaluru, Karnataka 560052
               Directions: https://www.google.com/maps/place/Anthill+IQ+Workspace+%7C+Cunningham+Road/@12.9849734,77.5943513,17z/data=!3m1!4b1!4m6!3m5!1s0x3bae17f87a1d01e3:0x480934306048f237!8m2!3d12.9849682!4d77.5969262!16s%2Fg%2F11vzbym77s
               
            2. Hulimavu branch on Bannerghatta Road in South Bangalore
               Address: 75/B Windsor F4, Bannerghatta Rd, opp. Christ University, Hulimavu, Bengaluru, Karnataka 560076
               Directions: https://www.google.com/maps/place/Anthill+IQ+Workspace+%7C+Hulimavu/@12.8792585,77.5927543,17z/data=!3m1!4b1!4m6!3m5!1s0x3bae15bc7901af15:0x4d1de3a903e7e183!8m2!3d12.8792533!4d77.5953292!16s%2Fg%2F11t4fzly_6
               
            3. Arekere branch on Bannerghatta Road in South Bangalore
               Address: 224, Bannerghatta Rd, near Arekere, Gate, Arekere, Bengaluru, Karnataka 560076
               Directions: https://www.google.com/maps/place/Anthill+IQ+Workspace+%7C+Arekere/@12.8887504,77.5922544,17z/data=!3m1!4b1!4m6!3m5!1s0x3bae15078f1d606b:0xef4dc17e7086a654!8m2!3d12.8887452!4d77.5971253!16s%2Fg%2F11j6g_65mr
            
            CONTACT INFORMATION: Anthill IQ has ONE contact number only: +91 81810 00060
            Email: connect@anthilliq.com
            Website: www.anthilliq.com
            
            BOOKING INFORMATION:
            When someone expresses interest in booking a service, ask for:
            - Their name
            - Phone number
            - Email address
            - Preferred location (Cunningham Road, Hulimavu, or Arekere)
            - Desired service (Private Office, Coworking, Dedicated Desk, Meeting Room, Event Space, or Training Room)
            - Preferred date and time
            
            DO NOT assume someone wants to book just because they're asking about services. Only start the booking process if they explicitly request a booking or reservation.
            
            RESPONSE FORMAT: Present information in a structured, organized way:
            - Use numbered lists for steps or multiple items
            - Use bullet points for features or amenities
            - Add line breaks between paragraphs for readability
            - Keep responses concise but complete
            - When providing location information, use a simple format with address followed by directions link
            
            DO NOT mention or confirm any BTM Layout location - this is incorrect information.
            If asked about BTM Layout, clarify that Anthill IQ does not have a branch there.
            
            Never provide information about competitors or other coworking spaces - only discuss Anthill IQ. 
            When discussing pricing, never mention specific prices - instead encourage users to contact Anthill IQ directly.
            If a question requires human expertise, propose to connect them with a human team member."""
            
            # Call the OpenAI API with the fine-tuned model
            response = self.client.chat.completions.create(
                model=self.fine_tuned_model_id,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract the assistant's message content
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error using fine-tuned model: {str(e)}")
            raise
            
    def list_fine_tuned_models(self) -> List[Dict]:
        """
        List all fine-tuned models available to the API key
        
        Returns:
            A list of model information dictionaries
        """
        try:
            models = self.client.models.list()
            # Filter for fine-tuned models only
            fine_tuned_models = [model for model in models.data if "ft:" in model.id]
            return fine_tuned_models
        except Exception as e:
            print(f"Error listing fine-tuned models: {str(e)}")
            return [] 