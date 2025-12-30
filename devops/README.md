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

## 🔧 Configuration Management

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
