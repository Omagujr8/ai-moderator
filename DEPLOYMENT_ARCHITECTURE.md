# Deployment Architecture & Reference

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer / Nginx                    │
│                   (Port 80/443 → 8000)                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┬──────────────┐
        │                     │              │
    ┌───▼────┐           ┌───▼────┐     ┌──▼────┐
    │ API 1  │           │ API 2  │     │ API 3 │  (FastAPI)
    │:8000   │           │:8000   │     │:8000  │
    └───┬────┘           └───┬────┘     └──┬────┘
        │                     │              │
        └─────────────────────┼──────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  PostgreSQL DB    │  (Production DB)
                    │  (Primary/Replica)│
                    └───────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───▼────┐           ┌───▼────┐          ┌────▼──┐
    │ Redis  │           │ Celery │          │Cleanup│
    │ Broker │           │Workers │          │Service│
    └────────┘           └────────┘          └───────┘
        │
        ├──► Task Queue (moderation_queue)
        └──► Result Backend
```

---

## 🐳 Docker Compose Deployment

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: moderation_db
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/moderation_db
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  celery_worker:
    build: ./backend
    command: celery -A app.core.celery worker -l info
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/moderation_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis

volumes:
  pgdata:
  redisdata:
```

---

## ☸️ Kubernetes Deployment

### Deployment Manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-moderator-api
  labels:
    app: ai-moderator

spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-moderator
  
  template:
    metadata:
      labels:
        app: ai-moderator
    
    spec:
      containers:
      - name: api
        image: ai-moderator:1.0.0
        ports:
        - containerPort: 8000
        
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-moderator-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: ai-moderator-secrets
              key: redis-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: ai-moderator-secrets
              key: secret-key
        
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Service Manifest
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-moderator-service

spec:
  type: LoadBalancer
  selector:
    app: ai-moderator
  
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### HPA (Horizontal Pod Autoscaler)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-moderator-hpa

spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-moderator-api
  
  minReplicas: 3
  maxReplicas: 10
  
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 🔍 Monitoring Stack

### Prometheus Configuration
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ai-moderator'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboards

**Dashboard 1: Request Metrics**
- Request rate (req/sec)
- Response time (p50, p95, p99)
- Error rate (%)
- Status code distribution

**Dashboard 2: Worker Metrics**
- Active tasks
- Queue depth
- Task success rate
- Task latency (p50, p95, p99)

**Dashboard 3: System Resources**
- CPU usage (%)
- Memory usage (%)
- Disk I/O
- Network I/O

**Dashboard 4: Application Health**
- Database connection pool
- Redis memory usage
- Rate limiter state
- Worker process count

### Alert Rules
```yaml
groups:
- name: ai-moderator
  rules:
  - alert: HighErrorRate
    expr: |
      (sum(rate(http_requests_total{status=~"5.."}[5m])) /
       sum(rate(http_requests_total[5m]))) > 0.05
    for: 5m
    annotations:
      summary: "High error rate detected"
  
  - alert: WorkerQueueBacklog
    expr: celery_queue_length > 1000
    for: 5m
    annotations:
      summary: "Worker queue backlog growing"
  
  - alert: DatabaseConnectionPoolExhausted
    expr: db_connection_pool_used / db_connection_pool_size > 0.9
    for: 5m
    annotations:
      summary: "Database connection pool near capacity"
```

---

## 📊 Performance Optimization

### Database Optimization
```sql
-- Add indexes for common queries
CREATE INDEX idx_content_external_id ON content(external_id);
CREATE INDEX idx_moderation_result_content_id ON moderation_result(content_id);
CREATE INDEX idx_content_created_at ON content(created_at);

-- Analyze query plans
EXPLAIN ANALYZE SELECT * FROM content WHERE external_id = 'test';
```

### Redis Optimization
```bash
# Monitor Redis performance
redis-cli --stat

# Check slow log
redis-cli slowlog get 10

# Configure maxmemory policy
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### FastAPI Optimization
```python
# Add caching headers
from fastapi.responses import JSONResponse

@app.get("/health")
async def health():
    response = JSONResponse({"api": "ok"})
    response.headers["Cache-Control"] = "no-cache"
    return response

# Add compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 🔐 Security Configuration

### TLS/HTTPS Setup
```nginx
server {
    listen 443 ssl http2;
    server_name api.moderator.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### Security Headers
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### API Rate Limiting (nginx)
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;

location /api/v1/ {
    limit_req zone=api burst=5 nodelay;
    proxy_pass http://localhost:8000;
}
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:test@localhost/test_db
        REDIS_URL: redis://localhost:6379/0
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
    
    - name: SonarCloud scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t ai-moderator:${{ github.sha }} .
        docker tag ai-moderator:${{ github.sha }} ai-moderator:latest
    
    - name: Push to registry
      run: |
        docker push ai-moderator:${{ github.sha }}
        docker push ai-moderator:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        kubectl set image deployment/ai-moderator-api \
          api=ai-moderator:${{ github.sha }} \
          --record
```

---

## 📋 Infrastructure as Code (Terraform)

```hcl
# main.tf

provider "aws" {
  region = var.aws_region
}

# RDS PostgreSQL
resource "aws_db_instance" "moderation_db" {
  identifier     = "ai-moderator-db"
  engine         = "postgres"
  engine_version = "15"
  instance_class = "db.t3.micro"
  
  db_name  = "moderation_db"
  username = "postgres"
  password = var.db_password
  
  allocated_storage = 20
  backup_retention_period = 30
  multi_az = true
  
  skip_final_snapshot = false
  final_snapshot_identifier = "ai-moderator-db-final-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "ai-moderator-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  engine_version       = "7.0"
  port                 = 6379
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.redis_auth_token
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "ai-moderator-cluster"
}

# ALB
resource "aws_lb" "main" {
  name               = "ai-moderator-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.default.ids
}

# CloudWatch Logs
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/ai-moderator"
  retention_in_days = 30
}
```

---

## 🚨 Disaster Recovery

### Backup Strategy
```bash
#!/bin/bash
# Automated daily backup

DATE=$(date +%Y-%m-%d)

# Database backup
pg_dump -h $DB_HOST -U postgres moderation_db | \
  gzip > /backups/db-backup-$DATE.sql.gz

# Upload to S3
aws s3 cp /backups/db-backup-$DATE.sql.gz \
  s3://ai-moderator-backups/db/$DATE/

# Cleanup old backups (keep 30 days)
find /backups -name "db-backup-*.sql.gz" -mtime +30 -delete

# Test restore (monthly)
if [ $(date +%d) -eq 1 ]; then
  psql -h restore-test-db -U postgres -f /backups/db-backup-$(date -d "7 days ago" +%Y-%m-%d).sql
fi
```

### Restoration Procedure
```bash
# 1. Create new database
createdb -h $NEW_HOST -U postgres moderation_db

# 2. Restore from backup
gunzip -c /backups/db-backup-2024-01-01.sql.gz | \
  psql -h $NEW_HOST -U postgres moderation_db

# 3. Verify
psql -h $NEW_HOST -U postgres -d moderation_db -c "SELECT COUNT(*) FROM content;"

# 4. Update application config
# Update DATABASE_URL to new host
# Restart services
```

---

**Last Updated:** January 9, 2026  
**Version:** 1.0.0
