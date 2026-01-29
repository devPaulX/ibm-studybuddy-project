def generate_flashcards(summary_text: str):
    """
    Generate concept-driven flashcards from summary text.
    Each card is a Q&A pair: question first, answer revealed interactively.
    """
    if not summary_text:
        return []

    flashcards = []
    # Split into concepts instead of raw sentences
    sentences = [s.strip() for s in summary_text.split('.') if s.strip()]
    for i, sentence in enumerate(sentences, 1):
        # Simple heuristic: turn definition/feature into a question
        if " is " in sentence:
            concept, definition = sentence.split(" is ", 1)
            question = f"What is {concept.strip()}?"
            answer = definition.strip()
        elif " provides " in sentence:
            concept, feature = sentence.split(" provides ", 1)
            question = f"What does {concept.strip()} provide?"
            answer = feature.strip()
        else:
            question = f"What is the key idea in point {i}?"
            answer = sentence

        flashcards.append({"question": question, "answer": answer})

    return flashcards