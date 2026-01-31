import os
import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = None
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    try:
        # Try to initialize with different approaches
        import httpx
        
        # Create a custom httpx client without proxies parameter
        http_client = httpx.Client()
        client = Groq(api_key=api_key, http_client=http_client)
    except Exception as e:
        try:
            # Fallback: try direct initialization
            client = Groq(api_key=api_key)
        except Exception as e2:
            print(f"Warning: Could not initialize Groq client: {e2}")
            client = None
else:
    print("Warning: GROQ_API_KEY not found in environment variables")


def generate_response(prompt):
    """
    Generate a response using Groq's API with LLaMA model.
    
    Args:
        prompt (str): The prompt to send to the AI model
        
    Returns:
        str: The generated response from the AI model
    """
    if not client:
        raise Exception("Groq client not initialized. Please check your API key in the .env file.")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional business intelligence AI assistant specializing in marketing, sales, and lead qualification. Provide detailed, actionable insights in a clear and structured format."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")
