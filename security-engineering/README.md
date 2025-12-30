# Security Engineering

Application security, infrastructure security, and compliance for senior engineers.

---

## 📋 Core Security Domains

### 1. **Authentication & Authorization**

#### OAuth 2.0 Flow
```javascript
// Authorization Code Flow (most secure for web apps)
const express = require('express');
const axios = require('axios');
const crypto = require('crypto');

const app = express();

// Step 1: Redirect user to OAuth provider
app.get('/login', (req, res) => {
  const state = crypto.randomBytes(16).toString('hex');
  const codeVerifier = crypto.randomBytes(32).toString('base64url');
  const codeChallenge = crypto
    .createHash('sha256')
    .update(codeVerifier)
    .digest('base64url');
  
  // Store state and codeVerifier in session
  req.session.state = state;
  req.session.codeVerifier = codeVerifier;
  
  const authUrl = new URL('https://oauth.provider.com/authorize');
  authUrl.searchParams.append('response_type', 'code');
  authUrl.searchParams.append('client_id', process.env.CLIENT_ID);
  authUrl.searchParams.append('redirect_uri', 'https://myapp.com/callback');
  authUrl.searchParams.append('scope', 'openid profile email');
  authUrl.searchParams.append('state', state);
  authUrl.searchParams.append('code_challenge', codeChallenge);
  authUrl.searchParams.append('code_challenge_method', 'S256');
  
  res.redirect(authUrl.toString());
});

// Step 2: Handle callback and exchange code for token
app.get('/callback', async (req, res) => {
  const { code, state } = req.query;
  
  // Verify state to prevent CSRF
  if (state !== req.session.state) {
    return res.status(403).send('Invalid state parameter');
  }
  
  try {
    const tokenResponse = await axios.post('https://oauth.provider.com/token', {
      grant_type: 'authorization_code',
      code: code,
      redirect_uri: 'https://myapp.com/callback',
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      code_verifier: req.session.codeVerifier
    });
    
    const { access_token, refresh_token, id_token } = tokenResponse.data;
    
    // Verify and decode JWT
    const decoded = verifyJWT(id_token);
    req.session.user = decoded;
    req.session.accessToken = access_token;
    req.session.refreshToken = refresh_token;
    
    res.redirect('/dashboard');
  } catch (error) {
    console.error('Token exchange failed:', error);
    res.status(500).send('Authentication failed');
  }
});
```

#### JWT Implementation
```javascript
const jwt = require('jsonwebtoken');
const { promisify } = require('util');

// Generate JWT
function generateToken(user) {
  const payload = {
    sub: user.id,
    email: user.email,
    role: user.role,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (60 * 60) // 1 hour
  };
  
  return jwt.sign(payload, process.env.JWT_SECRET, {
    algorithm: 'HS256'
  });
}

// Verify JWT middleware
async function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(403).json({ error: 'Invalid token' });
  }
}

// Role-based access control
function authorize(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
}

// Usage
app.get('/admin', authenticateToken, authorize('admin'), (req, res) => {
  res.json({ message: 'Admin area' });
});
```

---

### 2. **Encryption**

#### Encryption at Rest
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

class DataEncryptor:
    def __init__(self, password: str):
        # Derive key from password using PBKDF2
        salt = os.urandom(16)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
        self.salt = salt
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt sensitive data before storing"""
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt data when retrieving"""
        return self.cipher.decrypt(encrypted_data).decode()

# Usage for database fields
encryptor = DataEncryptor(os.environ['ENCRYPTION_KEY'])

# Before saving to DB
user.ssn = encryptor.encrypt("123-45-6789")
user.credit_card = encryptor.encrypt("4111-1111-1111-1111")

# When reading from DB
ssn = encryptor.decrypt(user.ssn)
```

#### TLS/SSL Configuration
```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    # SSL certificates
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # Strong SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    
    # SSL session cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'" always;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

### 3. **OWASP Top 10**

#### SQL Injection Prevention
```python
# ❌ VULNERABLE - Never do this!
def get_user_bad(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # SQL injection vulnerability!

# ✅ SECURE - Use parameterized queries
def get_user_secure(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))  # Safe from SQL injection

# ✅ SECURE - Using ORM (SQLAlchemy)
from sqlalchemy.orm import Session
from models import User

def get_user_orm(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
```

#### Cross-Site Scripting (XSS) Prevention
```javascript
// ❌ VULNERABLE - Direct innerHTML
document.getElementById('output').innerHTML = userInput;

// ✅ SECURE - Use textContent
document.getElementById('output').textContent = userInput;

// ✅ SECURE - Sanitize HTML
import DOMPurify from 'dompurify';
const cleanHTML = DOMPurify.sanitize(userInput);
document.getElementById('output').innerHTML = cleanHTML;

// Backend: Set Content Security Policy
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline' https://trusted-cdn.com"
  );
  next();
});
```

#### Cross-Site Request Forgery (CSRF) Prevention
```javascript
const csrf = require('csurf');
const cookieParser = require('cookie-parser');

app.use(cookieParser());
app.use(csrf({ cookie: true }));

// Send CSRF token to client
app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

// Verify CSRF token on POST
app.post('/transfer', (req, res) => {
  // Token automatically verified by csrf middleware
  const { amount, recipient } = req.body;
  // Process transfer...
});

// Frontend: Include CSRF token
<form method="POST" action="/transfer">
  <input type="hidden" name="_csrf" value="{{csrfToken}}">
  <input name="amount" type="number">
  <button type="submit">Transfer</button>
</form>
```

#### Input Validation
```javascript
const Joi = require('joi');

// Define validation schema
const userSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).pattern(/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])/).required(),
  age: Joi.number().integer().min(18).max(120),
  role: Joi.string().valid('user', 'admin', 'moderator')
});

app.post('/register', async (req, res) => {
  try {
    // Validate input
    const validatedData = await userSchema.validateAsync(req.body, {
      abortEarly: false
    });
    
    // Hash password
    const hashedPassword = await bcrypt.hash(validatedData.password, 12);
    
    // Create user
    const user = await User.create({
      ...validatedData,
      password: hashedPassword
    });
    
    res.json({ success: true, userId: user.id });
  } catch (error) {
    if (error.isJoi) {
      return res.status(400).json({ errors: error.details });
    }
    res.status(500).json({ error: 'Server error' });
  }
});
```

---

### 4. **API Security**

#### Rate Limiting
```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

const redisClient = new Redis({
  host: 'localhost',
  port: 6379
});

// General API rate limiter
const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:api:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false
});

// Stricter limit for authentication
const authLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts
  skipSuccessfulRequests: true
});

app.use('/api/', apiLimiter);
app.use('/auth/login', authLimiter);
```

#### API Key Authentication
```javascript
const crypto = require('crypto');

// Generate API key
function generateApiKey() {
  return crypto.randomBytes(32).toString('hex');
}

// Store in database with hash
async function createApiKey(userId) {
  const apiKey = generateApiKey();
  const hashedKey = crypto
    .createHash('sha256')
    .update(apiKey)
    .digest('hex');
  
  await db.apiKeys.create({
    userId,
    keyHash: hashedKey,
    createdAt: new Date()
  });
  
  return apiKey; // Return only once to user
}

// Verify API key middleware
async function verifyApiKey(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  
  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }
  
  const hashedKey = crypto
    .createHash('sha256')
    .update(apiKey)
    .digest('hex');
  
  const keyRecord = await db.apiKeys.findOne({
    where: { keyHash: hashedKey }
  });
  
  if (!keyRecord) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  
  req.userId = keyRecord.userId;
  next();
}
```

---

### 5. **Container Security**

#### Docker Security Best Practices
```dockerfile
# Use specific version tags (not 'latest')
FROM node:18.17-alpine3.18

# Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY --chown=nodejs:nodejs package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY --chown=nodejs:nodejs . .

# Remove unnecessary packages
RUN apk del apk-tools

# Use read-only filesystem where possible
VOLUME ["/app/data"]

# Drop all capabilities except required ones
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

EXPOSE 3000

CMD ["node", "index.js"]
```

#### Kubernetes Security
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  # Security context for pod
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  
  containers:
  - name: app
    image: myapp:v1.0.0
    
    # Container security context
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE
    
    # Resource limits
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "256Mi"
        cpu: "500m"
    
    # Read-only volume mounts
    volumeMounts:
    - name: config
      mountPath: /app/config
      readOnly: true
    - name: tmp
      mountPath: /tmp
  
  volumes:
  - name: config
    configMap:
      name: app-config
  - name: tmp
    emptyDir: {}
```

---

### 6. **Secrets Management**

#### HashiCorp Vault
```python
import hvac
import os

class SecretManager:
    def __init__(self):
        self.client = hvac.Client(
            url=os.getenv('VAULT_ADDR'),
            token=os.getenv('VAULT_TOKEN')
        )
    
    def get_secret(self, path: str) -> dict:
        """Retrieve secret from Vault"""
        response = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point='secret'
        )
        return response['data']['data']
    
    def set_secret(self, path: str, data: dict):
        """Store secret in Vault"""
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=data,
            mount_point='secret'
        )
    
    def get_database_credentials(self, role: str) -> dict:
        """Get dynamic database credentials"""
        response = self.client.secrets.database.generate_credentials(
            name=role,
            mount_point='database'
        )
        return {
            'username': response['data']['username'],
            'password': response['data']['password']
        }

# Usage
secrets = SecretManager()
db_creds = secrets.get_database_credentials('readonly-role')

# Credentials auto-expire after lease duration
```

#### AWS Secrets Manager
```python
import boto3
import json

def get_secret(secret_name: str, region: str = 'us-east-1'):
    client = boto3.client('secretsmanager', region_name=region)
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise

# Usage
db_config = get_secret('prod/database/credentials')
api_key = get_secret('prod/api/external-service')
```

---

## 🎯 Security Checklist for Senior Engineers

### **Application Security:**
- ✅ Input validation on all user inputs
- ✅ Output encoding to prevent XSS
- ✅ Parameterized queries to prevent SQL injection
- ✅ CSRF tokens on state-changing operations
- ✅ Secure session management
- ✅ Strong password policies (min 8 chars, complexity)
- ✅ Multi-factor authentication for sensitive operations

### **API Security:**
- ✅ Rate limiting implemented
- ✅ API authentication (JWT, OAuth, API keys)
- ✅ CORS properly configured
- ✅ Request/response validation
- ✅ API versioning
- ✅ Audit logging

### **Infrastructure Security:**
- ✅ TLS 1.2+ for all communications
- ✅ Network segmentation (VPC, subnets)
- ✅ Firewall rules (least privilege)
- ✅ Security groups properly configured
- ✅ Regular security patches
- ✅ Intrusion detection systems

### **Data Security:**
- ✅ Encryption at rest (databases, files)
- ✅ Encryption in transit (TLS/SSL)
- ✅ Secure key management
- ✅ PII data protection
- ✅ Data retention policies
- ✅ Secure backup procedures

### **Container/Kubernetes Security:**
- ✅ Run as non-root user
- ✅ Read-only filesystems
- ✅ Resource limits set
- ✅ Security contexts configured
- ✅ Image scanning (Trivy, Clair)
- ✅ Pod Security Policies

---

## 📚 Learning Resources

**Certifications:**
- Certified Information Systems Security Professional (CISSP)
- AWS Certified Security - Specialty
- Certified Ethical Hacker (CEH)
- GIAC Security Essentials (GSEC)

**Practice:**
- OWASP WebGoat (vulnerable web app for practice)
- HackTheBox (penetration testing practice)
- TryHackMe (security training platform)
- PortSwigger Web Security Academy

**Books:**
- "The Web Application Hacker's Handbook"
- "Cryptography Engineering"
- "Security Engineering" - Ross Anderson
