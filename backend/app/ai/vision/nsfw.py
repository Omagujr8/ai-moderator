from nudenet import NudeDetector

classifier = NudeDetector()

def analyze_image(image_path: str):
    result = detector.detect(image_path)
    score = list(result.values())[0]

    for item in result:
        if item["score"] > 0.7 and item["class"] in ["EXPOSED_GENITALIA", "EXPOSED_BREAST_F"]:
            return {
                "label": "nsfw",
                "score": item["unsafe"]
            }
    return None
