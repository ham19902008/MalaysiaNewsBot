import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize(text):
    try:
        prompt = f"Summarize this news article in 1-2 sentences:\n\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=100,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Summary unavailable."
