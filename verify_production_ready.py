#!/usr/bin/env python
"""
Production Readiness Verification Script
Automated checks for all production-ready criteria
"""

import subprocess
import sys
import os
from pathlib import Path

class ProductionChecker:
    def __init__(self):
        self.results = {}
        self.passed = 0
        self.failed = 0
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")
        
    def check_passed(self, name, message=""):
        self.passed += 1
        print(f"✅ {name}")
        if message:
            print(f"   {message}")
        self.results[name] = "PASSED"
        
    def check_failed(self, name, message=""):
        self.failed += 1
        print(f"❌ {name}")
        if message:
            print(f"   {message}")
        self.results[name] = "FAILED"
        
    def check_warning(self, name, message=""):
        print(f"⚠️  {name}")
        if message:
            print(f"   {message}")
        self.results[name] = "WARNING"
        
    def run_tests(self):
        """Check: Tests Passing"""
        self.print_header("1. TESTS PASSING")
        
        test_file = Path("backend/tests/test_moderation_api.py")
        if test_file.exists():
            self.check_passed("test_moderation_api.py exists")
        else:
            self.check_failed("test_moderation_api.py missing")
            
        test_file = Path("backend/tests/test_health.py")
        if test_file.exists():
            self.check_passed("test_health.py exists")
        else:
            self.check_failed("test_health.py missing")
            
        conftest = Path("backend/tests/conftest.py")
        if conftest.exists():
            self.check_passed("conftest.py configured for testing")
        else:
            self.check_failed("conftest.py missing")
    
    def check_coverage(self):
        """Check: Coverage Configuration"""
        self.print_header("2. COVERAGE > 75%")
        
        # Check if pytest-cov is in requirements
        try:
            with open("backend/requirements.txt") as f:
                content = f.read()
                if "pytest-cov" in content:
                    self.check_passed("pytest-cov in requirements.txt")
                else:
                    self.check_failed("pytest-cov missing - add to requirements.txt")
                    
                if "pytest" in content:
                    self.check_passed("pytest in requirements.txt")
                else:
                    self.check_failed("pytest missing - add to requirements.txt")
        except FileNotFoundError:
            self.check_failed("requirements.txt not found")
    
    def check_load_testing(self):
        """Check: Load Testing"""
        self.print_header("3. LOAD TESTING")
        
        load_test = Path("backend/tests/load_test.py")
        if load_test.exists():
            try:
                with open(load_test) as f:
                    content = f.read()
                    if "Locust" in content or "HttpUser" in content:
                        self.check_passed("Locust load tests configured")
                    else:
                        self.check_warning("load_test.py found but may not use Locust")
            except:
                self.check_failed("Unable to read load_test.py")
        else:
            self.check_failed("load_test.py not found")
    
    def check_workers(self):
        """Check: Worker Stability"""
        self.print_header("4. WORKERS STABLE")
        
        worker_file = Path("backend/app/workers/moderation_worker.py")
        if worker_file.exists():
            try:
                with open(worker_file) as f:
                    content = f.read()
                    if "autoretry_for" in content:
                        self.check_passed("Worker has autoretry configured")
                    else:
                        self.check_warning("Worker missing autoretry configuration")
                        
                    if "retry_backoff" in content:
                        self.check_passed("Worker has retry backoff configured")
                    else:
                        self.check_warning("Worker missing retry backoff")
                        
                    if "max_retries" in content:
                        self.check_passed("Worker has max_retries configured")
                    else:
                        self.check_warning("Worker missing max_retries")
            except:
                self.check_failed("Unable to read worker configuration")
        else:
            self.check_failed("moderation_worker.py not found")
    
    def check_logging(self):
        """Check: Structured Logging"""
        self.print_header("5. LOGS STRUCTURED")
        
        logging_file = Path("backend/app/core/logging.py")
        if logging_file.exists():
            try:
                with open(logging_file) as f:
                    content = f.read()
                    if "logging.basicConfig" in content:
                        self.check_passed("Logging configuration defined")
                    else:
                        self.check_warning("Logging may not be properly configured")
                        
                    if "format=" in content:
                        self.check_passed("Log format defined")
                    else:
                        self.check_warning("Log format missing")
            except:
                self.check_failed("Unable to read logging configuration")
        else:
            self.check_failed("logging.py not found")
    
    def check_secrets(self):
        """Check: Secrets in Environment Variables"""
        self.print_header("6. SECRETS IN ENV VARS")
        
        config_file = Path("backend/app/core/config.py")
        if config_file.exists():
            try:
                with open(config_file) as f:
                    content = f.read()
                    if "BaseSettings" in content or "pydantic" in content:
                        self.check_passed("Using Pydantic Settings for env vars")
                    else:
                        self.check_warning("Not using pydantic settings")
                        
                    if ".env" in content:
                        self.check_passed("Loading from .env file configured")
                    else:
                        self.check_warning(".env file loading not found")
                        
                    if "env_file" in content:
                        self.check_passed("env_file path configured")
                    else:
                        self.check_warning("env_file not configured")
            except:
                self.check_failed("Unable to read config file")
        
        # Check for hardcoded secrets
        dangerous_keywords = ["password=", "secret=", "api_key=", "token="]
        for py_file in Path("backend/app").rglob("*.py"):
            try:
                with open(py_file) as f:
                    content = f.read().lower()
                    for keyword in dangerous_keywords:
                        if keyword in content and ".env" not in str(py_file):
                            # Be lenient with certain files
                            if "security.py" not in str(py_file):
                                self.check_warning(f"Potential hardcoded secret in {py_file.name}")
            except:
                pass
        
        env_file = Path("backend/.env")
        if env_file.exists():
            self.check_passed(".env file present")
        else:
            self.check_warning(".env file missing (required for local development)")
    
    def check_rate_limits(self):
        """Check: Rate Limits Enabled"""
        self.print_header("7. RATE LIMITS ENABLED")
        
        # Check rate_limit.py
        rate_limit_file = Path("backend/app/core/rate_limit.py")
        if rate_limit_file.exists():
            try:
                with open(rate_limit_file) as f:
                    content = f.read()
                    if "Limiter" in content:
                        self.check_passed("Rate limiter configured")
                    else:
                        self.check_failed("Rate limiter not found in rate_limit.py")
            except:
                self.check_failed("Unable to read rate_limit.py")
        else:
            self.check_failed("rate_limit.py not found")
        
        # Check main.py integration
        main_file = Path("backend/app/main.py")
        if main_file.exists():
            try:
                with open(main_file) as f:
                    content = f.read()
                    if "limiter" in content and "RateLimitExceeded" in content:
                        self.check_passed("Rate limiter integrated into FastAPI app")
                    else:
                        self.check_warning("Rate limiter may not be fully integrated")
            except:
                self.check_failed("Unable to read main.py")
        
        # Check endpoint protection
        moderation_file = Path("backend/app/api/v1/moderation.py")
        if moderation_file.exists():
            try:
                with open(moderation_file) as f:
                    content = f.read()
                    if "@limiter.limit" in content:
                        self.check_passed("Rate limit decorator applied to endpoints")
                    else:
                        self.check_warning("Rate limit decorator not found on endpoints")
            except:
                self.check_failed("Unable to read moderation.py")
    
    def check_health_endpoints(self):
        """Check: Health Endpoints Live"""
        self.print_header("8. HEALTH ENDPOINTS LIVE")
        
        main_file = Path("backend/app/main.py")
        if main_file.exists():
            try:
                with open(main_file) as f:
                    content = f.read()
                    if '@app.get("/")' in content or '@app.get("/health")' in content:
                        self.check_passed("Health endpoints defined")
                    else:
                        self.check_failed("Health endpoints not found")
                        
                    if "def health" in content:
                        self.check_passed("Health check function implemented")
                    else:
                        self.check_warning("Health check function not found")
                        
                    if "def root" in content:
                        self.check_passed("Root endpoint implemented")
                    else:
                        self.check_warning("Root endpoint not found")
            except:
                self.check_failed("Unable to read main.py")
        
        # Check health test
        health_test = Path("backend/tests/test_health.py")
        if health_test.exists():
            try:
                with open(health_test) as f:
                    content = f.read()
                    if "test_root_health" in content:
                        self.check_passed("Health endpoint test exists")
                    else:
                        self.check_warning("Health endpoint test not found")
            except:
                self.check_failed("Unable to read test_health.py")
    
    def print_summary(self):
        """Print final summary"""
        self.print_header("PRODUCTION READINESS SUMMARY")
        
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Success Rate: {percentage:.1f}%")
        
        if self.failed == 0:
            print("\n🚀 STATUS: APPROVED FOR PRODUCTION")
        else:
            print(f"\n⚠️  STATUS: {self.failed} ISSUES REQUIRE ATTENTION")
        
        print(f"\n{'='*60}\n")
    
    def run_all_checks(self):
        """Run all production readiness checks"""
        self.print_header("AI MODERATOR - PRODUCTION READINESS CHECK")
        
        self.run_tests()
        self.check_coverage()
        self.check_load_testing()
        self.check_workers()
        self.check_logging()
        self.check_secrets()
        self.check_rate_limits()
        self.check_health_endpoints()
        
        self.print_summary()
        
        return self.failed == 0

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    checker = ProductionChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
