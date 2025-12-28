# Monitoring & Observability

Monitoring helps you understand what's happening in your system. Observability lets you debug complex distributed systems.

---

## 📊 Monitoring vs Observability

```
Monitoring: "Is the system working?"
  • Pre-defined metrics
  • Known failure modes
  • Dashboards and alerts
  • Example: CPU usage > 80%

Observability: "Why is the system broken?"
  • Explore unknown unknowns
  • Debug complex issues
  • Logs, metrics, traces
  • Example: Why is this specific request slow?
```

---

## 📈 The Three Pillars of Observability

### 1. Metrics (Numbers)

Time-series data: counters, gauges, histograms.

**Types of Metrics:**

```
Counter: Monotonically increasing
  • Total HTTP requests
  • Total errors
  • Total bytes transferred

Gauge: Can go up or down
  • Current CPU usage
  • Active connections
  • Queue depth

Histogram: Distribution of values
  • Request latency (p50, p95, p99)
  • Response sizes
  • Database query times
```

**Prometheus Example:**

```python
from prometheus_client import Counter, Gauge, Histogram, generate_latest

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

active_connections = Gauge(
    'active_connections',
    'Number of active database connections'
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Instrument code
@app.route('/api/users')
@request_duration.labels(method='GET', endpoint='/api/users').time()
def get_users():
    try:
        users = db.query("SELECT * FROM users")
        
        # Update metrics
        http_requests_total.labels(
            method='GET',
            endpoint='/api/users',
            status=200
        ).inc()
        
        active_connections.set(db.get_active_connections())
        
        return jsonify(users)
    
    except Exception as e:
        http_requests_total.labels(
            method='GET',
            endpoint='/api/users',
            status=500
        ).inc()
        raise

# Metrics endpoint (Prometheus scrapes this)
@app.route('/metrics')
def metrics():
    return generate_latest()
```

**Prometheus Query (PromQL):**

```promql
# Request rate (per second)
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Requests by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)
```

**Grafana Dashboard:**

```
┌────────────────────────────────────────────────────┐
│              System Overview Dashboard             │
├────────────────────────────────────────────────────┤
│                                                    │
│  [Request Rate]          [Error Rate]             │
│   1,234 req/s             0.5%                     │
│   ▲ Chart                 ▲ Chart                  │
│                                                    │
│  [Response Time (p95)]   [Active Connections]     │
│   250ms                   45                       │
│   ▲ Chart                 ▲ Chart                  │
│                                                    │
│  [CPU Usage]             [Memory Usage]            │
│   65%                     72%                      │
│   ▲ Chart                 ▲ Chart                  │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 2. Logs (Events)

Structured records of what happened.

**Log Levels:**

```
DEBUG: Detailed diagnostic information
INFO: General informational messages
WARNING: Something unexpected, but system still works
ERROR: Error occurred, but system continues
CRITICAL: System failure, immediate action required
```

**Structured Logging (JSON):**

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_obj['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_obj['request_id'] = record.request_id
        
        return json.dumps(log_obj)

# Configure logging
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Log with context
@app.route('/api/users/<user_id>')
def get_user(user_id):
    logger.info(
        'Fetching user',
        extra={'user_id': user_id, 'request_id': request.id}
    )
    
    try:
        user = db.get_user(user_id)
        
        logger.info(
            'User fetched successfully',
            extra={'user_id': user_id, 'request_id': request.id}
        )
        
        return jsonify(user)
    
    except Exception as e:
        logger.error(
            'Failed to fetch user',
            extra={
                'user_id': user_id,
                'request_id': request.id,
                'error': str(e)
            },
            exc_info=True
        )
        raise
```

**Log Output:**

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "message": "Fetching user",
  "module": "api",
  "function": "get_user",
  "line": 45,
  "user_id": "123",
  "request_id": "abc-def-ghi"
}
```

**Centralized Logging (ELK Stack):**

```
┌──────────┐      ┌──────────┐      ┌──────────────┐
│  Service │─────▶│Filebeat/ │─────▶│Elasticsearch │
│   Logs   │      │Fluentd   │      │   (Store)    │
└──────────┘      └──────────┘      └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │   Kibana     │
                                    │  (Visualize) │
                                    └──────────────┘

1. Services write logs to stdout/files
2. Log shipper (Filebeat/Fluentd) collects logs
3. Elasticsearch stores and indexes logs
4. Kibana provides search and visualization
```

**Searching Logs (Kibana):**

```
# Find all errors for user 123
level: ERROR AND user_id: 123

# Find slow requests (> 1s)
duration: > 1000 AND endpoint: "/api/orders"

# Find errors in last 1 hour
level: ERROR AND timestamp: [now-1h TO now]
```

### 3. Traces (Distributed Tracing)

Track requests as they flow through multiple services.

**Distributed Trace:**

```
┌────────────────────────────────────────────────────┐
│  Request: GET /api/orders/123                      │
│  Trace ID: abc123                                  │
├────────────────────────────────────────────────────┤
│                                                    │
│  [API Gateway] ───────────────────── 250ms        │
│    ├─ [Auth Service] ────────────── 20ms          │
│    ├─ [Order Service] ───────────── 200ms         │
│    │   ├─ [Database Query] ─────── 150ms          │
│    │   └─ [Cache Check] ───────── 5ms             │
│    └─ [User Service] ────────────── 30ms          │
│                                                    │
└────────────────────────────────────────────────────┘

Total: 250ms
Slowest: Order Service → Database Query (150ms)
```

**OpenTelemetry Example:**

```python
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Set up tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export traces to Jaeger
jaeger_exporter = JaegerExporter(
    agent_host_name='localhost',
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Auto-instrument Flask
FlaskInstrumentor().instrument_app(app)

# Auto-instrument requests library
RequestsInstrumentor().instrument()

# Manual instrumentation
@app.route('/api/orders/<order_id>')
def get_order(order_id):
    with tracer.start_as_current_span("get_order") as span:
        span.set_attribute("order_id", order_id)
        
        # This span will be parent
        
        # Check cache (child span)
        with tracer.start_as_current_span("check_cache"):
            cached = redis.get(f"order:{order_id}")
            if cached:
                span.set_attribute("cache_hit", True)
                return jsonify(json.loads(cached))
        
        # Query database (child span)
        with tracer.start_as_current_span("database_query"):
            order = db.query(f"SELECT * FROM orders WHERE id = {order_id}")
            span.set_attribute("cache_hit", False)
        
        # Call user service (child span, auto-instrumented)
        user = requests.get(f'http://user-service/users/{order.user_id}')
        
        return jsonify(order)
```

**Trace Visualization (Jaeger):**

```
Request: GET /api/orders/123
Trace ID: abc123def456

Timeline:
0ms    50ms   100ms  150ms  200ms  250ms
│──────┼──────┼──────┼──────┼──────┼──────│
│                                         │
├─ get_order ─────────────────────────────┤ 250ms
  │                                       │
  ├─ check_cache ─┤ 5ms                   │
  │                                       │
  ├─ database_query ─────────────────┤    │ 150ms
  │                                       │
  └─ GET /users/123 ──────────┤           │ 50ms
```

---

## 🚨 Alerting

Notify when something goes wrong.

### Alert Types

```
Threshold Alert:
  • CPU usage > 80% for 5 minutes
  • Error rate > 1% for 10 minutes
  
Anomaly Detection:
  • Request rate 3x higher than usual
  • Response time 2x slower than baseline
  
SLO Violation:
  • 99.9% availability not met this month
  • p95 latency > 500ms
```

### Prometheus Alerting Rules

```yaml
# prometheus-alerts.yml
groups:
  - name: example_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status="500"}[5m]) > 0.05
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} (threshold: 0.05)"
      
      # High latency
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "p95 latency is {{ $value }}s (threshold: 1s)"
      
      # Service down
      - alert: ServiceDown
        expr: up{job="api-server"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} is down"
```

### Alert Manager (Routing)

```yaml
# alertmanager.yml
route:
  receiver: team-pager
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  
  routes:
    # Critical alerts → PagerDuty
    - match:
        severity: critical
      receiver: pagerduty
      continue: true
    
    # Warnings → Slack
    - match:
        severity: warning
      receiver: slack

receivers:
  - name: pagerduty
    pagerduty_configs:
      - service_key: <pagerduty_key>
  
  - name: slack
    slack_configs:
      - api_url: https://hooks.slack.com/services/xxx
        channel: '#alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

---

## 🔍 Health Checks

### Types of Health Checks

**1. Liveness Probe:** Is the service alive?

```python
@app.route('/health/live')
def liveness():
    # Simple check: is process running?
    return jsonify({'status': 'alive'}), 200
```

**2. Readiness Probe:** Is the service ready to serve traffic?

```python
@app.route('/health/ready')
def readiness():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'external_api': check_external_api()
    }
    
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503
    
    return jsonify({
        'status': 'ready' if all_ready else 'not_ready',
        'checks': checks
    }), status_code

def check_database():
    try:
        db.execute("SELECT 1")
        return True
    except:
        return False

def check_redis():
    try:
        redis.ping()
        return True
    except:
        return False
```

**3. Startup Probe:** Has the service finished starting up?

```python
startup_complete = False

@app.route('/health/startup')
def startup():
    if startup_complete:
        return jsonify({'status': 'ready'}), 200
    else:
        return jsonify({'status': 'starting'}), 503

@app.before_first_request
def initialize():
    global startup_complete
    # Warm up caches, load data, etc.
    load_config()
    warm_cache()
    startup_complete = True
```

### Kubernetes Health Checks

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: api-server
spec:
  containers:
  - name: api
    image: api-server:latest
    
    # Liveness: Restart if fails
    livenessProbe:
      httpGet:
        path: /health/live
        port: 5000
      initialDelaySeconds: 30
      periodSeconds: 10
      failureThreshold: 3
    
    # Readiness: Remove from load balancer if fails
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 5000
      initialDelaySeconds: 5
      periodSeconds: 5
      failureThreshold: 2
    
    # Startup: Wait for startup before other checks
    startupProbe:
      httpGet:
        path: /health/startup
        port: 5000
      failureThreshold: 30
      periodSeconds: 10
```

---

## 📉 Debugging Distributed Systems

### Correlation IDs

Track requests across services:

```python
import uuid

@app.before_request
def add_correlation_id():
    # Get correlation ID from header or generate new
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    request.correlation_id = correlation_id

@app.after_request
def inject_correlation_id(response):
    response.headers['X-Correlation-ID'] = request.correlation_id
    return response

# Log with correlation ID
@app.route('/api/orders')
def create_order():
    logger.info(
        'Creating order',
        extra={'correlation_id': request.correlation_id}
    )
    
    # Pass correlation ID to downstream services
    response = requests.post(
        'http://inventory-service/reserve',
        headers={'X-Correlation-ID': request.correlation_id},
        json=order_data
    )
    
    return jsonify(order)
```

**Searching Logs by Correlation ID:**

```
# Find all logs for specific request
correlation_id: "abc-123-def-456"

Result:
  [API Gateway] Creating order (correlation_id: abc-123-def-456)
  [Inventory Service] Reserving items (correlation_id: abc-123-def-456)
  [Payment Service] Processing payment (correlation_id: abc-123-def-456)
  [API Gateway] Order created (correlation_id: abc-123-def-456)
```

### Error Tracking (Sentry)

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/123",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,  # Sample 10% of traces
    environment="production"
)

@app.route('/api/process')
def process():
    try:
        # Business logic
        result = expensive_operation()
        return jsonify(result)
    
    except Exception as e:
        # Automatically captured by Sentry
        sentry_sdk.capture_exception(e)
        
        # Add context
        sentry_sdk.set_user({"id": request.user_id})
        sentry_sdk.set_context("request", {
            "endpoint": "/api/process",
            "method": "POST",
            "params": request.args
        })
        
        raise
```

**Sentry Dashboard:**

```
┌────────────────────────────────────────────────────┐
│  Error: DatabaseConnectionError                    │
│  First seen: 2 hours ago                           │
│  Last seen: 5 minutes ago                          │
│  Occurrences: 234                                  │
│  Users affected: 45                                │
├────────────────────────────────────────────────────┤
│  Stack Trace:                                      │
│    File "api.py", line 123, in process             │
│      result = db.query(sql)                        │
│    File "database.py", line 45, in query           │
│      conn = self.pool.get_connection()             │
│    DatabaseConnectionError: Connection timeout     │
├────────────────────────────────────────────────────┤
│  Context:                                          │
│    User: user-123                                  │
│    Endpoint: /api/process                          │
│    Request params: {filter: "active"}              │
│    Tags: {environment: "production"}               │
└────────────────────────────────────────────────────┘
```

---

## 📊 SLIs, SLOs, SLAs

### Service Level Indicators (SLIs)

Metrics that matter to users:

```
Availability:
  • Successful requests / Total requests
  • Example: 99,900 / 100,000 = 99.9%

Latency:
  • p50, p95, p99 response times
  • Example: p95 = 200ms

Error Rate:
  • Failed requests / Total requests
  • Example: 100 / 100,000 = 0.1%

Throughput:
  • Requests per second
  • Example: 1,000 req/s
```

### Service Level Objectives (SLOs)

Targets for SLIs:

```
Availability SLO:
  • 99.9% uptime (43.8 minutes downtime/month)
  
Latency SLO:
  • p95 response time < 500ms
  • p99 response time < 1s
  
Error Rate SLO:
  • < 0.1% error rate
```

### Service Level Agreements (SLAs)

Contractual commitments with customers:

```
SLA Example:
  • Uptime: 99.9% monthly
  • Latency: p95 < 1s
  • Support: 24/7 response within 1 hour
  • Penalty: 10% refund if SLA violated
```

**Error Budget:**

```
Availability SLO: 99.9%
Allowed downtime: 43.8 minutes/month

Tracking:
  • Day 1-10: 2 minutes downtime (4.6% of budget used)
  • Day 11-20: 40 minutes downtime (91.3% of budget used)
  • Day 21-30: 1.8 minutes left
  
Decision:
  • Budget exhausted? Freeze new features, focus on stability
  • Budget remaining? Continue feature development
```

---

## 🎯 Interview Tips

**Key Points to Cover:**
1. ✅ Three pillars: Metrics, Logs, Traces
2. ✅ Difference between monitoring and observability
3. ✅ Health checks (liveness, readiness)
4. ✅ Alerting strategies (avoid alert fatigue)
5. ✅ SLOs and error budgets

**Common Questions:**
- "How would you debug a slow request?" → Distributed tracing to find bottleneck
- "How to monitor microservices?" → Centralized logging, metrics, traces with correlation IDs
- "What metrics would you track?" → Request rate, error rate, latency (RED method)
- "How to avoid alert fatigue?" → Set proper thresholds, group alerts, escalation policies
- "Difference between liveness and readiness?" → Liveness: restart, Readiness: traffic routing

**RED Method (Monitoring):**
```
Rate: Requests per second
Error: Error rate (%)
Duration: Latency (p50, p95, p99)
```

**USE Method (Resources):**
```
Utilization: % time resource is busy
Saturation: Queue depth, wait time
Errors: Error count
```

---

**Next:** [Design Social Media Feed](12_social_feed.md)
