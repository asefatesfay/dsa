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

**Practice:**
- Build multi-tier applications
- Implement CI/CD pipelines
- Set up monitoring and alerting
- Practice disaster recovery scenarios
