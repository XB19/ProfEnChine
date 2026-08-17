import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# llama-3.3-70b-versatile a été retiré du catalogue Groq (modèle
# déprécié) ; openai/gpt-oss-120b est le modèle généraliste recommandé
# en remplacement (cf. https://console.groq.com/docs/models).
MODEL = "openai/gpt-oss-120b"

if GROQ_API_KEY:
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
else:
    client = None