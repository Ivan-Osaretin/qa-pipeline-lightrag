"""
PHASE 4 - MULTI-MODEL CLIENT (DEFINITIVE VERSION)
Supports Groq (Llama), Google (Gemini), and Cohere (Command R+).
Includes safety delays to protect free-tier rate limits.
"""
import os
import time
from dotenv import load_dotenv
from loguru import logger

# Provider Libraries
from groq import Groq
import google.generativeai as genai
import cohere

load_dotenv()

class LLMClient:
    def __init__(self, provider="groq"):
        self.provider = provider
        try:
            if provider == "groq":
                self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                self.model = "llama-3.3-70b-versatile"
            
            elif provider == "gemini":
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                # Fixed: Standard model identifier for Google AI Studio
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            elif provider == "cohere":
                self.client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
                # Fixed: Specific versioned identifier to avoid the 'removed' error
                self.model = "command-r-plus-08-2024"
            
            logger.info(f"✅ {provider.upper()} Client initialized.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize {provider}: {e}")

    def generate_answer(self, system_prompt, user_prompt):
        # Professional standard: 5-second delay to protect your free token limits
        time.sleep(5)
        
        try:
            if self.provider == "gemini":
                # Google Gemini Logic: Merging prompts for the simplest interface
                full_prompt = f"INSTRUCTIONS: {system_prompt}\n\nQUESTION: {user_prompt}"
                response = self.model.generate_content(full_prompt)
                return response.text
            
            elif self.provider == "cohere":
                # Cohere Logic
                response = self.client.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.message.content[0].text
            
            else: 
                # Groq (Llama-3.3) Logic
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ {self.provider.upper()} API Error: {e}")
            return "ERROR: API limit or connection issue."