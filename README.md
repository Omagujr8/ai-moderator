## 🚀 Features

- **Text Moderation**
  - Detects:
    - Toxicity
    - Hate speech
    - Offensive language
    - Personally Identifiable Information (PII)
  - Supports **multiple languages**
  - Fast and optimized: model loads once at startup
  - Circuit breaker for handling model failures gracefully

- **Image & Video Moderation**
  - NSFW detection for images
  - Frame-by-frame video analysis for inappropriate content

- **API-first Design**
  - FastAPI-based REST API
  - Async endpoints for low-latency responses
  - Health checks and graceful shutdown support

- **Background Processing**
  - Celery workers for asynchronous AI model tasks
  - Optimized for throughput and stability

- **Rate Limiting & Cost-based Throttling**
  - Limits heavy requests
  - Protects system and reduces latency

- **Stability & Failure Handling**
  - Circuit breaker: auto-approve content if AI model fails
  - Logging & monitoring ready
  - Graceful shutdown to safely release resources

- **Performance Optimizations**
  - Models load once at startup
  - Async I/O where needed
  - Celery tuned for concurrency and prefetching
