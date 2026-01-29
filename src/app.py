import gradio as gr
import os
import sys
import re
from PyPDF2 import PdfReader

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import summarizer_hybrid as sh

def check_and_summarize(file, mode, key):
    if file is None:
        return "⚠️ Please upload a file first."
    
    file_size_mb = os.path.getsize(file.name) / (1024 * 1024)
    
    # 1. ENFORCE FILE SIZE (For Local Only)
    if mode == "local" and file_size_mb > 5:
        return f"❌ Local Engine Limit: {file_size_mb:.1f}MB is too large. Use 'groq' for files over 5MB."
    
    # 2. ENFORCE PAGE LIMIT (For Local Only)
    if mode == "local" and file.name.lower().endswith(".pdf"):
        reader = PdfReader(file.name)
        page_count = len(reader.pages)
        if page_count > 15:
            return f"❌ Local Engine Limit: {page_count} pages is too many. Use 'groq' for documents over 15 pages."
        
    return sh.summarize_document(file, mode, key)

def generate_cards(summary, api_key):
    # SAFETY CHECK: Prevent the "Red Error Boxes" in Study Deck
    if not summary or "❌" in summary or "⚠️" in summary or "Ready" in summary:
        return "N/A", "Please generate a successful summary first.", [], gr.update(maximum=0)
    
    prompt = "Create 10 flashcards. Format exactly as: Q: [Question] A: [Answer]"
    raw_data = sh.summarize_with_groq(summary, api_key, system_prompt=prompt)
    
    # Robust search for Q&A pairs
    cards = re.findall(r"Q:\s*(.*?)\s*A:\s*(.*)", raw_data, re.I)
    
    if not cards:
        return "Empty", "AI didn't format cards correctly. Try again!", [], gr.update(maximum=0)
    
    return cards[0][0], cards[0][1], cards, gr.update(maximum=len(cards)-1, value=0)

# UI Code remains the same, just calling the new 'check_and_summarize'
with gr.Blocks() as demo:
    gr.Markdown("# 📚 IBM-AICTE StudyBuddy: Pro Version")
    card_state = gr.State([])

    with gr.Row():
        with gr.Column(scale=1):
            file_in = gr.File(label="📂 PDF")
            mode = gr.Dropdown(["groq", "local"], label="Engine", value="groq")
            key_in = gr.Textbox(label="🔑 API Key", type="password")
            sum_btn = gr.Button("🚀 Summarize", variant="primary")
            quiz_btn = gr.Button("🪄 Make 10 Flashcards", visible=False)
        
        with gr.Column(scale=2):
            with gr.Tabs() as tabs:
                with gr.TabItem("🧠 Summary", id=0):
                    output = gr.Markdown("Ready...")
                with gr.TabItem("🗂️ Study Deck", id=1):
                    slider = gr.Slider(0, 9, step=1, label="Card #")
                    q_box = gr.Textbox(label="Question", interactive=False)
                    a_box = gr.Textbox(label="Answer", interactive=False)

    sum_btn.click(check_and_summarize, [file_in, mode, key_in], output, show_progress="full").then(
        lambda m: gr.update(visible=True) if "❌" not in m and "⚠️" not in m else gr.update(visible=False), 
        [output], quiz_btn
    )
    
    quiz_btn.click(generate_cards, [output, key_in], [q_box, a_box, card_state, slider], show_progress="full").then(
        lambda: gr.update(selected=1), None, tabs
    )
    
    slider.change(lambda i, c: (c[int(i)][0], c[int(i)][1]) if c else ("",""), [slider, card_state], [q_box, a_box])

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft()) # type: ignore