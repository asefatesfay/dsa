# DevOps Engineering

Modern DevOps practices, CI/CD, automation, and infrastructure management.

---

## 📋 Core Concepts

### 1. **CI/CD Pipelines**

#### GitHub Actions
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: '18'
  DOCKER_REGISTRY: 'myregistry.azurecr.io'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linting
        run: npm run lint
      
      - name: Run tests
        run: npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.DOCKER_REGISTRY }}
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_REGISTRY }}/myapp:latest
            ${{ env.DOCKER_REGISTRY }}/myapp:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.DOCKER_REGISTRY }}/myapp:latest
          cache-to: type=inline

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: |
            ${{ env.DOCKER_REGISTRY }}/myapp:${{ github.sha }}
          kubectl-version: 'latest'
```

#### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'myapp'
        KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        
        stage('Security Scan') {
            steps {
                sh 'trivy image ${IMAGE_NAME}:${env.BUILD_NUMBER}'
            }
        }
        
        stage('Push') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        docker.image("${IMAGE_NAME}:${env.BUILD_NUMBER}").push()
                        docker.image("${IMAGE_NAME}:${env.BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    kubectl set image deployment/myapp \
                        myapp=${IMAGE_NAME}:${BUILD_NUMBER} \
                        --record
                    kubectl rollout status deployment/myapp
                '''
            }
        }
    }
    
    post {
        success {
            slackSend channel: '#deployments',
                      color: 'good',
                      message: "Deployment successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#deployments',
                      color: 'danger',
                      message: "Deployment failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
    }
}
```

#### GitLab CI/CD
```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

test:
  stage: test
  image: node:18
  cache:
    paths:
      - node_modules/
  before_script:
    - npm ci
  script:
    - npm run lint
    - npm test
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  image: docker:20
  services:
    - docker:20-dind
  only:
    - main
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest

deploy_production:
  stage: deploy
  image: bitnami/kubectl:latest
  only:
    - main
  environment:
    name: production
    url: https://app.example.com
  script:
    - kubectl config use-context production
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
```

---

## 🌟 Real-World Example: Netflix-Style Deployment Pipeline

### Scenario: Microservices Platform with 200+ Services

**Requirements:**
- Deploy 50-100 times per day
- Zero-downtime deployments
- Automatic rollback on errors
- Canary releases for gradual traffic shifting
- Complete audit trail

### Architecture

```
┌───────────────────────────────────────────────────────┐
│                    Developer Commits                      │
│                          to main                          │
└───────────────────────────────────────────────────────┘
                             │
                             ▼
        ┌─────────────────────────────────────────────┐
        │         CI: GitHub Actions                   │
        │  ✓ Lint code                              │
        │  ✓ Run unit tests (80% coverage min)     │
        │  ✓ Run integration tests                 │
        │  ✓ Security scan (Snyk, Trivy)           │
        │  ✓ Build Docker image                    │
        │  ✓ Push to ECR                           │
        └─────────────────────────────────────────────┘
                             │
                             ▼
        ┌─────────────────────────────────────────────┐
        │      Deploy to Staging (Auto)              │
        │  ✓ Deploy via ArgoCD                     │
        │  ✓ Run smoke tests                       │
        │  ✓ Run E2E tests (Cypress)               │
        │  ✓ Performance tests (k6)                │
        └─────────────────────────────────────────────┘
                             │
                             ▼
        ┌─────────────────────────────────────────────┐
        │    Manual Approval Required               │
        │    (Senior Engineer/Tech Lead)            │
        └─────────────────────────────────────────────┘
                             │
                             ▼
        ┌─────────────────────────────────────────────┐
        │   Production Canary Deployment           │
        │   (5% traffic for 10 minutes)            │
        │   Monitor:                               │
        │    - Error rate < 0.1%                   │
        │    - Latency P95 < 200ms                 │
        │    - CPU/Memory within limits            │
        └─────────────────────────────────────────────┘
                      │
          ┌───────────┼────────────┐
          │ Metrics OK?         │
          ▼ NO                YES ▼
    ┌──────────┐        ┌─────────────────┐
    │ Auto     │        │ Gradual Rollout:│
    │ Rollback │        │ 5% → 25% → 50% │
    │ to v1.2  │        │ → 75% → 100%   │
    └──────────┘        └─────────────────┘
```

### Complete CI/CD Implementation

```yaml
# .github/workflows/deploy.yml
name: Deploy Microservice

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: user-service
  EKS_CLUSTER: production-cluster

jobs:
  # Job 1: Run Tests
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run unit tests
        run: npm test -- --coverage
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379
      
      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
  
  # Job 2: Security Scanning
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: test
          args: --severity-threshold=high
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
  
  # Job 3: Build and Push Docker Image
  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.version }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:cache
          cache-to: type=inline
          build-args: |
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
            VCS_REF=${{ github.sha }}
      
      - name: Scan image with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta.outputs.tags }}
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
  
  # Job 4: Deploy to Staging
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig \
            --region ${{ env.AWS_REGION }} \
            --name staging-cluster
      
      - name: Deploy to Staging via ArgoCD
        run: |
          # Update image tag in Helm values
          yq eval '.image.tag = "${{ needs.build.outputs.image-tag }}"' \
            -i k8s/staging/values.yaml
          
          # Commit and push to trigger ArgoCD
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add k8s/staging/values.yaml
          git commit -m "Deploy ${{ needs.build.outputs.image-tag }} to staging"
          git push
      
      - name: Wait for deployment
        run: |
          kubectl rollout status deployment/user-service \
            -n staging \
            --timeout=5m
      
      - name: Run smoke tests
        run: |
          npm run test:smoke -- --env=staging
      
      - name: Run E2E tests
        uses: cypress-io/github-action@v5
        with:
          config: baseUrl=https://staging.example.com
          spec: cypress/e2e/**/*.cy.js
      
      - name: Run performance tests
        run: |
          k6 run --vus 50 --duration 2m tests/load-test.js
  
  # Job 5: Deploy to Production (Canary)
  deploy-production:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://api.example.com
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig \
            --region ${{ env.AWS_REGION }} \
            --name ${{ env.EKS_CLUSTER }}
      
      - name: Deploy Canary (5%)
        run: |
          kubectl set image deployment/user-service-canary \
            user-service=${{ needs.build.outputs.image-tag }} \
            -n production
          
          kubectl rollout status deployment/user-service-canary \
            -n production \
            --timeout=5m
      
      - name: Monitor canary metrics (10 minutes)
        run: |
          python scripts/monitor-canary.py \
            --deployment user-service-canary \
            --duration 600 \
            --error-rate-threshold 0.1 \
            --latency-p95-threshold 200
      
      - name: Gradual rollout
        run: |
          # If canary succeeded, roll out gradually
          for percentage in 25 50 75 100; do
            echo "Rolling out to $percentage%"
            kubectl patch deployment user-service \
              -n production \
              -p '{"spec":{"template":{"spec":{"containers":[{"name":"user-service","image":"${{ needs.build.outputs.image-tag }}"}]}}}}'
            
            kubectl rollout status deployment/user-service \
              -n production \
              --timeout=5m
            
            # Monitor for 5 minutes at each stage
            python scripts/monitor-deployment.py \
              --deployment user-service \
              --duration 300
            
            echo "$percentage% rollout successful"
          done
      
      - name: Rollback on failure
        if: failure()
        run: |
          echo "Deployment failed, rolling back..."
          kubectl rollout undo deployment/user-service -n production
          kubectl rollout status deployment/user-service -n production
          
          # Send alert
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{
              "text": "\u26a0\ufe0f Production deployment FAILED and rolled back",
              "blocks": [{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Deployment Failed*\nService: user-service\nVersion: ${{ needs.build.outputs.image-tag }}\nAction: Rolled back to previous version"
                }
              }]
            }'
      
      - name: Success notification
        if: success()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{
              "text": "\u2705 Production deployment successful",
              "blocks": [{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Deployment Successful*\nService: user-service\nVersion: ${{ needs.build.outputs.image-tag }}\nCommit: ${{ github.sha }}"
                }
              }]
            }'
```

### Canary Monitoring Script

```python
# scripts/monitor-canary.py
import time
import sys
import requests
from datadog import initialize, api

class CanaryMonitor:
    def __init__(self, deployment, duration, error_threshold, latency_threshold):
        self.deployment = deployment
        self.duration = duration
        self.error_threshold = error_threshold
        self.latency_threshold = latency_threshold
        
        initialize(
            api_key=os.getenv('DATADOG_API_KEY'),
            app_key=os.getenv('DATADOG_APP_KEY')
        )
    
    def check_error_rate(self):
        """Check if error rate is below threshold"""
        query = f'''
            sum:requests.errors{{deployment:{self.deployment}}} /
            sum:requests.total{{deployment:{self.deployment}}}
        '''
        
        result = api.Metric.query(
            start=int(time.time()) - 300,  # Last 5 minutes
            end=int(time.time()),
            query=query
        )
        
        if result['series']:
            error_rate = result['series'][0]['pointlist'][-1][1]
            print(f"Current error rate: {error_rate:.4f}%")
            return error_rate < self.error_threshold
        
        return True
    
    def check_latency(self):
        """Check if P95 latency is below threshold"""
        query = f'p95:requests.duration{{deployment:{self.deployment}}}'
        
        result = api.Metric.query(
            start=int(time.time()) - 300,
            end=int(time.time()),
            query=query
        )
        
        if result['series']:
            p95_latency = result['series'][0]['pointlist'][-1][1]
            print(f"Current P95 latency: {p95_latency:.2f}ms")
            return p95_latency < self.latency_threshold
        
        return True
    
    def check_resource_usage(self):
        """Check CPU and memory usage"""
        queries = {
            'cpu': f'avg:kubernetes.cpu.usage.total{{deployment:{self.deployment}}}',
            'memory': f'avg:kubernetes.memory.usage{{deployment:{self.deployment}}}'
        }
        
        for metric, query in queries.items():
            result = api.Metric.query(
                start=int(time.time()) - 300,
                end=int(time.time()),
                query=query
            )
            
            if result['series']:
                value = result['series'][0]['pointlist'][-1][1]
                print(f"Current {metric}: {value:.2f}%")
                
                if value > 90:
                    print(f"WARNING: {metric} usage above 90%")
                    return False
        
        return True
    
    def monitor(self):
        """Monitor canary deployment"""
        start_time = time.time()
        check_interval = 30  # Check every 30 seconds
        
        print(f"Monitoring canary deployment for {self.duration} seconds...")
        
        while time.time() - start_time < self.duration:
            print(f"\nChecking metrics at {int(time.time() - start_time)}s...")
            
            if not self.check_error_rate():
                print("\u274c Error rate threshold exceeded!")
                sys.exit(1)
            
            if not self.check_latency():
                print("\u274c Latency threshold exceeded!")
                sys.exit(1)
            
            if not self.check_resource_usage():
                print("\u274c Resource usage threshold exceeded!")
                sys.exit(1)
            
            print("\u2705 All metrics within thresholds")
            time.sleep(check_interval)
        
        print("\n\u2705 Canary monitoring completed successfully!")
        return 0

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--deployment', required=True)
    parser.add_argument('--duration', type=int, required=True)
    parser.add_argument('--error-rate-threshold', type=float, default=0.1)
    parser.add_argument('--latency-p95-threshold', type=float, default=200)
    
    args = parser.parse_args()
    
    monitor = CanaryMonitor(
        deployment=args.deployment,
        duration=args.duration,
        error_threshold=args.error_rate_threshold,
        latency_threshold=args.latency_p95_threshold
    )
    
    sys.exit(monitor.monitor())
```

---

## 🚨 Real Production Incident Response

### Incident: Service Down at 3 AM

**Timeline:**

```
03:00 AM - PagerDuty alert: API error rate 25% (threshold: 1%)
03:02 AM - On-call engineer acknowledged
03:05 AM - Identified: Recent deployment (v2.4.5) 15 minutes ago
03:07 AM - Decision: Rollback to v2.4.4
03:08 AM - Executed rollback command
03:12 AM - Service recovered, error rate back to 0.1%
03:15 AM - Post-mortem started
```

**Runbook (Incident Response)**

```bash
#!/bin/bash
# Production Incident Response Runbook

set -e

echo "=== PRODUCTION INCIDENT RESPONSE ==="
echo "Timestamp: $(date)"
echo "Incident ID: INC-$(date +%Y%m%d-%H%M%S)"

# Step 1: Check current status
echo "\n[1] Checking service health..."
kubectl get pods -n production -l app=user-service
kubectl top pods -n production -l app=user-service

# Step 2: Check recent deployments
echo "\n[2] Recent deployments:"
kubectl rollout history deployment/user-service -n production

# Step 3: Check logs for errors
echo "\n[3] Recent error logs:"
kubectl logs -n production -l app=user-service \
  --tail=100 \
  --since=15m \
  | grep -i "error\|exception\|fatal"

# Step 4: Check metrics
echo "\n[4] Current metrics:"
ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~'5..'}[5m])" \
  | jq -r '.data.result[0].value[1]')
echo "Error rate: $ERROR_RATE"

LATENCY_P95=$(curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.95,http_request_duration_seconds_bucket[5m])" \
  | jq -r '.data.result[0].value[1]')
echo "P95 Latency: ${LATENCY_P95}ms"

# Step 5: Decision point
read -p "\nProceed with rollback? (yes/no): " ROLLBACK

if [ "$ROLLBACK" = "yes" ]; then
  echo "\n[5] Rolling back to previous version..."
  
  # Get previous revision
  PREVIOUS_REVISION=$(kubectl rollout history deployment/user-service -n production \
    | tail -n 2 | head -n 1 | awk '{print $1}')
  
  echo "Rolling back to revision $PREVIOUS_REVISION"
  
  kubectl rollout undo deployment/user-service \
    -n production \
    --to-revision=$PREVIOUS_REVISION
  
  echo "Waiting for rollback to complete..."
  kubectl rollout status deployment/user-service \
    -n production \
    --timeout=5m
  
  echo "\n[6] Verifying recovery..."
  sleep 60  # Wait for metrics to stabilize
  
  NEW_ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~'5..'}[5m])" \
    | jq -r '.data.result[0].value[1]')
  
  echo "New error rate: $NEW_ERROR_RATE"
  
  if (( $(echo "$NEW_ERROR_RATE < 0.01" | bc -l) )); then
    echo "\u2705 Service recovered successfully!"
    
    # Send success notification
    curl -X POST $SLACK_WEBHOOK \
      -H 'Content-Type: application/json' \
      -d '{
        "text": "Incident resolved: Service rolled back successfully",
        "channel": "#incidents"
      }'
  else
    echo "\u26a0\ufe0f Service still experiencing issues. Escalating..."
    # Page senior engineer
  fi
fi

echo "\n=== INCIDENT RESPONSE COMPLETE ==="
echo "Next steps:"
echo "1. Create post-mortem document"
echo "2. Schedule blameless retrospective"
echo "3. Identify root cause"
echo "4. Implement preventive measures"
```

### Post-Mortem Template

```markdown
# Post-Mortem: API Service Outage

**Date:** 2024-12-30  
**Duration:** 12 minutes  
**Severity:** P1 (Critical)  
**Affected Users:** ~50,000 (5% of total)  

## Summary
API service experienced 25% error rate following deployment of v2.4.5 due to database connection pool exhaustion.

## Timeline (UTC)
- **02:45** - Deployment of v2.4.5 started
- **03:00** - First alerts triggered (error rate spike)
- **03:02** - On-call engineer paged
- **03:05** - Root cause identified: connection pool size unchanged despite increased traffic
- **03:08** - Rollback initiated to v2.4.4
- **03:12** - Service fully recovered

## Root Cause
New feature in v2.4.5 made additional database queries per request (N+1 problem), exhausting connection pool (max 20 connections).

```sql
-- Before (1 query)
SELECT * FROM users WHERE id IN (1,2,3,4,5);

-- After (N queries - bug!)
FOR EACH user_id:
  SELECT * FROM users WHERE id = user_id;
```

## Impact
- **Users Affected:** 50,000 (5%)
- **API Error Rate:** 25% for 12 minutes
- **Revenue Impact:** ~$2,500 in lost transactions
- **SLA Impact:** Consumed 30% of monthly error budget

## Detection
- **Time to Detect:** 15 minutes (too long)
- **Detection Method:** Automated alerts (Prometheus)

## Resolution
- **Time to Resolve:** 12 minutes
- **Resolution:** Rolled back to v2.4.4

## What Went Well
1. \u2705 Automated rollback process worked perfectly
2. \u2705 Monitoring caught the issue quickly
3. \u2705 Clear runbook made response straightforward
4. \u2705 Communication to stakeholders was timely

## What Went Wrong
1. \u274c N+1 query not caught in code review
2. \u274c Load tests didn't reflect production query patterns
3. \u274c No canary deployment (went straight to 100%)
4. \u274c Database connection pool size not reviewed

## Action Items

### Immediate (Week 1)
- [x] Fix N+1 query issue (PR #1234) - @john
- [x] Increase connection pool to 50 - @sarah  
- [x] Add database query monitoring - @mike

### Short-term (Month 1)
- [ ] Implement mandatory canary deployments - @devops-team
- [ ] Add query count checks to CI pipeline - @qa-team
- [ ] Improve load test scenarios - @perf-team
- [ ] Add connection pool saturation alerts - @sre-team

### Long-term (Quarter 1)
- [ ] Implement automatic query optimization checks
- [ ] Add pre-deployment database impact analysis
- [ ] Create automated performance regression tests
- [ ] Document database best practices

## Lessons Learned
1. **Always use canary deployments for production**
2. **Load tests must mirror production query patterns**
3. **Monitor database connection pool utilization**
4. **Code review must check for N+1 queries**
5. **Fast rollback capability is critical**

## Supporting Documents
- Incident Slack thread: #incident-20241230-api-outage
- Grafana dashboard: https://grafana.company.com/d/incident-123
- GitHub PR with fix: https://github.com/company/api/pull/1234
```

---

## 🛠️ Configuration Management

### Ansible Playbook
```yaml
---
- name: Deploy web application
  hosts: webservers
  become: yes
  vars:
    app_name: myapp
    app_version: "1.0.0"
    app_port: 3000
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install required packages
      apt:
        name:
          - nodejs
          - npm
          - nginx
        state: present
    
    - name: Create application directory
      file:
        path: /opt/{{ app_name }}
        state: directory
        owner: www-data
        group: www-data
        mode: '0755'
    
    - name: Copy application files
      synchronize:
        src: dist/
        dest: /opt/{{ app_name }}/
        delete: yes
      notify: Restart application
    
    - name: Install npm dependencies
      npm:
        path: /opt/{{ app_name }}
        production: yes
      become_user: www-data
    
    - name: Configure nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
      notify: Reload nginx
    
    - name: Enable nginx site
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link
      notify: Reload nginx
    
    - name: Start application service
      systemd:
        name: "{{ app_name }}"
        state: started
        enabled: yes
  
  handlers:
    - name: Restart application
      systemd:
        name: "{{ app_name }}"
        state: restarted
    
    - name: Reload nginx
      systemd:
        name: nginx
        state: reloaded
```

### Chef Recipe
```ruby
# Recipe: myapp::default

package %w[nodejs npm nginx] do
  action :install
end

directory '/opt/myapp' do
  owner 'www-data'
  group 'www-data'
  mode '0755'
  action :create
end

git '/opt/myapp' do
  repository 'https://github.com/myorg/myapp.git'
  revision 'main'
  user 'www-data'
  group 'www-data'
  action :sync
  notifies :run, 'execute[npm-install]', :immediately
end

execute 'npm-install' do
  command 'npm ci --production'
  cwd '/opt/myapp'
  user 'www-data'
  action :nothing
end

template '/etc/nginx/sites-available/myapp' do
  source 'nginx.conf.erb'
  variables({
    app_port: 3000,
    server_name: node['myapp']['server_name']
  })
  notifies :reload, 'service[nginx]'
end

service 'myapp' do
  action [:enable, :start]
end

service 'nginx' do
  action [:enable, :start]
end
```

---

## 📦 Artifact Management

### Nexus Repository Configuration
```groovy
// Maven pom.xml
<distributionManagement>
  <repository>
    <id>nexus-releases</id>
    <url>https://nexus.example.com/repository/maven-releases/</url>
  </repository>
  <snapshotRepository>
    <id>nexus-snapshots</id>
    <url>https://nexus.example.com/repository/maven-snapshots/</url>
  </snapshotRepository>
</distributionManagement>
```

### JFrog Artifactory
```yaml
# .npmrc configuration
registry=https://artifactory.example.com/artifactory/api/npm/npm-remote/
//artifactory.example.com/artifactory/api/npm/npm-remote/:_authToken=${ARTIFACTORY_TOKEN}
```

---

## 🔍 Monitoring & Logging

### ELK Stack (Elasticsearch, Logstash, Kibana)

#### Logstash Configuration
```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  if [type] == "nginx" {
    grok {
      match => {
        "message" => '%{IPORHOST:clientip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "%{WORD:verb} %{DATA:request} HTTP/%{NUMBER:httpversion}" %{NUMBER:response:int} (?:-|%{NUMBER:bytes:int}) %{QS:referrer} %{QS:agent}'
      }
    }
    date {
      match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    }
    geoip {
      source => "clientip"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logstash-%{+YYYY.MM.dd}"
  }
  stdout {
    codec => rubydebug
  }
}
```

### Grafana Dashboard (Prometheus)
```json
{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "Response Time P95",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

---

## 🛡️ Security & Compliance

### Secret Management (HashiCorp Vault)
```python
import hvac

# Connect to Vault
client = hvac.Client(url='https://vault.example.com')
client.token = os.getenv('VAULT_TOKEN')

# Read secret
secret = client.secrets.kv.v2.read_secret_version(
    path='myapp/database',
    mount_point='secret'
)

db_password = secret['data']['data']['password']

# Dynamic database credentials
db_creds = client.secrets.database.generate_credentials(
    name='my-role',
    mount_point='database'
)
```

### Security Scanning
```bash
# Trivy - Container vulnerability scanning
trivy image myapp:latest

# SonarQube - Code quality and security
sonar-scanner \
  -Dsonar.projectKey=myapp \
  -Dsonar.sources=. \
  -Dsonar.host.url=https://sonar.example.com

# OWASP Dependency Check
dependency-check.sh --scan . --format HTML --out report.html
```

---

## 🎯 Senior DevOps Engineer Focus

### 1. **GitOps**
- ArgoCD for Kubernetes deployments
- Flux for continuous delivery
- Infrastructure as Code principles

### 2. **Chaos Engineering**
- Resilience testing
- Failure injection
- Recovery procedures

### 3. **Service Mesh**
- Istio configuration
- Traffic management
- Security policies

### 4. **Platform Engineering**
- Developer self-service
- Internal developer platforms
- Standardization and best practices

### 5. **SRE Practices**
- SLO/SLI/SLA definitions
- Error budgets
- Incident response

---

## 📚 Learning Path

**Month 1-2:** CI/CD Fundamentals
- Jenkins, GitHub Actions, GitLab CI
- Docker and containerization
- Basic Kubernetes

**Month 3-4:** Infrastructure as Code
- Terraform
- Ansible/Chef
- Cloud provider tools (CloudFormation, ARM)

**Month 5-6:** Advanced Topics
- Service mesh (Istio)
- GitOps (ArgoCD)
- Observability stack

**Month 7-8:** Security & Compliance
- Secrets management
- Security scanning
- Compliance automation

**Certifications:**
- Kubernetes Administrator (CKA)
- AWS DevOps Engineer Professional
- Terraform Associate
