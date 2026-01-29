import os
import requests
import re
import time
import sys

# ANALOGY: The "GPS Coordinator" (Ensures the app always knows where it is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

def safe_decode(text):
    # ANALOGY: The "Universal Sanitizer" (Scrubs out the weird characters that cause gibberish)
    if not text: return ""
    # Remove non-printable characters and mathematical "loop" symbols
    text = re.sub(r'[^\x20-\x7E]+', ' ', text)
    return ' '.join(text.split())

def summarize_with_groq(text, user_key, system_prompt=None):
    api_key = os.getenv("GROQ_API_KEY") or user_key
    if not api_key: return "⚠️ Missing API Key."
    
    clean_text = safe_decode(text)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt or "Provide a comprehensive, detailed summary. Use multiple sections with bold headers, bullet points for key technical details, and a 'Final Takeaway' paragraph at the end."},
            {"role": "user", "content": clean_text[:7000]} # Increased context window
        ],
        "temperature": 0.3 # Lower temperature = less "gibberish" hallucination
    }
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Groq Error: {str(e)}"

# ... (Keep all your existing imports and Groq code at the top)

def summarize_document(file_path, api_provider, user_key=None):
    from ingestion import extract_text_from_pdf, extract_text_from_txt
    actual_path = file_path.name if hasattr(file_path, 'name') else file_path
    raw_text = extract_text_from_pdf(actual_path) if actual_path.lower().endswith(".pdf") else extract_text_from_txt(actual_path)
    
    if not raw_text.strip(): return "❌ Error: Empty file."
    
    if str(api_provider).lower() == "local":
        try:
            from transformers import pipeline
            # ANALOGY: The "Strict Editor" (Stops the AI from repeating itself)
            summarizer = pipeline("text-generation", model="distilgpt2")
            
            clean_input = safe_decode(raw_text)[:600]
            prompt = f"Summarize these notes concisely:\n{clean_input}\n\nSummary:"
            
            # Added repetition_penalty to stop the loops and do_sample=True for variety
            res = summarizer(prompt, 
                             max_new_tokens=80, 
                             do_sample=True, 
                             temperature=0.7, 
                             repetition_penalty=1.5, 
                             pad_token_id=50256)
            
            generated = res[0]['generated_text']
            summary_output = generated.split("Summary:")[-1].strip()
            
            return f"### 📍 Local Summary (Lite Mode)\n{summary_output}"
        except Exception as e:
            return f"❌ Local Error: {str(e)}"

    return summarize_with_groq(raw_text, user_key)