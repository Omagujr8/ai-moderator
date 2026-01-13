try:
    from nudenet import NudeDetector

    _detector = NudeDetector()

    def analyze_image(image_path: str):
        result = _detector.detect(image_path)
        # Normalize and return first detection if above threshold
        for item in result:
            if item.get("score", 0) > 0.7 and item.get("class") in ["EXPOSED_GENITALIA", "EXPOSED_BREAST_F"]:
                return {"label": "nsfw", "score": item.get("score")}
        return None
except Exception:
    # Fallback stub for test/dev environments without nudenet
    def analyze_image(image_path: str):
        return None
