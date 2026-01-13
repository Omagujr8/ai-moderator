# Pre-Deployment Production Checklist

## 📋 Complete this checklist before deploying to production

---

## 1. Code & Testing

- [ ] All tests passing: `pytest tests/ -v`
- [ ] Coverage > 75%: `pytest tests/ -v --cov=app --cov-report=term-missing`
- [ ] No linting errors: `flake8 backend/app`
- [ ] Type checking passes: `mypy backend/app`
- [ ] Load test successful: `locust -f tests/load_test.py`
- [ ] No hardcoded secrets in code
- [ ] No debug mode enabled
- [ ] No print() statements left in code (use logging instead)
- [ ] All TODOs reviewed and addressed

---

## 2. Environment & Secrets

- [ ] `.env` file created with production values
- [ ] `.env` added to `.gitignore` (verify: `git check-ignore .env`)
- [ ] Strong SECRET_KEY generated (32+ random characters)
- [ ] DATABASE_URL points to production database
- [ ] REDIS_URL points to production Redis instance
- [ ] API_KEYS rotated and updated
- [ ] All env vars documented in `.env.example`
- [ ] No secrets in git history: `git log -S password --all`

---

## 3. Database

- [ ] PostgreSQL database created and accessible
- [ ] Database backups configured
- [ ] Alembic migrations up-to-date: `alembic current`
- [ ] Latest migration applied: `alembic upgrade head`
- [ ] Rollback tested: `alembic downgrade -1 && alembic upgrade head`
- [ ] Connection pooling configured (if needed)
- [ ] Database user has limited permissions (not full admin)
- [ ] Read replicas configured (if applicable)

---

## 4. Redis/Caching

- [ ] Redis instance running and accessible
- [ ] Redis persistence configured (RDB or AOF)
- [ ] Redis max memory policy set appropriately
- [ ] Redis authentication enabled (if applicable)
- [ ] Redis backup strategy in place
- [ ] Redis monitoring alerts configured

---

## 5. Celery Workers

- [ ] Celery broker (Redis) accessible
- [ ] Celery workers can connect to broker
- [ ] Worker process management configured (systemd/supervisor)
- [ ] Worker auto-restart on failure enabled
- [ ] Worker logs monitored
- [ ] Celery Flower monitoring deployed (optional but recommended)
- [ ] Task timeout values appropriate for workload
- [ ] Dead letter queue monitoring configured

---

## 6. Logging & Monitoring

- [ ] Log aggregation service configured (ELK, DataDog, CloudWatch, etc.)
- [ ] Logs shipping to aggregation service
- [ ] Log retention policy set (30+ days recommended)
- [ ] Error alerting configured
- [ ] Performance alerts configured
- [ ] Rate limit breach alerts configured
- [ ] Database query logging enabled for debugging
- [ ] No sensitive data in logs (passwords, tokens, PII)

---

## 7. Metrics & Observability

- [ ] Prometheus configured to scrape `/metrics` endpoint
- [ ] Grafana dashboards created for:
  - [ ] Request rate and latency
  - [ ] Error rate by endpoint
  - [ ] Worker task queue depth
  - [ ] Database connection pool
  - [ ] Redis memory usage
  - [ ] System CPU and memory
- [ ] Alert rules configured in Prometheus/Alertmanager
- [ ] Alertmanager notifications configured (Slack/PagerDuty/etc.)
- [ ] Health check endpoints verified: GET / and GET /health

---

## 8. Security

- [ ] HTTPS/TLS enforced (certificate installed)
- [ ] CORS configured appropriately (not wildcards in production)
- [ ] Security headers configured:
  - [ ] X-Content-Type-Options: nosniff
  - [ ] X-Frame-Options: DENY
  - [ ] Strict-Transport-Security
  - [ ] X-XSS-Protection
- [ ] API key rotation schedule established
- [ ] SQL injection prevention verified (using ORM)
- [ ] XSS prevention verified (FastAPI automatic escaping)
- [ ] CSRF protection configured (if needed)
- [ ] Rate limiting working: 30 req/min per client
- [ ] API keys validated on every request
- [ ] Admin/client role separation enforced

---

## 9. Container & Deployment

- [ ] Docker image builds successfully
- [ ] Docker image layers optimized (minimal size)
- [ ] Docker image scanned for vulnerabilities
- [ ] Docker Compose working: `docker-compose up -d`
- [ ] Health check defined in Dockerfile
- [ ] Resource limits configured (memory, CPU)
- [ ] Container log collection configured
- [ ] Container image signed/verified (if applicable)

---

## 10. Kubernetes (if applicable)

- [ ] Deployment manifest created
- [ ] Service manifest created
- [ ] Ingress manifest created (with TLS)
- [ ] ConfigMap created for non-secret config
- [ ] Secret created for sensitive values
- [ ] Resource requests/limits configured
- [ ] Health check probes configured:
  - [ ] Liveness probe: GET /health
  - [ ] Readiness probe: GET /health
- [ ] Pod Disruption Budget configured
- [ ] Network Policy configured (if needed)
- [ ] RBAC roles configured

---

## 11. Load Balancer & Reverse Proxy

- [ ] Load balancer health check configured
- [ ] Health check interval appropriate (30s recommended)
- [ ] Sticky sessions configured (if needed)
- [ ] SSL/TLS termination configured
- [ ] Request timeout values appropriate
- [ ] Connection pooling configured
- [ ] Logging configured for troubleshooting

---

## 12. Backup & Disaster Recovery

- [ ] Database backup strategy implemented
- [ ] Backup retention policy set (30+ days recommended)
- [ ] Backup encryption enabled
- [ ] Restore tested successfully (full and point-in-time)
- [ ] RTO (Recovery Time Objective) defined and tested
- [ ] RPO (Recovery Point Objective) defined and tested
- [ ] Disaster recovery runbook created
- [ ] Team trained on runbook

---

## 13. Performance

- [ ] Database query performance analyzed (slow queries addressed)
- [ ] N+1 query problems identified and fixed
- [ ] Database indexes on foreign keys verified
- [ ] Connection pooling configured
- [ ] Caching strategy reviewed
- [ ] API response times acceptable (<200ms p95)
- [ ] Worker task processing time monitored
- [ ] Memory leaks ruled out (monitored over time)

---

## 14. Documentation

- [ ] Architecture diagram created
- [ ] API documentation up-to-date (OpenAPI/Swagger)
- [ ] Environment variables documented
- [ ] Deployment runbook created
- [ ] Troubleshooting guide created
- [ ] Incident response procedures documented
- [ ] On-call rotation documented
- [ ] Emergency contacts listed

---

## 15. Team & Process

- [ ] All team members aware of deployment
- [ ] On-call engineer assigned for first 24 hours
- [ ] Rollback plan documented and tested
- [ ] Change management process followed
- [ ] Stakeholders notified of deployment window
- [ ] Deployment window scheduled during low-traffic time
- [ ] Status page updated (if applicable)
- [ ] Post-deployment review scheduled

---

## 16. Final Verification Steps

### Run verification script:
```bash
python verify_production_ready.py
```

### Expected output:
```
✅ Passed: 24
❌ Failed: 0
📊 Success Rate: 100.0%

🚀 STATUS: APPROVED FOR PRODUCTION
```

### Manual smoke tests:
```bash
# Test root endpoint
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# Test metrics endpoint
curl http://localhost:8000/metrics

# Test moderation endpoint with proper auth
curl -X POST http://localhost:8000/api/v1/moderation/analyse \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "test-1",
    "text": "Test content",
    "content_type": "comment",
    "source_app": "test"
  }'

# Verify rate limiting (should get 429 after 30 requests)
for i in {1..35}; do
  curl -X POST http://localhost:8000/api/v1/moderation/analyse \
    -H "X-API-KEY: your-api-key" \
    -H "Content-Type: application/json" \
    -d '{"external_id": "test-'$i'", "text": "Test", "content_type": "comment", "source_app": "test"}'
done
```

---

## 17. Deployment Day

### Pre-deployment (1 hour before)

- [ ] All team members online and available
- [ ] Database backed up fresh
- [ ] Redis persisted
- [ ] Monitoring dashboards open
- [ ] Alert channels muted (if needed)
- [ ] Communication channel active (Slack/Teams)

### During deployment

- [ ] Roll out to canary/staging first
- [ ] Monitor metrics during rollout
- [ ] Gradually increase traffic to new version
- [ ] Watch for errors, latency increases, memory leaks
- [ ] Have rollback plan ready to execute

### Post-deployment (24+ hours monitoring)

- [ ] Monitor error rates closely
- [ ] Monitor latency metrics
- [ ] Monitor worker queue depth
- [ ] Verify no memory leaks over 24 hours
- [ ] Verify backup strategy still working
- [ ] Verify all integrations still functional
- [ ] Gather metrics for post-mortem
- [ ] Document any issues encountered

---

## 18. Post-Deployment

- [ ] Update deployment log with version, time, and notes
- [ ] Notify stakeholders of successful deployment
- [ ] Schedule post-deployment review
- [ ] Archive metrics and logs for future reference
- [ ] Review any alerts that fired
- [ ] Document any issues for next sprint

---

## 📊 Approval Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Tech Lead | _____________ | _____________ | _____________ |
| DevOps | _____________ | _____________ | _____________ |
| Product | _____________ | _____________ | _____________ |
| QA | _____________ | _____________ | _____________ |

---

## 🚨 Rollback Procedures

If critical issues occur post-deployment:

1. **Immediate Actions:**
   ```bash
   # Stop traffic to affected instances
   kubectl set replicas deployment/ai-moderator 0
   
   # Or if using docker-compose
   docker-compose down
   
   # Revert to previous image
   docker pull ai-moderator:previous-version
   docker run -d ai-moderator:previous-version
   ```

2. **Database Rollback (if needed):**
   ```bash
   # Restore from backup
   alembic downgrade -1
   psql moderation_db < backup.sql
   ```

3. **Communication:**
   - Notify all stakeholders
   - Post status update to status page
   - Send incident notification
   - Schedule post-incident review

4. **Investigation:**
   - Collect logs and metrics
   - Identify root cause
   - Create issue for team
   - Plan fix for next deployment

---

## ✅ Final Checklist

- [ ] This checklist has been completed entirely
- [ ] Verification script shows green (100% pass rate)
- [ ] Smoke tests passed successfully
- [ ] Team is ready for deployment
- [ ] Rollback plan is ready to execute
- [ ] Monitoring is in place and verified
- [ ] On-call engineer briefed and available

**Ready for Production Deployment: ______ (Date/Time)**

---

*Last Updated: January 9, 2026*  
*AI Moderator v1.0.0*
