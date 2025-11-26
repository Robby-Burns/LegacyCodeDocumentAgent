import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test 1: Check if dotenv is working
print("✅ python-dotenv is installed and working!")

# Test 2: Check if we can read our config
model = os.getenv("DEFAULT_MODEL")
print(f"✅ DEFAULT_MODEL loaded: {model}")

# Test 3: Check if API key exists (don't print the actual key!)
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key and openai_key != "your-key-here":
    print(f"✅ OPENAI_API_KEY loaded: {openai_key[:8]}...hidden")
else:
    print("⚠️  OPENAI_API_KEY not set or still placeholder")

# Test 4: Check if litellm is installed
import litellm
print("✅ litellm is installed and ready!")

print("\n🎉 Environment setup complete! You're ready for Step 2.")