# EduGenie: Google Gemini Powered Learning Assistant

A lightweight AI-powered educational assistant. Ask questions, get concept
explanations, generate quizzes, summarize passages, and get personalized
learning paths.

## Folder structure
```
hari.4/
├── main.py                # FastAPI app
├── explanation_module.py  # Concept explanation logic (local LaMini-Flan-T5)
├── qna.py                 # Question answering (Gemini)
├── quiz_module.py         # Quiz generation (Gemini)
├── summary_module.py      # Summarization (Gemini)
├── learning_path.py       # Learning recommendations (Gemini)
├── templates/index.html   # HTML frontend
├── static/style.css       # Styling
├── requirements.txt       # Python dependencies
├── .env.example            # Sample env file for your Gemini API key
└── README.md
```

## Pre-requisites
- Python 3.10+
- A Google Gemini API key (from [Google AI Studio](https://aistudio.google.com))

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add your Gemini API key:
   ```
   cp .env.example .env
   # then edit .env and paste your key after GEMINI_API_KEY=
   ```

## Run locally
```
uvicorn main:app --reload
```
Then open: http://127.0.0.1:8000

## Endpoints
| Endpoint                    | Method | Purpose                         |
|------------------------------|--------|----------------------------------|
| `/qa?question=...`           | GET    | Ask a question                  |
| `/explain/`                  | POST   | `{ "topic": "..." }`            |
| `/summarize/`                | POST   | `{ "text": "..." }`             |
| `/quiz`                      | POST   | `{ "text": "..." }`             |
| `/learn/recommendations?topic=...` | GET | Personalized learning path |

## Notes
- The Explanation module downloads `MBZUAI/LaMini-Flan-T5-783M` the first
  time it runs (via `transformers`/`torch`), so the first request will be
  slower while the model is fetched and cached.
- All other modules (Q&A, quiz, summary, learning path) call Gemini 1.5 Pro
  and require `GEMINI_API_KEY` to be set.
