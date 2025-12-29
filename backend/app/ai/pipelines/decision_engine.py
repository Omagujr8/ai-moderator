def decide_text(results):
    if not results:
        return "approved"

    max_score =  max(r['score'] for r in results)

    if max_score > 0.9 :
        return "blocked"

    return "flagged"

