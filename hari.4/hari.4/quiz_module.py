"""
quiz_module.py
--------------
Generates 3 multiple-choice questions (4 options each) from a passage,
using Gemini 1.5 Pro. Output is parsed into a Python list of dicts.
"""

import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def clean_json_block(text: str) -> str:
    """Remove Markdown ```json code fences if present."""
    return re.sub(r"```(?:json)?\n(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

        prompt = f"""
You are a quiz generator.

From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""
        response = model.generate_content(prompt)
        quiz_text = response.text.strip()

        # Clean markdown code blocks if any
        cleaned_text = clean_json_block(quiz_text)

        quiz = json.loads(cleaned_text)
        return quiz
    except Exception as e:
        return [{"error": f"⚠ Error in Quiz generation: {e}"}]
