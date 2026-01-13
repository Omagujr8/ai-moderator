try:
    from langdetect import detect

    def detect_language(text: str) -> str:
        try:
            return detect(text)
        except Exception:
            return "unknown"
except Exception:
    # Fallback stub for environments without langdetect
    def detect_language(text: str) -> str:
        return "unknown"
