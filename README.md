
# 📚 IBM-AICTE Student Project: StudyBuddy Pro Version

An AI-powered document summarizer and study tool featuring a **Hybrid Inference Engine**.

## 🚀 Key Features
- **Cloud Engine (Groq):** High-speed, comprehensive summarization using Llama-3.1 for large documents.
- **Local Engine (Edge-Optimized):** Privacy-focused, local inference using `distilgpt2` for machines with limited hardware.
- **Auto-Flashcards:** Generates a 10-card study deck automatically from any summary.
- **Smart Logic:** Automatically enforces file size (5MB) and page limits (15 pages) for local stability.

## 🛠️ Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python -m src.app`

## 🛠️ Folder Structure
```
ibm-studybuddy-project/
├── requirements.txt         # The "Toolbox" list
├── README.md                # The "Billboard" description
└── src/                     # The "Engine" folder 
    ├── __init__.py          # (Empty file) Tells Python this is a package
    ├── app.py                   # The main UI (The "Face" of the app)
    ├── ingestion.py         # 📄 INGESTION: Handles PDF/Text extraction
    └── summarizer_hybrid.py # 🧠 AI LOGIC: Handles Groq, Local, & Flashcard prompts
```
