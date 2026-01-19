import os
from groq import Groq
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class GroqClient:
    def __init__(self, model: str = 'llama-3.3-70b-versatile'):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError('❌ GROQ_API_KEY not found in .env')
        self.client = Groq(api_key=self.api_key)
        self.model = model
        logger.info(f'✅ Groq Client ready: {model}')

    def generate_answer(self, system_prompt: str, user_prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                temperature=0.1,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f'Groq Error: {e}')
            return 'ERROR: API failure.'
