import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twilio.rest import Client
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class TwilioAgent:
    def __init__(self):
        # Initialize Twilio
        self.twilio_client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
        

        self.llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        print("✅ Twilio Agent initialized successfully!")
    
    def is_late_night_call(self, call_time):
        """Check if call was made between 2 AM and 8 AM"""
        hour = call_time.hour
        return 2 <= hour < 8
    
    def generate_response_message(self, caller_name, call_time):
        """Generate AI response for late night caller"""
        prompt = f"""
        Someone named {caller_name} called me at {call_time.strftime('%I:%M %p')} on {call_time.strftime('%B %d, %Y')}.
        
        Generate a polite but firm SMS message that:
        1. Explains I don't take calls after 2 AM
        2. Offers to schedule a meeting during business hours (9 AM - 6 PM)
        3. Asks them to reply with their email and preferred meeting time
        4. Keep it under 160 characters for SMS
        
        Make it professional but friendly.
        """
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def send_sms(self, to_number, message):
        """Send SMS via Twilio"""
        try:
            message = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_number,
                to=to_number
            )
            return f"✅ SMS sent successfully! Message SID: {message.sid}"
        except Exception as e:
            return f"❌ Failed to send SMS: {str(e)}"
    
    def handle_late_night_call(self, caller_number, caller_name=None, call_time=None):
        """Main function to handle a late night call"""
        
        # Use current time if not provided
        if call_time is None:
            call_time = datetime.now()
        
        if caller_name is None:
            caller_name = "Unknown Caller"
        
        print(f"\n📞 Processing call from {caller_name} ({caller_number}) at {call_time}")
        
        # Check if it's a late night call
        if not self.is_late_night_call(call_time):
            print("⏰ Call was during normal hours, no action needed.")
            return
        
        print("🌙 Late night call detected! Generating response...")
        
        # Generate AI response
        response_message = self.generate_response_message(caller_name, call_time)
        print(f"🤖 Generated message: {response_message}")
        
        # Send SMS
        result = self.send_sms(caller_number, response_message)
        print(f"📱 {result}")
        
        return {
            "call_time": call_time,
            "caller": caller_name,
            "message_sent": response_message,
            "sms_result": result
        }

def test_agent():
    """Test the agent with sample data"""
    agent = TwilioAgent()
    
    test_time = datetime.now().replace(hour=11, minute=42)
    
    
    test_number = "+447456238582"  
    
    result = agent.handle_late_night_call(
        caller_number=test_number,
        caller_name="Test Caller",
        call_time=test_time
    )
    
    print("\n" + "="*50)
    print("TEST COMPLETED")
    print("="*50)
    
def force_test_agent():
    """Force test - always sends SMS regardless of time"""
    print("🚀 Starting FORCE TEST (always sends SMS)...")
    
    agent = TwilioAgent()
    
    # Current time (any time)
    test_time = datetime.now()
    test_number = "+447456238582"  # Your Twilio number
    
    print(f"\n📞 FORCE TEST: Processing call at {test_time}")
    print("🌙 Forcing SMS send for testing...")
    
    # Generate AI response (skip time check)
    response_message = agent.generate_response_message("Test Caller", test_time)
    print(f"🤖 Generated message: {response_message}")
    
    # Send SMS
    result = agent.send_sms(test_number, response_message)
    print(f"📱 {result}")
    
    print("\n" + "="*50)
    print("FORCE TEST COMPLETED - SMS SHOULD BE SENT")
    print("="*50)

if __name__ == "__main__":
    print("🚀 Starting Twilio Agent...")
    
    # Test the basic functionality
    force_test_agent()