"""
learning_path.py
-----------------
Generates a personalized, structured learning path for a given topic
using Gemini 1.5 Pro: beginner -> intermediate -> advanced, with
timelines and resource suggestions.
"""

import os
import traceback
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (videos, articles, or books).
Include beginner, intermediate, and advanced levels if needed.
"""
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "parts") and response.parts:
            return response.parts[0].text
        else:
            return "❌ Could not extract content from Gemini response."
    except Exception as e:
        traceback.print_exc()  # full error trace for debugging
        return f"❌ Error occurred: {str(e)}"
