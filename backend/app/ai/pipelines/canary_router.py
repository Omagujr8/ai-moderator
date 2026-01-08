import random
from app.ai.model_registry import (
    ACTIVE_TOXICITY_MODEL,
    CANARY_TOXICITY_MODEL
)

CANARY_PERCENTAGE = 10  # 10%

def select_model():
    if random.randint(1, 100) <= CANARY_PERCENTAGE:
        return CANARY_TOXICITY_MODEL
    return ACTIVE_TOXICITY_MODEL
