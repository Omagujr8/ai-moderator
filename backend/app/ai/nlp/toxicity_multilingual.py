from transformers import pipeline

_model = None

def get_model():
    global _model
    if _model is None:
        _model = pipeline(
            "text-classification",
            model="xlm-roberta-base",
            return_all_scores=True
        )
    return _model


def analyze_text_multilingual(text: str):
    model = get_model()
    return model(text)
