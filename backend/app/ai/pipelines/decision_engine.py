def decide_text(results):
    model_version = "xlm-roberta-base-toxic-v1"

    decision = (
        "blocked"
        if any(r["score"] > 0.85 for r in results)
        else "approved"
    )

    return decision, model_version
