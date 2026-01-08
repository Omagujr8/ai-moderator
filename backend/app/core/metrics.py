from prometheus_client import Counter, Histogram

moderation_requests_total = Counter(
    'moderation_requests_total',
    'Total number of moderation requests',
)

moderation_decisions_total = Counter(
    'moderation_decisions_total',
    'Moderation decisions',
    ['decision']
)

moderation_duration_seconds = Histogram(
    'moderation_duration_seconds',
    'Time spent moderating content'
)