"""
Strings - Basics
================
Strings are immutable sequences of characters in Python.
Time Complexity: Access O(1), Search O(n), Slice O(k), Concatenation O(n+m)
Space Complexity: O(n)
"""

# Creating strings
empty_string = ""
single_quote = 'Hello'
double_quote = "World"
triple_quote = """Multi
line
string"""
raw_string = r"C:\Users\path"  # Raw string (ignores escape sequences)

print("Basic Strings:")
print(f"Empty: '{empty_string}'")
print(f"Single quotes: {single_quote}")
print(f"Double quotes: {double_quote}")
print(f"Triple quotes: {triple_quote}")
print(f"Raw string: {raw_string}")
print()

# Accessing characters
text = "Python"
print("Accessing Characters:")
print(f"First character: {text[0]}")
print(f"Last character: {text[-1]}")
print(f"Second character: {text[1]}")
print()

# String slicing
print("String Slicing:")
print(f"First 3 chars: {text[0:3]}")
print(f"From index 2: {text[2:]}")
print(f"Last 3 chars: {text[-3:]}")
print(f"Every 2nd char: {text[::2]}")
print(f"Reverse: {text[::-1]}")
print()

# String length
print(f"Length: {len(text)}")
print()

# String immutability
print("Strings are Immutable:")
original = "hello"
print(f"Original: {original}")
# original[0] = 'H'  # This would raise TypeError
modified = 'H' + original[1:]  # Create new string instead
print(f"Modified (new string): {modified}")
print()

# String concatenation
print("String Concatenation:")
str1 = "Hello"
str2 = "World"
result = str1 + " " + str2
print(f"Using +: {result}")
result = " ".join([str1, str2])
print(f"Using join: {result}")
print()

# String repetition
print("String Repetition:")
print(f"'Ha' * 3 = {'Ha' * 3}")
print(f"'-' * 10 = {'-' * 10}")
print()

# Membership testing
print("Membership Testing:")
print(f"'Py' in 'Python': {'Py' in 'Python'}")
print(f"'java' in 'Python': {'java' in 'Python'}")
print()

# String methods - Case
print("=" * 60)
print("String Methods - Case Conversion")
print("=" * 60)
text = "Hello World"
print(f"Original: {text}")
print(f"upper(): {text.upper()}")
print(f"lower(): {text.lower()}")
print(f"capitalize(): {text.capitalize()}")
print(f"title(): {text.title()}")
print(f"swapcase(): {text.swapcase()}")
print()

# String methods - Checking
print("=" * 60)
print("String Methods - Checking")
print("=" * 60)
print(f"'123'.isdigit(): {'123'.isdigit()}")
print(f"'abc'.isalpha(): {'abc'.isalpha()}")
print(f"'abc123'.isalnum(): {'abc123'.isalnum()}")
print(f"'   '.isspace(): {'   '.isspace()}")
print(f"'Hello World'.istitle(): {'Hello World'.istitle()}")
print(f"'HELLO'.isupper(): {'HELLO'.isupper()}")
print(f"'hello'.islower(): {'hello'.islower()}")
print()

# String methods - Searching
print("=" * 60)
print("String Methods - Searching")
print("=" * 60)
text = "Hello World Hello"
print(f"Text: {text}")
print(f"find('World'): {text.find('World')}")
print(f"find('xyz'): {text.find('xyz')}")  # Returns -1 if not found
print(f"index('Hello'): {text.index('Hello')}")
print(f"rfind('Hello'): {text.rfind('Hello')}")  # Find from right
print(f"count('Hello'): {text.count('Hello')}")
print()

# String methods - Trimming
print("=" * 60)
print("String Methods - Trimming")
print("=" * 60)
text = "  Hello World  "
print(f"Original: '{text}'")
print(f"strip(): '{text.strip()}'")
print(f"lstrip(): '{text.lstrip()}'")
print(f"rstrip(): '{text.rstrip()}'")
print(f"strip('Hd'): '{'HelloWorld'.strip('Hd')}'")  # Remove specific chars
print()

# String methods - Splitting and Joining
print("=" * 60)
print("String Methods - Splitting and Joining")
print("=" * 60)
text = "apple,banana,orange"
print(f"Original: {text}")
words = text.split(',')
print(f"split(','): {words}")
print(f"join with ' | ': {' | '.join(words)}")
print()

text = "Hello World Python"
print(f"Text: {text}")
print(f"split(): {text.split()}")  # Split by whitespace
print(f"split(' ', 1): {text.split(' ', 1)}")  # Max 1 split
print()

lines = "Line1\nLine2\nLine3"
print(f"splitlines(): {lines.splitlines()}")
print()

# String methods - Replacing
print("=" * 60)
print("String Methods - Replacing")
print("=" * 60)
text = "Hello World Hello"
print(f"Original: {text}")
print(f"replace('Hello', 'Hi'): {text.replace('Hello', 'Hi')}")
print(f"replace('Hello', 'Hi', 1): {text.replace('Hello', 'Hi', 1)}")  # Replace only once
print()

# String methods - Startswith and Endswith
print("=" * 60)
print("String Methods - Prefix/Suffix")
print("=" * 60)
filename = "document.pdf"
print(f"Filename: {filename}")
print(f"startswith('doc'): {filename.startswith('doc')}")
print(f"endswith('.pdf'): {filename.endswith('.pdf')}")
print(f"endswith(('.pdf', '.doc')): {filename.endswith(('.pdf', '.doc'))}")
print()

# String formatting - Old style
print("=" * 60)
print("String Formatting - % operator (old style)")
print("=" * 60)
name = "Alice"
age = 30
print("Name: %s, Age: %d" % (name, age))
print("Pi: %.2f" % 3.14159)
print()

# String formatting - format() method
print("=" * 60)
print("String Formatting - format() method")
print("=" * 60)
print("Name: {}, Age: {}".format(name, age))
print("Name: {0}, Age: {1}, Name again: {0}".format(name, age))
print("Name: {n}, Age: {a}".format(n=name, a=age))
print("Pi: {:.2f}".format(3.14159))
print()

# String formatting - f-strings (Python 3.6+)
print("=" * 60)
print("String Formatting - f-strings (best practice)")
print("=" * 60)
print(f"Name: {name}, Age: {age}")
print(f"Next year: {age + 1}")
print(f"Pi: {3.14159:.2f}")
print(f"Uppercase: {name.upper()}")
print()

# String alignment and padding
print("=" * 60)
print("String Alignment and Padding")
print("=" * 60)
text = "Python"
print(f"ljust(10): '{text.ljust(10)}'")
print(f"rjust(10): '{text.rjust(10)}'")
print(f"center(10): '{text.center(10)}'")
print(f"zfill(10): '{'42'.zfill(10)}'")  # Pad with zeros
print()

# Using format for alignment
print(f"Left: '{text:<10}'")
print(f"Right: '{text:>10}'")
print(f"Center: '{text:^10}'")
print(f"Center with *: '{text:*^10}'")
print()

# String encoding and decoding
print("=" * 60)
print("String Encoding and Decoding")
print("=" * 60)
text = "Hello 世界"
print(f"Original: {text}")
encoded = text.encode('utf-8')
print(f"Encoded (UTF-8): {encoded}")
decoded = encoded.decode('utf-8')
print(f"Decoded: {decoded}")
print()

# String partition
print("=" * 60)
print("String Partition")
print("=" * 60)
email = "user@example.com"
print(f"Email: {email}")
before, sep, after = email.partition('@')
print(f"partition('@'): ('{before}', '{sep}', '{after}')")
print()

# String translation
print("=" * 60)
print("String Translation")
print("=" * 60)
# Remove vowels using translation
text = "Hello World"
print(f"Original: {text}")
translation_table = str.maketrans('aeiou', '12345')
print(f"With translation: {text.translate(translation_table)}")

# Remove characters
translation_table = str.maketrans('', '', 'aeiou')
print(f"Remove vowels: {text.translate(translation_table)}")
print()

# Common string operations
print("=" * 60)
print("Common String Operations")
print("=" * 60)

# Check if palindrome
def is_palindrome(s):
    return s == s[::-1]

print(f"'racecar' is palindrome: {is_palindrome('racecar')}")
print(f"'hello' is palindrome: {is_palindrome('hello')}")
print()

# Reverse words in a string
sentence = "Hello World Python"
reversed_words = ' '.join(sentence.split()[::-1])
print(f"Original: {sentence}")
print(f"Reversed words: {reversed_words}")
print()

# Count vowels
def count_vowels(s):
    return sum(1 for char in s.lower() if char in 'aeiou')

text = "Hello World"
print(f"Vowels in '{text}': {count_vowels(text)}")
print()

# Remove duplicates (preserve order)
def remove_duplicates(s):
    seen = set()
    result = []
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    return ''.join(result)

text = "programming"
print(f"Original: {text}")
print(f"Without duplicates: {remove_duplicates(text)}")
print()

# Check if anagram
def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

print(f"'listen' and 'silent' are anagrams: {is_anagram('listen', 'silent')}")
print(f"'hello' and 'world' are anagrams: {is_anagram('hello', 'world')}")
print()

print("=" * 60)
print("String Complexity Summary")
print("=" * 60)
print("Access (by index):        O(1)")
print("Search (find/in):         O(n)")
print("Slice:                    O(k) where k is slice length")
print("Concatenation:            O(n + m)")
print("Replace:                  O(n)")
print("Split:                    O(n)")
print("Join:                     O(n)")
print("upper/lower:              O(n)")
print()
print("Best Practices:")
print("  • Use f-strings for formatting (Python 3.6+)")
print("  • Use str.join() instead of + for multiple concatenations")
print("  • Use str methods instead of loops when possible")
print("  • Remember strings are immutable")
print("  • Use raw strings (r'') for regex patterns and file paths")
