from app.ai.pipelines.decision_engine import decide_text

def test_decision_blocked():
    results = [{"label": "toxicity", "score": 0.95}]
    assert decide_text(results) == "blocked"

def test_decision_flagged():
    results = [{"label": "toxicity", "score": 0.8}]
    assert decide_text(results) == "flagged"

def test_decision_approved():
    assert decide_text([]) == "approved"
