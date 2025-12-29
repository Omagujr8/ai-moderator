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

def analyze_text(text: str):
    # Temporary stub (no transformers yet)
    return {
        "toxicity": 0.1,
        "hate": 0.0,
        "sexual": 0.0
    }