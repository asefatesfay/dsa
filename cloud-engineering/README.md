# Cloud Engineering - AWS/Azure/GCP

Comprehensive guide for cloud architecture, deployment, and operations.

---

## 📋 Topics Covered

### 1. **AWS Core Services**
- **Compute:** EC2, Lambda, ECS/EKS, Fargate
- **Storage:** S3, EBS, EFS, Glacier
- **Database:** RDS, DynamoDB, Aurora, ElastiCache
- **Networking:** VPC, Route53, CloudFront, API Gateway
- **Security:** IAM, KMS, Secrets Manager, WAF
- **Monitoring:** CloudWatch, X-Ray, CloudTrail

### 2. **Azure Core Services**
- **Compute:** Virtual Machines, Azure Functions, AKS
- **Storage:** Blob Storage, Azure Files, Data Lake
- **Database:** Azure SQL, Cosmos DB, Azure Cache
- **Networking:** Virtual Network, Application Gateway, Front Door
- **Security:** Azure AD, Key Vault, Security Center
- **Monitoring:** Azure Monitor, Application Insights

### 3. **GCP Core Services**
- **Compute:** Compute Engine, Cloud Functions, GKE
- **Storage:** Cloud Storage, Persistent Disk, Filestore
- **Database:** Cloud SQL, Firestore, Cloud Spanner
- **Networking:** VPC, Cloud CDN, Cloud DNS
- **Security:** IAM, Secret Manager, Security Command Center
- **Monitoring:** Cloud Monitoring, Cloud Logging

---

## 🌟 Real-World Example: E-Commerce Platform on AWS

### Scenario
Deploy a high-traffic e-commerce platform handling 10,000 requests/second with 99.99% uptime.

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                        CloudFront CDN                        │
│                  (Static assets, edge caching)               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Load Balancer (ALB)                 │
│           (SSL termination, health checks)                   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌─────────┐         ┌─────────┐         ┌─────────┐
  │  ECS     │         │  ECS    │         │  ECS    │
  │ Task 1   │         │ Task 2  │         │ Task 3  │
  │(us-east) │         │(us-east)│         │(us-west)│
  └─────────┘         └─────────┘         └─────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
        ┌───────────────────────────────────────┐
        │     ElastiCache Redis Cluster         │
        │  (Session store, product cache)       │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │   RDS PostgreSQL Multi-AZ             │
        │  Primary (us-east-1a)                 │
        │  Standby (us-east-1b)                 │
        │  Read Replicas (3)                    │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │         S3 Bucket                     │
        │  (Product images, invoices)           │
        └───────────────────────────────────────┘
```

### Cost Breakdown (Monthly)
```
Service                    | Quantity      | Cost/Month
─────────────────────────────────────────────────────────
EC2 (ECS tasks)           | 10 × t3.large | $730
RDS PostgreSQL (db.r5.2xl)| 1 primary     | $1,200
RDS Read Replicas         | 3 × db.r5.large| $1,800
ElastiCache Redis         | r6g.xlarge    | $280
Application Load Balancer | 1             | $23
S3 Storage                | 5 TB          | $115
CloudFront                | 10 TB transfer| $850
Route53                   | 1 hosted zone | $1
CloudWatch Logs           | 100 GB/month  | $50
─────────────────────────────────────────────────────────
Total                                      | $5,049/month
```

### Implementation Steps

#### Step 1: VPC Network Setup
```hcl
# Create VPC with public and private subnets across 3 AZs
resource "aws_vpc" "ecommerce" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "ecommerce-vpc"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.ecommerce.id

  tags = {
    Name = "ecommerce-igw"
  }
}

# Public subnets (for ALB)
resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.ecommerce.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}"
    Tier = "public"
  }
}

# Private subnets (for ECS tasks)
resource "aws_subnet" "private_app" {
  count             = 3
  vpc_id            = aws_vpc.ecommerce.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-app-subnet-${count.index + 1}"
    Tier = "application"
  }
}

# Database subnets (isolated)
resource "aws_subnet" "private_db" {
  count             = 3
  vpc_id            = aws_vpc.ecommerce.id
  cidr_block        = "10.0.${count.index + 20}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-db-subnet-${count.index + 1}"
    Tier = "database"
  }
}

# NAT Gateway for private subnets
resource "aws_eip" "nat" {
  count  = 3
  domain = "vpc"

  tags = {
    Name = "nat-eip-${count.index + 1}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "nat-gateway-${count.index + 1}"
  }
}
```

#### Step 2: RDS Database Setup
```hcl
resource "aws_db_subnet_group" "main" {
  name       = "ecommerce-db-subnet-group"
  subnet_ids = aws_subnet.private_db[*].id

  tags = {
    Name = "ecommerce-db-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  identifier     = "ecommerce-postgres"
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.r5.2xlarge"

  allocated_storage     = 500
  storage_type          = "gp3"
  iops                  = 12000
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.rds.arn

  db_name  = "ecommerce"
  username = "admin"
  password = random_password.db_password.result

  # High availability
  multi_az               = true
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  # Backups
  backup_retention_period   = 30
  backup_window             = "03:00-04:00"
  maintenance_window        = "mon:04:00-mon:05:00"
  copy_tags_to_snapshot     = true
  skip_final_snapshot       = false
  final_snapshot_identifier = "ecommerce-postgres-final-snapshot"

  # Performance Insights
  performance_insights_enabled    = true
  performance_insights_kms_key_id = aws_kms_key.rds.arn
  performance_insights_retention_period = 7

  # Monitoring
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  monitoring_interval             = 60
  monitoring_role_arn             = aws_iam_role.rds_monitoring.arn

  tags = {
    Name        = "ecommerce-postgres"
    Environment = "production"
  }
}

# Read replicas
resource "aws_db_instance" "postgres_replica" {
  count              = 3
  identifier         = "ecommerce-postgres-replica-${count.index + 1}"
  replicate_source_db = aws_db_instance.postgres.identifier
  instance_class     = "db.r5.large"

  publicly_accessible = false
  skip_final_snapshot = true

  tags = {
    Name = "ecommerce-postgres-replica-${count.index + 1}"
    Role = "read-replica"
  }
}
```

#### Step 3: ECS Fargate Service
```hcl
resource "aws_ecs_cluster" "main" {
  name = "ecommerce-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "ecommerce-cluster"
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "ecommerce-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = "app"
    image = "${aws_ecr_repository.app.repository_url}:latest"

    portMappings = [{
      containerPort = 3000
      protocol      = "tcp"
    }]

    environment = [
      { name = "NODE_ENV", value = "production" },
      { name = "DB_HOST", value = aws_db_instance.postgres.address },
      { name = "REDIS_HOST", value = aws_elasticache_replication_group.main.primary_endpoint_address }
    ]

    secrets = [
      {
        name      = "DB_PASSWORD"
        valueFrom = aws_secretsmanager_secret.db_password.arn
      },
      {
        name      = "JWT_SECRET"
        valueFrom = aws_secretsmanager_secret.jwt_secret.arn
      }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.app.name
        "awslogs-region"        = "us-east-1"
        "awslogs-stream-prefix" = "ecs"
      }
    }

    healthCheck = {
      command     = ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 60
    }
  }])
}

resource "aws_ecs_service" "app" {
  name            = "ecommerce-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 10
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private_app[*].id
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 3000
  }

  # Auto scaling
  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  depends_on = [aws_lb_listener.https]
}

# Auto Scaling
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = 50
  min_capacity       = 10
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ecs_cpu" {
  name               = "cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}
```

#### Step 4: Application Load Balancer
```hcl
resource "aws_lb" "main" {
  name               = "ecommerce-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = true
  enable_http2               = true
  enable_cross_zone_load_balancing = true

  access_logs {
    bucket  = aws_s3_bucket.alb_logs.id
    prefix  = "alb"
    enabled = true
  }

  tags = {
    Name = "ecommerce-alb"
  }
}

resource "aws_lb_target_group" "app" {
  name        = "ecommerce-tg"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.ecommerce.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  deregistration_delay = 30

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Redirect HTTP to HTTPS
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}
```

#### Step 5: ElastiCache Redis
```hcl
resource "aws_elasticache_subnet_group" "main" {
  name       = "ecommerce-cache-subnet"
  subnet_ids = aws_subnet.private_app[*].id
}

resource "aws_elasticache_replication_group" "main" {
  replication_group_id       = "ecommerce-redis"
  replication_group_description = "Redis cluster for sessions and caching"
  
  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.r6g.xlarge"
  number_cache_clusters = 3
  
  port                       = 6379
  parameter_group_name       = aws_elasticache_parameter_group.main.name
  subnet_group_name          = aws_elasticache_subnet_group.main.name
  security_group_ids         = [aws_security_group.redis.id]
  
  # High availability
  automatic_failover_enabled = true
  multi_az_enabled          = true
  
  # Backups
  snapshot_retention_limit   = 7
  snapshot_window            = "03:00-05:00"
  maintenance_window         = "sun:05:00-sun:07:00"
  
  # Encryption
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = random_password.redis_auth.result
  
  # Monitoring
  notification_topic_arn = aws_sns_topic.alerts.arn
  
  tags = {
    Name = "ecommerce-redis"
  }
}
```

### Monitoring & Alerts

```hcl
# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "ecs_cpu_high" {
  alarm_name          = "ecommerce-ecs-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "ECS CPU utilization is too high"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.app.name
  }
}

resource "aws_cloudwatch_metric_alarm" "rds_cpu_high" {
  alarm_name          = "ecommerce-rds-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "RDS CPU utilization is too high"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.postgres.id
  }
}

resource "aws_cloudwatch_metric_alarm" "alb_5xx_errors" {
  alarm_name          = "ecommerce-alb-5xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "Too many 5xx errors from ALB"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    LoadBalancer = aws_lb.main.arn_suffix
  }
}
```

### Disaster Recovery

```bash
#!/bin/bash
# Automated backup script

# Snapshot RDS
aws rds create-db-snapshot \
  --db-instance-identifier ecommerce-postgres \
  --db-snapshot-identifier ecommerce-postgres-$(date +%Y%m%d-%H%M%S)

# Copy to DR region
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier ecommerce-postgres-latest \
  --target-db-snapshot-identifier ecommerce-postgres-dr \
  --source-region us-east-1 \
  --region us-west-2

# Backup S3 to Glacier
aws s3 sync s3://ecommerce-prod s3://ecommerce-backup \
  --storage-class GLACIER

# Export ElastiCache snapshot
aws elasticache create-snapshot \
  --replication-group-id ecommerce-redis \
  --snapshot-name ecommerce-redis-$(date +%Y%m%d)
```

---

## 🏗️ Infrastructure as Code (IaC)

### Terraform
```hcl
# Example: AWS VPC with public/private subnets
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  
  tags = {
    Name = "production-vpc"
    Environment = "prod"
  }
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "private-subnet-${count.index + 1}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "main-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "public-route-table"
  }
}
```

### CloudFormation (AWS)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Auto Scaling Web Application'

Parameters:
  KeyName:
    Description: EC2 Key Pair
    Type: AWS::EC2::KeyPair::KeyName
  
  InstanceType:
    Description: EC2 instance type
    Type: String
    Default: t3.micro

Resources:
  LaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: web-app-template
      LaunchTemplateData:
        ImageId: !Ref LatestAmiId
        InstanceType: !Ref InstanceType
        KeyName: !Ref KeyName
        SecurityGroupIds:
          - !Ref WebServerSecurityGroup
        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            yum update -y
            yum install -y httpd
            systemctl start httpd
            systemctl enable httpd
  
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      LaunchTemplate:
        LaunchTemplateId: !Ref LaunchTemplate
        Version: !GetAtt LaunchTemplate.LatestVersionNumber
      TargetGroupARNs:
        - !Ref TargetGroup
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
```

### Azure ARM Templates
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2021-02-01",
      "name": "[parameters('webAppName')]",
      "location": "[parameters('location')]",
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', parameters('appServicePlanName'))]",
        "siteConfig": {
          "linuxFxVersion": "NODE|14-lts",
          "appSettings": [
            {
              "name": "WEBSITES_ENABLE_APP_SERVICE_STORAGE",
              "value": "false"
            }
          ]
        }
      }
    }
  ]
}
```

---

## 🐳 Containerization & Orchestration

### Docker Best Practices
```dockerfile
# Multi-stage build for Node.js app
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

USER nodejs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: myregistry/web-app:v1.2.3
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: NODE_ENV
          value: "production"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
---
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 📊 Observability & Monitoring

### CloudWatch Alarms
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Create CPU alarm
cloudwatch.put_metric_alarm(
    AlarmName='high-cpu-utilization',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=80.0,
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:us-west-2:123456789:alerts'],
    AlarmDescription='Alert when CPU exceeds 80%',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-1234567890abcdef0'
        },
    ]
)
```

### Prometheus + Grafana
```yaml
# Prometheus configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
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
```

---

## 🎯 Senior Engineer Focus Areas

### 1. **Cost Optimization**
- Reserved instances vs spot instances
- Right-sizing resources
- Storage tiering strategies
- Data transfer optimization

### 2. **High Availability Architecture**
- Multi-region deployments
- Disaster recovery planning
- Failover strategies
- Health checks and auto-recovery

### 3. **Security Best Practices**
- Principle of least privilege
- Encryption at rest and in transit
- Network segmentation
- Secrets management

### 4. **Performance Optimization**
- CDN configuration
- Caching strategies
- Database query optimization
- Auto-scaling policies

### 5. **Compliance & Governance**
- Tagging strategies
- Cost allocation
- Access auditing
- Compliance frameworks (SOC2, HIPAA, PCI-DSS)

---

## 📚 Learning Resources

**AWS:**
- AWS Solutions Architect Professional
- AWS Well-Architected Framework
- AWS Whitepapers

**Azure:**
- Azure Solutions Architect Expert
- Azure Architecture Center

**GCP:**
- Google Cloud Professional Architect
- Google Cloud Architecture Framework

**Practice Labs:**

1. **Lab 1: Multi-Region Active-Active Setup**
   - Deploy application in us-east-1 and eu-west-1
   - Configure Route53 latency-based routing
   - Set up cross-region RDS read replicas
   - Implement S3 cross-region replication

2. **Lab 2: Zero-Downtime Blue-Green Deployment**
   - Create two identical ECS services (blue/green)
   - Deploy new version to green environment
   - Run automated tests
   - Switch ALB target group to green
   - Keep blue as rollback option

3. **Lab 3: Cost Optimization Challenge**
   - Analyze CloudWatch Cost Explorer
   - Implement auto-scaling policies
   - Convert to Spot Instances where possible
   - Enable S3 Intelligent-Tiering
   - Target: Reduce costs by 30%

4. **Lab 4: Security Hardening**
   - Enable AWS GuardDuty
   - Configure AWS WAF rules
   - Implement least-privilege IAM policies
   - Enable VPC Flow Logs
   - Set up AWS Security Hub

5. **Lab 5: Disaster Recovery Drill**
   - Simulate region failure
   - Restore from RDS snapshot in different region
   - Recover from S3 versioning
   - Test RPO (Recovery Point Objective) < 1 hour
   - Test RTO (Recovery Time Objective) < 4 hours

**Real Interview Questions:**

**Q1:** "How would you design a system to handle a sudden 10x traffic spike (like Black Friday)?"  
**A:** 
- Use auto-scaling groups with predictive scaling
- Pre-warm load balancers (contact AWS support)
- Enable CloudFront caching (cache hit ratio >90%)
- Use ElastiCache for database query caching
- Implement SQS queues for async processing
- Consider DynamoDB for better write scalability
- Enable API Gateway throttling to protect backend

**Q2:** "Your RDS database is at 90% CPU. How do you troubleshoot and fix this?"  
**A:**
1. **Immediate**: Enable Performance Insights, check slow query log
2. **Short-term**: Add read replicas, offload read traffic
3. **Medium-term**: 
   - Optimize queries (add indexes, rewrite N+1 queries)
   - Implement connection pooling (RDS Proxy)
   - Enable query caching in application layer
4. **Long-term**: Consider sharding or Aurora Serverless

**Q3:** "How do you ensure zero-downtime deployments?"  
**A:**
- Use blue-green deployment or rolling updates
- Implement health checks (readiness & liveness probes)
- Configure ALB deregistration delay (30-60s)
- Ensure backward-compatible API changes
- Use feature flags for gradual rollout
- Always keep previous version for instant rollback
- Test deployment process in staging first

**Q4:** "Explain your approach to multi-region failover."  
**A:**
```
Primary Region (us-east-1)     Secondary Region (us-west-2)
─────────────────────────      ──────────────────────────────
ECS Service (active)           ECS Service (standby)
RDS Primary                    RDS Read Replica (promoted on fail)
ElastiCache                    ElastiCache (separate cluster)
S3 Bucket                      S3 Bucket (CRR enabled)
                
           Route53 Health Check
                    │
      ┌─────────────┴──────────────┐
      │ Failover if 3 consecutive  │
      │ health check failures      │
      └────────────────────────────┘
```

- Use Route53 health checks with failover routing
- Replicate data: S3 CRR, RDS cross-region replicas
- Keep secondary region warm (min instances running)
- Automate failover with Lambda functions
- Regular DR drills (quarterly)

**Practice:**
- Build multi-tier applications
- Implement CI/CD pipelines with AWS CodePipeline
- Set up comprehensive monitoring and alerting
- Practice disaster recovery scenarios monthly
- Participate in AWS Game Days
