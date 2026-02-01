"""
Strings - Real World Examples
==============================
Practical string manipulation applications in real scenarios.
"""

import re
from collections import Counter
from typing import List


print("=" * 60)
print("Example 1: Email Validation")
print("=" * 60)
print()

def is_valid_email(email):
    """
    Validate email address format.
    Used in: User registration, form validation
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def extract_email_parts(email):
    """Extract username and domain from email."""
    if '@' not in email:
        return None, None
    username, domain = email.split('@', 1)
    return username, domain

print("Email Validation:")
emails = ["user@example.com", "invalid.email", "test@domain.co.uk", "@example.com"]
for email in emails:
    valid = is_valid_email(email)
    username, domain = extract_email_parts(email) if valid else (None, None)
    print(f"  {email}")
    print(f"    Valid: {valid}")
    if valid:
        print(f"    Username: {username}, Domain: {domain}")
print()


print("=" * 60)
print("Example 2: URL Parser")
print("=" * 60)
print()

def parse_url(url):
    """
    Parse URL into components.
    Used in: Web scraping, API clients, routers
    """
    from urllib.parse import urlparse, parse_qs
    
    parsed = urlparse(url)
    
    return {
        'scheme': parsed.scheme,
        'domain': parsed.netloc,
        'path': parsed.path,
        'params': parse_qs(parsed.query),
        'fragment': parsed.fragment
    }

print("URL Parser:")
url = "https://example.com:8080/path/to/page?id=123&name=test#section"
components = parse_url(url)
print(f"  URL: {url}")
for key, value in components.items():
    print(f"    {key}: {value}")
print()


print("=" * 60)
print("Example 3: Slug Generator")
print("=" * 60)
print()

def generate_slug(title):
    """
    Convert title to URL-friendly slug.
    Used in: Blog platforms, CMS, URL generation
    """
    # Convert to lowercase
    slug = title.lower()
    # Replace spaces and special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

print("Slug Generator:")
titles = [
    "My First Blog Post!",
    "10 Tips for Python Programming",
    "Understanding AI & Machine Learning",
    "  Extra   Spaces   Here  "
]
for title in titles:
    print(f"  '{title}'")
    print(f"    Slug: {generate_slug(title)}")
print()


print("=" * 60)
print("Example 4: Password Strength Checker")
print("=" * 60)
print()

def check_password_strength(password):
    """
    Validate password meets security requirements.
    Used in: User authentication, security systems
    """
    errors = []
    strength = 0
    
    if len(password) < 8:
        errors.append("At least 8 characters required")
    else:
        strength += 1
    
    if not re.search(r'[a-z]', password):
        errors.append("At least one lowercase letter required")
    else:
        strength += 1
    
    if not re.search(r'[A-Z]', password):
        errors.append("At least one uppercase letter required")
    else:
        strength += 1
    
    if not re.search(r'\d', password):
        errors.append("At least one digit required")
    else:
        strength += 1
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("At least one special character required")
    else:
        strength += 1
    
    strength_levels = ["Weak", "Fair", "Good", "Strong", "Very Strong"]
    
    return {
        'valid': len(errors) == 0,
        'strength': strength_levels[strength] if strength <= 4 else "Very Strong",
        'errors': errors
    }

print("Password Strength Checker:")
passwords = ["pass", "Password1", "P@ssw0rd", "MyP@ssw0rd123!"]
for pwd in passwords:
    result = check_password_strength(pwd)
    print(f"  Password: {pwd}")
    print(f"    Valid: {result['valid']}")
    print(f"    Strength: {result['strength']}")
    if result['errors']:
        print(f"    Errors: {', '.join(result['errors'])}")
print()


print("=" * 60)
print("Example 5: Log Parser")
print("=" * 60)
print()

def parse_log_entry(log_line):
    """
    Parse server log entry.
    Used in: Log analysis, monitoring systems, debugging
    """
    # Example format: [2024-01-15 10:30:45] INFO: User login successful - user_id: 123
    pattern = r'\[([^\]]+)\]\s+(\w+):\s+(.+)'
    match = re.match(pattern, log_line)
    
    if match:
        timestamp, level, message = match.groups()
        return {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
    return None

def analyze_logs(log_lines):
    """Analyze log patterns for errors and warnings."""
    levels = Counter()
    errors = []
    
    for line in log_lines:
        parsed = parse_log_entry(line)
        if parsed:
            levels[parsed['level']] += 1
            if parsed['level'] in ['ERROR', 'CRITICAL']:
                errors.append(parsed)
    
    return {'level_counts': levels, 'errors': errors}

print("Log Parser:")
logs = [
    "[2024-01-15 10:30:45] INFO: User login successful - user_id: 123",
    "[2024-01-15 10:31:22] WARNING: High memory usage detected",
    "[2024-01-15 10:32:10] ERROR: Database connection failed",
    "[2024-01-15 10:33:00] INFO: Request processed successfully"
]
for log in logs:
    parsed = parse_log_entry(log)
    if parsed:
        print(f"  {parsed['level']}: {parsed['message']}")

analysis = analyze_logs(logs)
print(f"\n  Summary: {dict(analysis['level_counts'])}")
print()


print("=" * 60)
print("Example 6: Credit Card Masking")
print("=" * 60)
print()

def mask_credit_card(card_number):
    """
    Mask credit card number for security.
    Used in: Payment systems, PCI compliance
    """
    # Remove spaces and hyphens
    clean = re.sub(r'[\s-]', '', card_number)
    
    if len(clean) < 4:
        return '*' * len(clean)
    
    # Show only last 4 digits
    return '*' * (len(clean) - 4) + clean[-4:]

def mask_sensitive_data(text):
    """Mask email and phone numbers in text."""
    # Mask email
    text = re.sub(
        r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        r'***@\2',
        text
    )
    # Mask phone (XXX-XXX-1234)
    text = re.sub(
        r'\b(\d{3})[-.]?(\d{3})[-.]?(\d{4})\b',
        r'***-***-\3',
        text
    )
    return text

print("Credit Card Masking:")
cards = ["4532-1234-5678-9010", "378282246310005", "6011 1111 1111 1117"]
for card in cards:
    print(f"  {card} -> {mask_credit_card(card)}")

print("\nSensitive Data Masking:")
text = "Contact: john@example.com or call 555-123-4567"
print(f"  Original: {text}")
print(f"  Masked: {mask_sensitive_data(text)}")
print()


print("=" * 60)
print("Example 7: Search Query Highlighter")
print("=" * 60)
print()

def highlight_search_terms(text, query):
    """
    Highlight search terms in text.
    Used in: Search results, text editors
    """
    words = query.split()
    highlighted = text
    
    for word in words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        highlighted = pattern.sub(f'**{word}**', highlighted)
    
    return highlighted

print("Search Highlighting:")
text = "Python is a high-level programming language. Python is easy to learn."
query = "python programming"
print(f"  Text: {text}")
print(f"  Query: {query}")
print(f"  Result: {highlight_search_terms(text, query)}")
print()


print("=" * 60)
print("Example 8: CSV Parser (Simple)")
print("=" * 60)
print()

def parse_csv_line(line, delimiter=','):
    """
    Parse CSV line handling quoted values.
    Used in: Data import/export, ETL pipelines
    """
    result = []
    current = []
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == delimiter and not in_quotes:
            result.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
    
    result.append(''.join(current).strip())
    return result

print("CSV Parser:")
csv_lines = [
    'John,Doe,30,Engineer',
    'Jane,"Smith, Jr.",25,"Software Engineer"',
    '"Bob","Johnson",35,"Data, Analyst"'
]
for line in csv_lines:
    parsed = parse_csv_line(line)
    print(f"  {line}")
    print(f"    Parsed: {parsed}")
print()


print("=" * 60)
print("Example 9: File Path Operations")
print("=" * 60)
print()

def get_file_extension(filename):
    """Extract file extension."""
    return filename.rsplit('.', 1)[-1] if '.' in filename else ''

def sanitize_filename(filename):
    """
    Remove invalid characters from filename.
    Used in: File upload systems, file management
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    return sanitized

def generate_unique_filename(filename, existing_files):
    """Generate unique filename if file exists."""
    if filename not in existing_files:
        return filename
    
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    counter = 1
    
    while True:
        new_name = f"{name}_{counter}.{ext}" if ext else f"{name}_{counter}"
        if new_name not in existing_files:
            return new_name
        counter += 1

print("File Path Operations:")
filenames = ["document.pdf", "my<file>.txt", "  .hidden  ", "report.docx"]
for filename in filenames:
    print(f"  Original: {filename}")
    print(f"    Sanitized: {sanitize_filename(filename)}")
    print(f"    Extension: {get_file_extension(filename)}")

print("\nUnique Filename Generation:")
existing = ["document.pdf", "document_1.pdf"]
new_file = generate_unique_filename("document.pdf", existing)
print(f"  Existing: {existing}")
print(f"  New file: {new_file}")
print()


print("=" * 60)
print("Example 10: Text Diff/Comparison")
print("=" * 60)
print()

def simple_diff(text1, text2):
    """
    Compare two texts and find differences.
    Used in: Version control, document comparison
    """
    words1 = text1.split()
    words2 = text2.split()
    
    added = set(words2) - set(words1)
    removed = set(words1) - set(words2)
    common = set(words1) & set(words2)
    
    return {
        'added': list(added),
        'removed': list(removed),
        'common': len(common),
        'similarity': len(common) / max(len(set(words1)), len(set(words2)))
    }

print("Text Comparison:")
text1 = "The quick brown fox jumps"
text2 = "The fast brown fox runs"
diff = simple_diff(text1, text2)
print(f"  Text 1: {text1}")
print(f"  Text 2: {text2}")
print(f"  Added: {diff['added']}")
print(f"  Removed: {diff['removed']}")
print(f"  Similarity: {diff['similarity']:.2%}")
print()


print("=" * 60)
print("Real-World String Applications Summary")
print("=" * 60)
print()
print("1. Email Validation: User registration, forms")
print("2. URL Parsing: Web scraping, APIs, routing")
print("3. Slug Generation: SEO-friendly URLs")
print("4. Password Validation: Security, authentication")
print("5. Log Parsing: Monitoring, debugging")
print("6. Data Masking: Security, PCI compliance")
print("7. Search Highlighting: Search results, editors")
print("8. CSV Parsing: Data import/export")
print("9. Filename Operations: File management, uploads")
print("10. Text Comparison: Version control, diff tools")
print()
print("Common Use Cases:")
print("  • Input validation and sanitization")
print("  • Data parsing and extraction")
print("  • Text transformation and formatting")
print("  • Security and privacy (masking, hashing)")
print("  • Search and pattern matching")
