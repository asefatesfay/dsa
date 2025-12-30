# DevOps - Real-World Examples

## 🎯 Case Study: Spotify's CI/CD Pipeline

**Scale:**
- 200+ engineering teams
- 4,000+ deployments/day
- 99.9% deployment success rate
- 10-minute average deployment time

**Architecture:**

```
┌─────────────────────────────────────────────┐
│              Developer Workflow              │
└───────────────┬─────────────────────────────┘
                │
                ▼
         ┌──────────────┐
         │   Git Push    │
         └──────┬────────┘
                │
                ▼
    ┌───────────────────────┐
    │   Jenkins Pipeline     │
    │   - Unit Tests         │
    │   - Integration Tests  │
    │   - Security Scans     │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │   Build & Package      │
    │   - Docker Image       │
    │   - Version Tag        │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │   Deploy to Staging    │
    │   - Smoke Tests        │
    │   - E2E Tests          │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │   Canary Deployment    │
    │   - 1% traffic         │
    │   - Monitor 10 min     │
    │   - Auto rollback      │
    └───────────┬───────────┘
                │
         Success? ──No──> Rollback
                │
               Yes
                │
                ▼
    ┌───────────────────────┐
    │   Production Deploy    │
    │   - Blue/Green         │
    │   - 100% traffic       │
    └───────────────────────┘
```

## 🎯 Real Problem: Production Outage Response

**Incident:** Payment service down (June 15, 2024)

**Timeline:**

```
14:32 UTC - Alert triggered (error rate 45%)
14:33 UTC - On-call engineer paged
14:35 UTC - Incident declared, war room opened
14:40 UTC - Identified: Bad deployment v2.3.1
14:42 UTC - Rollback initiated to v2.3.0
14:45 UTC - Service restored (error rate < 0.1%)
14:50 UTC - All systems normal
15:30 UTC - Post-mortem meeting scheduled
```

**Root Cause:**
- Database connection pool misconfiguration
- Connection timeout reduced from 30s to 3s
- High load caused connection exhaustion

**Automated Runbook:**

```bash
#!/bin/bash
# incident-response.sh

set -e

ENVIRONMENT=$1
SERVICE_NAME=$2

echo "🚨 Incident Response Started: $SERVICE_NAME in $ENVIRONMENT"

# 1. Check current status
echo "📊 Current Status:"
kubectl get pods -n $ENVIRONMENT -l app=$SERVICE_NAME

# 2. Check recent deployments
echo "📦 Recent Deployments:"
kubectl rollout history deployment/$SERVICE_NAME -n $ENVIRONMENT

# 3. Fetch error logs
echo "📋 Error Logs (last 100 lines):"
kubectl logs -n $ENVIRONMENT -l app=$SERVICE_NAME --tail=100 | grep ERROR

# 4. Check metrics
echo "📈 Key Metrics:"
curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{service=\"$SERVICE_NAME\"}[5m])"

# 5. Initiate rollback if errors > 5%
ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=rate(http_errors_total{service=\"$SERVICE_NAME\"}[5m])")

if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
    echo "🔄 ERROR RATE TOO HIGH - INITIATING ROLLBACK"
    kubectl rollout undo deployment/$SERVICE_NAME -n $ENVIRONMENT
    
    # Wait for rollout
    kubectl rollout status deployment/$SERVICE_NAME -n $ENVIRONMENT
    
    echo "✅ Rollback completed"
else
    echo "✅ Error rate acceptable"
fi

# 6. Verify service health
echo "🏥 Health Check:"
HEALTH_URL=$(kubectl get svc $SERVICE_NAME -n $ENVIRONMENT -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl -f "http://$HEALTH_URL/health" && echo "✅ Service healthy"

echo "📝 Generate incident report"
```

## 🎯 GitOps Implementation: ArgoCD

**Repository Structure:**

```
k8s-configs/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── replicas.yaml
│   └── production/
│       ├── kustomization.yaml
│       ├── replicas.yaml
│       └── resources.yaml
└── argocd/
    ├── app-staging.yaml
    └── app-production.yaml
```

**ArgoCD Application:**

```yaml
# argocd/app-production.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service-prod
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/company/k8s-configs
    targetRevision: main
    path: overlays/production
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    
    syncOptions:
      - CreateNamespace=true
    
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  # Health checks
  health:
    spec:
      resources:
        - group: apps
          kind: Deployment
          check: |
            hs = {}
            if obj.status.replicas == obj.status.availableReplicas then
              hs.status = "Healthy"
            else
              hs.status = "Progressing"
            end
            return hs
```

## 🎯 Infrastructure as Code: Terraform Best Practices

**Multi-Environment Setup:**

```hcl
# terraform/environments/production/main.tf

terraform {
  required_version = ">= 1.0"
  
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

module "vpc" {
  source = "../../modules/vpc"
  
  environment         = "production"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  tags = local.common_tags
}

module "eks" {
  source = "../../modules/eks"
  
  cluster_name    = "prod-cluster"
  cluster_version = "1.28"
  
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      desired_size = 3
      min_size     = 3
      max_size     = 10
      instance_types = ["t3.large"]
    }
    compute = {
      desired_size = 2
      min_size     = 2
      max_size     = 20
      instance_types = ["c5.2xlarge"]
    }
  }
  
  tags = local.common_tags
}

module "rds" {
  source = "../../modules/rds"
  
  identifier     = "prod-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.r6g.xlarge"
  
  allocated_storage = 100
  storage_encrypted = true
  
  multi_az               = true
  backup_retention_period = 30
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.database_subnet_ids
  
  tags = local.common_tags
}

locals {
  common_tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Team        = "platform"
    CostCenter  = "engineering"
  }
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "database_endpoint" {
  value = module.rds.endpoint
}
```

**Terraform Pipeline:**

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths:
      - 'terraform/**'
  push:
    branches:
      - main
    paths:
      - 'terraform/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.6.0
      
      - name: Terraform Format Check
        run: terraform fmt -check -recursive
      
      - name: Terraform Init
        run: |
          cd terraform/environments/production
          terraform init
      
      - name: Terraform Validate
        run: |
          cd terraform/environments/production
          terraform validate
      
      - name: Terraform Plan
        if: github.event_name == 'pull_request'
        run: |
          cd terraform/environments/production
          terraform plan -out=tfplan
      
      - name: Post Plan to PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('terraform/environments/production/tfplan.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Terraform Plan\n\`\`\`\n${plan}\n\`\`\``
            });
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: |
          cd terraform/environments/production
          terraform apply -auto-approve
```

## 🎯 Monitoring & Alerting: Complete Setup

**Prometheus Configuration:**

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

# Load rules
rule_files:
  - '/etc/prometheus/rules/*.yml'

# Scrape configs
scrape_configs:
  # Kubernetes API server
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

  # Node exporter
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  # Pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

**Alert Rules:**

```yaml
# prometheus/rules/alerts.yml
groups:
  - name: application
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "High error rate detected"
          description: "{{ $labels.service }} has error rate {{ $value | humanizePercentage }}"
      
      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1.0
        for: 10m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "High latency detected"
          description: "{{ $labels.service }} P95 latency is {{ $value }}s"
      
      # Pod restarts
      - alert: PodRestarting
        expr: |
          rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod is restarting"
          description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is restarting"
      
      # High CPU usage
      - alert: HighCPU
        expr: |
          (
            sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)
            /
            sum(container_spec_cpu_quota/container_spec_cpu_period) by (pod)
          ) > 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "Pod {{ $labels.pod }} CPU usage is {{ $value | humanizePercentage }}"
      
      # Database connections
      - alert: DatabaseConnectionsHigh
        expr: |
          pg_stat_activity_count > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Database connections high"
          description: "PostgreSQL has {{ $value }} active connections"
```

## 🎯 Disaster Recovery Drill

**Monthly DR Exercise:**

```bash
#!/bin/bash
# disaster-recovery-drill.sh

echo "🚨 DISASTER RECOVERY DRILL - $(date)"
echo "================================================"

# 1. Backup validation
echo "1️⃣ Validating backups..."
aws s3 ls s3://company-backups/database/ --recursive | tail -1
aws rds describe-db-snapshots --db-instance-identifier prod-db --query 'DBSnapshots[-1]'

# 2. Restore to DR region
echo "2️⃣ Restoring to DR region (us-west-2)..."
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier prod-db-dr-test \
  --db-snapshot-identifier latest-snapshot \
  --region us-west-2

# 3. Deploy application to DR cluster
echo "3️⃣ Deploying to DR cluster..."
kubectl config use-context dr-cluster
kubectl apply -f k8s/production/

# 4. Run smoke tests
echo "4️⃣ Running smoke tests..."
curl -f https://dr.example.com/health
python tests/smoke_tests.py --env=dr

# 5. DNS failover test
echo "5️⃣ Testing DNS failover..."
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456 \
  --change-batch file://dns-failover.json

# 6. Verify traffic routing
echo "6️⃣ Verifying traffic..."
sleep 60
curl -v https://example.com | grep "x-served-by: dr-cluster"

# 7. Rollback
echo "7️⃣ Rolling back to primary..."
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456 \
  --change-batch file://dns-rollback.json

# 8. Cleanup DR resources
echo "8️⃣ Cleaning up DR test..."
kubectl config use-context dr-cluster
kubectl delete -f k8s/production/
aws rds delete-db-instance --db-instance-identifier prod-db-dr-test --skip-final-snapshot --region us-west-2

echo "✅ DR DRILL COMPLETE"
echo "📝 Review metrics and update runbook"
```

## 📊 Key Metrics Dashboard

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Deployment Frequency | 10+/day | 12/day | ✅ |
| Lead Time | < 1 hour | 45 min | ✅ |
| MTTR (Mean Time to Recovery) | < 30 min | 15 min | ✅ |
| Change Failure Rate | < 15% | 8% | ✅ |
| Deployment Success Rate | > 95% | 98.5% | ✅ |
| Test Coverage | > 80% | 87% | ✅ |
| Security Scan Pass Rate | 100% | 100% | ✅ |

## 🎓 Interview Questions

### Q1: How do you handle secrets in Kubernetes?

**Answer:**
1. **Never commit secrets to Git**
2. Use Kubernetes Secrets with encryption at rest
3. Use external secret managers (AWS Secrets Manager, HashiCorp Vault)
4. Rotate secrets regularly
5. Use RBAC to limit access

```yaml
# Using External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-secret
spec:
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
  data:
    - secretKey: password
      remoteRef:
        key: prod/database/password
```

### Q2: Explain blue-green vs canary deployment

**Blue-Green:**
- Two identical environments (blue = current, green = new)
- Switch traffic instantly
- Easy rollback
- Higher cost (2x resources)

**Canary:**
- Gradual rollout (5% → 25% → 50% → 100%)
- Monitor metrics at each stage
- Automatic rollback on errors
- Resource efficient

### Q3: How do you debug a Kubernetes pod that won't start?

```bash
# 1. Check pod status
kubectl get pods -n production

# 2. Describe pod for events
kubectl describe pod my-app-xxx -n production

# 3. Check logs
kubectl logs my-app-xxx -n production --previous

# 4. Check resource limits
kubectl top pod my-app-xxx -n production

# 5. Interactive debug
kubectl debug my-app-xxx -n production -it --image=busybox

# Common issues:
# - ImagePullBackOff: Image doesn't exist or auth issues
# - CrashLoopBackOff: Application crashing on start
# - Pending: Resource constraints or node selector issues
```
