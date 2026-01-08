from transformers import pipeline

multilingual_model = pipeline(
    "text-classification",
    model="xlm-roberta-base",
    return_all_score= True
)

def analyze_text_multilingual(text: str):
    return multilingual_model(text)
