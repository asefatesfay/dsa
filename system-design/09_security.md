# Security

Security must be designed into systems from the start. This covers authentication, authorization, encryption, and common vulnerabilities.

---

## 🔐 Authentication vs Authorization

```
Authentication: Who are you?
  • Login with username/password
  • Verify identity
  • Answer: "You are Alice"

Authorization: What can you do?
  • Check permissions
  • Verify access rights
  • Answer: "Alice can read, but not delete"
```

---

## 🎫 Authentication Methods

### 1. Session-Based Authentication

Traditional server-side sessions with cookies.

```
┌────────┐                    ┌────────┐
│ Client │                    │ Server │
└────┬───┘                    └───┬────┘
     │                            │
     │── POST /login ────────────▶│
     │  {user, pass}              │ 1. Verify credentials
     │                            │ 2. Create session
     │                            │ 3. Store in Redis
     │◀─ Set-Cookie: sid=abc123 ──│
     │                            │
     │── GET /api/data ───────────▶│
     │  Cookie: sid=abc123        │ 1. Check Redis for session
     │                            │ 2. Valid? Return data
     │◀─ 200 OK {data} ───────────│
     │                            │
```

**Implementation:**

```python
from flask import Flask, session, request, jsonify
import redis

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Session store
redis_client = redis.Redis(host='localhost', port=6379)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials
    user = db.get_user(username)
    if user and verify_password(password, user.password_hash):
        # Create session
        session_id = generate_session_id()
        session['user_id'] = user.id
        
        # Store in Redis (expire in 1 hour)
        redis_client.setex(
            f'session:{session_id}',
            3600,
            json.dumps({'user_id': user.id, 'username': username})
        )
        
        return jsonify({'session_id': session_id})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/data')
def get_data():
    session_id = request.cookies.get('session_id')
    
    # Check session
    session_data = redis_client.get(f'session:{session_id}')
    if not session_data:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = json.loads(session_data)
    data = get_user_data(user['user_id'])
    
    return jsonify(data)

@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.cookies.get('session_id')
    
    # Delete session
    redis_client.delete(f'session:{session_id}')
    session.clear()
    
    return jsonify({'message': 'Logged out'})
```

**Advantages:**
- ✅ Server controls sessions (can revoke anytime)
- ✅ Secure (session ID in secure cookie)

**Disadvantages:**
- ❌ Not stateless (requires Redis/database)
- ❌ Harder to scale (session store dependency)
- ❌ CORS complexity for cross-domain

### 2. Token-Based Authentication (JWT)

Stateless authentication using JSON Web Tokens.

```
┌────────┐                    ┌────────┐
│ Client │                    │ Server │
└────┬───┘                    └───┬────┘
     │                            │
     │── POST /login ────────────▶│
     │  {user, pass}              │ 1. Verify credentials
     │                            │ 2. Generate JWT
     │◀─ JWT: eyJ0eXAi... ────────│ 3. Sign with secret
     │  (store in localStorage)   │
     │                            │
     │── GET /api/data ───────────▶│
     │  Authorization: Bearer JWT │ 1. Verify JWT signature
     │                            │ 2. Check expiration
     │◀─ 200 OK {data} ───────────│ 3. Return data
     │                            │
```

**JWT Structure:**

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTY0MDk5NTIwMH0.signature

[         Header         ].[         Payload          ].[Signature]

Header (Base64):
{
  "typ": "JWT",
  "alg": "HS256"
}

Payload (Base64):
{
  "user_id": 123,
  "username": "alice",
  "exp": 1640995200,  // Expiration timestamp
  "iat": 1640991600   // Issued at
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

**Implementation:**

```python
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = 'your-secret-key'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials
    user = db.get_user(username)
    if user and verify_password(password, user.password_hash):
        # Generate JWT
        payload = {
            'user_id': user.id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1),  # Expires in 1 hour
            'iat': datetime.utcnow()  # Issued at
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

def require_auth(f):
    """Decorator to protect routes"""
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            # Verify token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
            request.username = payload['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated

@app.route('/api/data')
@require_auth
def get_data():
    # User authenticated via JWT
    data = get_user_data(request.user_id)
    return jsonify(data)
```

**Advantages:**
- ✅ Stateless (no session storage)
- ✅ Scales easily (no shared state)
- ✅ Works across domains (CORS-friendly)
- ✅ Mobile-friendly

**Disadvantages:**
- ❌ Can't revoke token (until expiration)
- ❌ Larger payload (sent with every request)
- ❌ Token theft risk (if not secured properly)

**Security Best Practices:**
```python
# ✅ Store JWT in httpOnly cookie (not localStorage)
@app.route('/login', methods=['POST'])
def login():
    # ... verify credentials ...
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    response = jsonify({'message': 'Logged in'})
    response.set_cookie(
        'token',
        token,
        httponly=True,  # Prevent JavaScript access (XSS protection)
        secure=True,    # HTTPS only
        samesite='Strict'  # CSRF protection
    )
    return response

# ✅ Short expiration + refresh tokens
# Access token: 15 minutes
# Refresh token: 7 days (stored securely, can be revoked)
```

### 3. OAuth 2.0 (Third-Party Login)

Allow users to login with Google, Facebook, GitHub, etc.

```
┌────────┐              ┌────────┐              ┌────────┐
│  User  │              │  Your  │              │ Google │
│        │              │  App   │              │        │
└───┬────┘              └───┬────┘              └───┬────┘
    │                       │                       │
    │─ Click "Login with Google" ─▶│               │
    │                       │                       │
    │◀─ Redirect to Google ─────────┘               │
    │                                               │
    │─ Login to Google ────────────────────────────▶│
    │  (Enter credentials)                          │
    │                                               │
    │◀─ Authorization code ─────────────────────────│
    │                                               │
    │─ Send code to your app ─▶                     │
    │                       │                       │
    │                       │─ Exchange code for token ─▶│
    │                       │                       │
    │                       │◀─ Access token ───────│
    │                       │                       │
    │                       │─ Get user info ───────▶│
    │                       │◀─ User data ───────────│
    │                       │                       │
    │◀─ Create session/JWT ─│                       │
    │                       │                       │
```

**Implementation (Google OAuth):**

```python
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your-secret-key'

oauth = OAuth(app)

# Configure Google OAuth
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/login/google')
def login_google():
    # Redirect to Google login
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    # Google redirects back with code
    token = google.authorize_access_token()
    
    # Get user info
    user_info = google.parse_id_token(token)
    
    # Create user or login
    user = db.get_or_create_user(
        email=user_info['email'],
        name=user_info['name'],
        google_id=user_info['sub']
    )
    
    # Create session
    session['user_id'] = user.id
    
    return redirect('/dashboard')
```

---

## 🔑 Authorization (Access Control)

### 1. Role-Based Access Control (RBAC)

Users have roles, roles have permissions.

```
┌──────────────────────────────────────┐
│             RBAC Model               │
├──────────────────────────────────────┤
│                                      │
│  Users:                              │
│    • Alice → Admin                   │
│    • Bob → Editor                    │
│    • Carol → Viewer                  │
│                                      │
│  Roles:                              │
│    • Admin → [create, read, update, delete] │
│    • Editor → [create, read, update] │
│    • Viewer → [read]                 │
│                                      │
│  Check: Can Bob delete?              │
│    Bob → Editor → [create, read, update] │
│    ❌ No "delete" permission         │
│                                      │
└──────────────────────────────────────┘
```

**Database Schema:**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE  -- admin, editor, viewer
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE  -- create_post, delete_post, etc.
);

-- Many-to-many: users ↔ roles
CREATE TABLE user_roles (
    user_id INT REFERENCES users(id),
    role_id INT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);

-- Many-to-many: roles ↔ permissions
CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(id),
    permission_id INT REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);
```

**Implementation:**

```python
def require_permission(permission_name):
    """Decorator to check permission"""
    def decorator(f):
        def decorated(*args, **kwargs):
            user_id = request.user_id  # From JWT/session
            
            # Check permission
            if not has_permission(user_id, permission_name):
                return jsonify({'error': 'Forbidden'}), 403
            
            return f(*args, **kwargs)
        
        decorated.__name__ = f.__name__
        return decorated
    return decorator

def has_permission(user_id, permission_name):
    """Check if user has permission"""
    query = """
        SELECT COUNT(*) 
        FROM users u
        JOIN user_roles ur ON u.id = ur.user_id
        JOIN role_permissions rp ON ur.role_id = rp.role_id
        JOIN permissions p ON rp.permission_id = p.id
        WHERE u.id = ? AND p.name = ?
    """
    count = db.execute(query, user_id, permission_name).fetchone()[0]
    return count > 0

@app.route('/api/posts/<post_id>', methods=['DELETE'])
@require_auth
@require_permission('delete_post')
def delete_post(post_id):
    # User has delete_post permission
    db.delete_post(post_id)
    return jsonify({'message': 'Deleted'})
```

### 2. Attribute-Based Access Control (ABAC)

Policies based on attributes (user, resource, environment).

```
Policy: Can user U access resource R?

Example:
  • User: Alice (department=Engineering, level=Senior)
  • Resource: Document (department=Engineering, classification=Confidential)
  • Environment: time=9AM-5PM, location=Office
  
  Rule: Allow if:
    - user.department == resource.department
    - user.level == "Senior"
    - time in 9AM-5PM
    - location == "Office"
```

**Implementation:**

```python
from datetime import datetime

def check_access(user, resource, action):
    """ABAC policy engine"""
    # Rule 1: Same department
    if user.department != resource.department:
        return False
    
    # Rule 2: Senior level for confidential
    if resource.classification == 'Confidential' and user.level != 'Senior':
        return False
    
    # Rule 3: Office hours
    now = datetime.now().hour
    if not (9 <= now < 17):
        return False
    
    # Rule 4: Read vs Write
    if action == 'write' and user.level not in ['Senior', 'Lead']:
        return False
    
    return True

@app.route('/api/documents/<doc_id>')
@require_auth
def get_document(doc_id):
    user = get_user(request.user_id)
    document = db.get_document(doc_id)
    
    if not check_access(user, document, 'read'):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(document)
```

---

## 🔒 Encryption

### 1. Encryption at Rest

Encrypt data stored in databases, files, backups.

```python
from cryptography.fernet import Fernet

# Generate key (store securely!)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt sensitive data before storing
def encrypt_data(plaintext):
    return cipher.encrypt(plaintext.encode())

def decrypt_data(ciphertext):
    return cipher.decrypt(ciphertext).decode()

# Example: Encrypt credit card
credit_card = "1234-5678-9012-3456"
encrypted = encrypt_data(credit_card)
db.save_user_payment(user_id, encrypted)

# Decrypt when needed
encrypted_cc = db.get_user_payment(user_id)
credit_card = decrypt_data(encrypted_cc)
```

**Database-Level Encryption:**

```sql
-- PostgreSQL: Encrypt column
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt when inserting
INSERT INTO users (username, ssn)
VALUES ('alice', pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Decrypt when reading
SELECT username, pgp_sym_decrypt(ssn::bytea, 'encryption_key') AS ssn
FROM users
WHERE username = 'alice';
```

### 2. Encryption in Transit (TLS/SSL)

Always use HTTPS for data transmission (covered in Networking).

```nginx
# Enforce HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Strong SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### 3. Hashing (Passwords)

**Never store passwords in plaintext!**

```python
import bcrypt

# Hash password when user signs up
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# Verify password when user logs in
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    password = data['password']
    
    # Hash password
    password_hash = hash_password(password)
    
    # Store hash (never plaintext!)
    db.create_user(data['username'], password_hash)
    
    return jsonify({'message': 'User created'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = db.get_user(data['username'])
    
    # Verify password against hash
    if user and verify_password(data['password'], user.password_hash):
        # Login successful
        return jsonify({'token': generate_token(user.id)})
    
    return jsonify({'error': 'Invalid credentials'}), 401
```

**Hash Algorithms:**
```
❌ MD5: INSECURE (collision attacks)
❌ SHA1: INSECURE (collision attacks)
⚠️  SHA256: OK but not ideal for passwords
✅ bcrypt: Recommended (slow, salted)
✅ Argon2: Best (memory-hard, PBKDF2 winner)
```

---

## 🛡️ Common Vulnerabilities

### 1. SQL Injection

**Vulnerable Code:**

```python
# ❌ NEVER do this
username = request.args.get('username')
query = f"SELECT * FROM users WHERE username = '{username}'"
db.execute(query)

# Attack: ?username=admin' OR '1'='1
# Query becomes: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# Returns ALL users!
```

**Secure Code:**

```python
# ✅ Use parameterized queries
username = request.args.get('username')
query = "SELECT * FROM users WHERE username = ?"
db.execute(query, username)

# ✅ Or use ORM
user = User.query.filter_by(username=username).first()
```

### 2. Cross-Site Scripting (XSS)

**Vulnerable Code:**

```javascript
// ❌ User input directly in HTML
const username = getQueryParam('name');
document.getElementById('greeting').innerHTML = `Hello, ${username}!`;

// Attack: ?name=<script>alert('XSS')</script>
// Executes malicious JavaScript!
```

**Secure Code:**

```javascript
// ✅ Escape user input
const username = getQueryParam('name');
document.getElementById('greeting').textContent = `Hello, ${username}!`;

// ✅ Or use framework that auto-escapes (React, Vue)
<div>Hello, {username}!</div>  // React escapes by default
```

**Content Security Policy (CSP):**

```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    return response
```

### 3. Cross-Site Request Forgery (CSRF)

**Attack:**

```html
<!-- Malicious site: evil.com -->
<img src="https://bank.com/transfer?to=attacker&amount=1000" />

<!-- If user is logged into bank.com, transfer executes! -->
```

**Defense: CSRF Tokens**

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Form includes CSRF token
@app.route('/transfer', methods=['POST'])
@csrf.protect()
def transfer():
    # Only proceeds if valid CSRF token included
    pass
```

**Double Submit Cookie:**

```python
@app.route('/api/data', methods=['POST'])
def api_endpoint():
    # Check CSRF token in header matches cookie
    token_header = request.headers.get('X-CSRF-Token')
    token_cookie = request.cookies.get('csrf_token')
    
    if token_header != token_cookie:
        return jsonify({'error': 'Invalid CSRF token'}), 403
    
    # Process request
    pass
```

### 4. Rate Limiting (DDoS Prevention)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    # Login logic
    pass

@app.route('/api/expensive')
@limiter.limit("10 per hour")
def expensive_operation():
    # Expensive computation
    pass
```

**Distributed Rate Limiting (Redis):**

```python
import redis
import time

redis_client = redis.Redis()

def rate_limit(key, limit, window):
    """
    Rate limit using sliding window
    key: user ID or IP
    limit: max requests
    window: time window in seconds
    """
    now = time.time()
    
    # Remove old requests
    redis_client.zremrangebyscore(key, 0, now - window)
    
    # Count requests in window
    count = redis_client.zcard(key)
    
    if count >= limit:
        return False  # Rate limited
    
    # Add current request
    redis_client.zadd(key, {str(now): now})
    redis_client.expire(key, window)
    
    return True  # Allowed

@app.route('/api/data')
def get_data():
    if not rate_limit(f"user:{request.user_id}", limit=100, window=3600):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    return jsonify(data)
```

---

## 🔐 API Security Best Practices

### 1. API Keys

```python
# Generate API key for user
import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)

api_key = generate_api_key()
db.save_api_key(user_id, api_key)

# Use API key
@app.route('/api/data')
def get_data():
    api_key = request.headers.get('X-API-Key')
    
    user = db.get_user_by_api_key(api_key)
    if not user:
        return jsonify({'error': 'Invalid API key'}), 401
    
    return jsonify(data)
```

### 2. Input Validation

```python
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True, validate=lambda x: 3 <= len(x) <= 20)
    email = fields.Email(required=True)
    age = fields.Int(validate=lambda x: 0 < x < 150)

@app.route('/api/users', methods=['POST'])
def create_user():
    schema = UserSchema()
    
    try:
        # Validate input
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Create user
    user = db.create_user(**data)
    return jsonify(user), 201
```

### 3. Secure Headers

```python
@app.after_request
def set_secure_headers(response):
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # XSS protection
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # HTTPS only
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # CSP
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    
    return response
```

---

## 🎯 Interview Tips

**Key Points to Cover:**
1. ✅ Authentication vs Authorization
2. ✅ JWT vs Session-based auth
3. ✅ Password hashing (bcrypt/Argon2)
4. ✅ Common vulnerabilities (SQL injection, XSS, CSRF)
5. ✅ Encryption at rest and in transit

**Common Questions:**
- "How would you implement authentication?" → JWT for stateless, sessions for traditional
- "How to store passwords?" → Hash with bcrypt/Argon2, never plaintext
- "What is SQL injection?" → Explain + show parameterized queries
- "How to prevent XSS?" → Escape output, CSP headers
- "JWT vs sessions?" → JWT: stateless, scalable; Sessions: revocable, simpler

**Red Flags:**
- ❌ Storing passwords in plaintext
- ❌ Not validating user input
- ❌ Using HTTP instead of HTTPS
- ❌ Not implementing rate limiting

---

**Next:** [Monitoring & Observability](10_monitoring.md)
