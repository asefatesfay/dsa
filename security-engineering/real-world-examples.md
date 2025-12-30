# Security Engineering - Real-World Examples

## 🎯 Case Study 1: Capital One Data Breach (2019)

**What Happened:**
- Attacker exploited misconfigured WAF
- Accessed 100 million credit applications
- Data stored in S3 buckets

**Root Cause:**
```bash
# Misconfigured IAM role allowed SSRF attack
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name

# Attacker obtained temporary AWS credentials
# Used credentials to list and download S3 buckets
```

**Prevention:**
1. Implement least-privilege IAM policies
2. Disable IMDS v1, use IMDSv2
3. Regular security audits
4. Network segmentation

## 🎯 Case Study 2: SolarWinds Supply Chain Attack (2020)

**Attack Vector:**
- Compromised build system
- Malicious code in software update
- 18,000 organizations affected

**Lessons:**
- Implement software supply chain security
- Code signing and verification
- Build system isolation
- Dependency scanning

**Implementation:**

```yaml
# GitHub Actions - Secure build pipeline
name: Secure Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    
    steps:
      - uses: actions/checkout@v3
      
      # Verify dependencies
      - name: Dependency Review
        uses: actions/dependency-review-action@v3
      
      # SBOM (Software Bill of Materials)
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: spdx-json
      
      # Sign artifacts
      - name: Sign with Cosign
        uses: sigstore/cosign-installer@v3
      - run: |
          cosign sign --key cosign.key $IMAGE_URI
```

## 🎯 Interview Question: Design Zero-Trust Architecture

**Answer:**

```
┌─────────────────────────────────────────────────┐
│          Internet / External Users               │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   Identity Provider  │
         │   (Okta, Auth0)      │
         │   - MFA required     │
         └─────────┬────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   Zero Trust Gateway │
         │   - Device check     │
         │   - Context aware    │
         └─────────┬────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Service A│ │ Service B│ │ Service C│
│ mTLS     │ │ mTLS     │ │ mTLS     │
│ Encrypted│ │ Encrypted│ │ Encrypted│
└──────────┘ └──────────┘ └──────────┘
```

**Key Principles:**
1. Never trust, always verify
2. Least privilege access
3. Assume breach
4. Inspect all traffic
5. Log everything

## 🛡️ Practical Security Checklist

### Pre-Deployment
- [ ] Code review completed
- [ ] SAST scan passed
- [ ] Dependency scan passed
- [ ] Container scan passed
- [ ] Secrets not in code
- [ ] Input validation implemented
- [ ] Authentication/authorization tested
- [ ] Rate limiting configured
- [ ] Logging enabled
- [ ] Error handling secure (no info leakage)

### Deployment
- [ ] TLS 1.3 configured
- [ ] Security headers set
- [ ] WAF rules active
- [ ] DDoS protection enabled
- [ ] Backup/recovery tested
- [ ] Monitoring alerts configured
- [ ] Incident response plan ready

### Post-Deployment
- [ ] Penetration test scheduled
- [ ] Bug bounty program active
- [ ] Security training completed
- [ ] Regular patching schedule
- [ ] Access reviews quarterly
- [ ] Disaster recovery drills
