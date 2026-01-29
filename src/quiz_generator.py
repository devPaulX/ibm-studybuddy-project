import random

def generate_quiz(summary_text: str):
    """
    Generate multiple-choice quiz questions from summary text.
    Each question has 1 correct answer and 3 distractors.
    """
    if not summary_text:
        return []

    sentences = [s.strip() for s in summary_text.split('.') if s.strip()]
    questions = []

    for i, sentence in enumerate(sentences, 1):
        correct = sentence
        distractors = random.sample([s for s in sentences if s != correct], min(3, len(sentences)-1))
        options = [correct] + distractors
        random.shuffle(options)

        # Build a concept-driven question
        if " is " in sentence:
            concept = sentence.split(" is ")[0].strip()
            q_text = f"Q{i}: What best describes {concept}?"
        elif " provides " in sentence:
            concept = sentence.split(" provides ")[0].strip()
            q_text = f"Q{i}: What does {concept} provide?"
        else:
            q_text = f"Q{i}: Which statement is correct?"

        questions.append({
            "question": q_text,
            "options": options,
            "answer": correct
        })

    return questions