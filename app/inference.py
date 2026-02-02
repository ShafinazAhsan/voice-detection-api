import random

def predict_voice(language: str):
    # MOCK LOGIC — will be replaced by ML later
    is_ai = random.choice([True, False])

    return {
        "classification": "AI_GENERATED" if is_ai else "HUMAN_GENERATED",
        "confidence": round(random.uniform(0.75, 0.95), 2),
        "language": language,
        "explanation": "Mock prediction based on placeholder logic"
    }
