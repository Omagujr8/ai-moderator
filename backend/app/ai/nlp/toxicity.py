# from transformers import pipeline
#
# toxicity_classifier = pipeline("text-classification",
#                                model= "unitary/toxic-bert",
#                                top_k=None)

# def analyse_text(text:str):
#     results = toxicity_classifier(text)
#     flagged = []
#
#     for item in results[0]:
#         if item ['score'] > 0.7 :
#             flagged.append({
#                 'label': item['label'],
#                 'score': item['score']})
#
#     return flagged
from app.ai.model_registry import ACTIVE_TOXICITY_MODEL

def analyze_text(text: str):
    model_version = select_model()

    if model_version == "toxicity_v1.2":
        results = new_classifier(text)
    else:
        results = old_classifier(text)

    return {
        "results": results,
        "model_version": model_version
    }