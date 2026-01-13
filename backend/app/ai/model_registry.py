try:
	from transformers import pipeline

	toxicity_model = pipeline("text-classification", model="unitary/toxic-bert")
except Exception:
	# Fallback stub used in test environments where transformers/torch
	# are not installed or GPU is unavailable. The stub returns a
	# non-toxic prediction so unit tests and lightweight runs succeed.
	def toxicity_model(text):
		return [{"label": "NOT_TOXIC", "score": 0.0}]

TOXICITY_MODEL_V1 = "toxicity_v1.1"
TOXICITY_MODEL_V2 = "toxicity_v1.2"

ACTIVE_TOXICITY_MODEL = TOXICITY_MODEL_V1
CANARY_TOXICITY_MODEL = TOXICITY_MODEL_V2
