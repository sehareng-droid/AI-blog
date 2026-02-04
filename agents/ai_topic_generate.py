import json
from groq import Groq
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")

with open(CONFIG_PATH) as f:
    config = json.load(f)

client = Groq(api_key=config["groq_api_key"])
MODEL = config["model"]

def generate_daily_topic(n=1):
    prompt = f"""
    Suggest {n} unique AI tools or automation topics
    focused on business, productivity, or agents.
    Return ONLY a JSON array of strings.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return json.loads(response.choices[0].message.content)
