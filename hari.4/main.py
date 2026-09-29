"""
main.py
-------
EduGenie: Google Gemini Powered Learning Assistant
FastAPI backend that routes user requests to the right module:
explanation, Q&A, quiz generation, summarization, and learning paths.

Run locally with:
    uvicorn main:app --reload
Then navigate to:
    http://127.0.0.1:8000
"""

from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie", description="Google Gemini Powered Learning Assistant")

# Static files (CSS) and HTML templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------------------------------------------------
# Q&A - GET API using Gemini
# ---------------------------------------------------------------------
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# ---------------------------------------------------------------------
# Explanation - POST API using LaMini-Flan-T5 (local)
# ---------------------------------------------------------------------
@app.post("/explain/")
async def explain_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}


# ---------------------------------------------------------------------
# Summarization - POST API using Gemini
# ---------------------------------------------------------------------
@app.post("/summarize/")
async def summarize_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}


# ---------------------------------------------------------------------
# Quiz Generation - POST API using Gemini
# ---------------------------------------------------------------------
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    return JSONResponse(content={"quiz": quiz})


# ---------------------------------------------------------------------
# Learning Recommendations - GET API using Gemini
# ---------------------------------------------------------------------
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}
