import os
from dotenv import load_dotenv

# Load environment variables
print("Loading .env file...")
load_dotenv()

# Check each variable
variables = [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN", 
    "TWILIO_PHONE_NUMBER",
    "OPENAI_API_KEY"
]

print("\nChecking environment variables:")
print("="*50)

for var in variables:
    value = os.getenv(var)
    if value:
        # Hide sensitive parts
        if len(value) > 10:
            masked = value[:8] + "..." + value[-4:]
        else:
            masked = value[:3] + "..."
        print(f"✅ {var}: {masked} (length: {len(value)})")
    else:
        print(f"❌ {var}: NOT FOUND")

print("\n" + "="*50)

# Test if we can create OpenAI client
try:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    print("✅ OpenAI client created successfully!")
except Exception as e:
    print(f"❌ OpenAI client failed: {e}")