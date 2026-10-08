from dotenv import load_dotenv; load_dotenv()
import os, json, pathlib
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

resp = client.chat.completions.create(
    model='openai/gpt-oss-20b',
    messages=[{'role': 'user', 'content': 'Translate "What is the capital of Rajasthan?" into Hindi (Devanagari) and Hinglish. Output JSON only in format: {"hindi": "...", "hinglish": "..."}'}],
    temperature=0.3,
    max_tokens=300,
)
content = resp.choices[0].message.content or ""
pathlib.Path('debug_response.txt').write_text(content, encoding='utf-8')
print("Successfully received response:")
print(content)
