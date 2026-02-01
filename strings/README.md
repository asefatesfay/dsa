# Strings

String manipulation and pattern matching implementations in Python.

## Overview

Strings are immutable sequences of characters that are fundamental in programming. This module covers string operations, common patterns, and real-world applications.

## Contents

### 01_basics.py
- String creation and initialization
- Accessing and slicing
- String methods (case, searching, trimming, splitting)
- String formatting (%, format(), f-strings)
- Encoding and decoding
- Common operations

### 02_common_patterns.py
- Two pointers technique
- Sliding window problems
- Character frequency (hash maps)
- String building and compression
- Subsequence/substring problems
- String reversal patterns
- Pattern matching and search
- Parentheses validation

### 03_real_world_examples.py
- Email validation
- URL parsing
- Slug generation
- Password strength checking
- Log parsing and analysis
- Data masking (credit cards, PII)
- Search term highlighting
- CSV parsing
- File path operations
- Text comparison and diff

### 04_leetcode_problems.py
- Valid Anagram (LC 242)
- Group Anagrams (LC 49)
- Longest Palindromic Substring (LC 5)
- Palindromic Substrings (LC 647)
- Encode and Decode Strings (LC 271)
- Longest Repeating Character Replacement (LC 424)
- Minimum Window Substring (LC 76)
- Valid Palindrome II (LC 680)
- Longest Common Prefix (LC 14)
- String to Integer atoi (LC 8)
- Find All Anagrams (LC 438)
- Longest Substring K Distinct (LC 340)
- Reverse Words in String (LC 151)
- Implement strStr (LC 28)
- Zigzag Conversion (LC 6)

## Key Concepts

### Time Complexity
- Access by index: O(1)
- Search (find/in): O(n)
- Slice: O(k) where k is slice length
- Concatenation: O(n + m)
- Replace: O(n)
- Split/Join: O(n)

### Space Complexity
- String storage: O(n)
- Immutable - modifications create new strings

## Common Patterns

1. **Two Pointers**: Palindrome checking, reversing
2. **Sliding Window**: Substrings with constraints
3. **Hash Map**: Character frequency, anagrams
4. **String Builder**: Efficient concatenation
5. **Pattern Matching**: Regular expressions, KMP

## Best Practices

- Use f-strings for formatting (Python 3.6+)
- Use `str.join()` instead of `+` for multiple concatenations
- Leverage built-in string methods instead of loops
- Remember strings are immutable in Python
- Use raw strings `r''` for regex and file paths
- Consider `collections.Counter` for frequency counting

## Real-World Applications

- **Web Development**: URL parsing, slugs, validation
- **Security**: Password validation, data masking
- **Data Processing**: Parsing logs, CSV, JSON
- **Search**: Pattern matching, highlighting
- **Text Processing**: NLP, text analysis
- **File Operations**: Path handling, sanitization

## Interview Tips

- Always consider edge cases: empty strings, single character
- Think about character encoding (ASCII vs Unicode)
- Watch for case sensitivity requirements
- Optimize string building with join() or StringBuilder pattern
- Many string problems can use hash maps or two pointers
