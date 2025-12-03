"""
Trie (Prefix Tree)
==================
Understanding Trie data structure for string operations.
"""


class TrieNode:
    """Node in a Trie"""
    def __init__(self):
        self.children = {}  # Character -> TrieNode
        self.is_end_of_word = False  # True if this completes a word
        self.word_count = 0  # How many words end here (for duplicates)


print("=" * 60)
print("What is a Trie?")
print("=" * 60)
print()
print("A Trie (pronounced 'try') is a tree for storing strings.")
print("Also called: Prefix Tree, Digital Tree")
print()
print("Key Properties:")
print("  • Each node represents a character")
print("  • Root represents empty string")
print("  • Path from root to node = prefix")
print("  • Nodes with is_end_of_word=True mark complete words")
print()
print("Why Use Tries?")
print("  • Fast prefix search: O(m) where m = word length")
print("  • Autocomplete functionality")
print("  • Spell checking")
print("  • IP routing (longest prefix match)")
print("  • Dictionary implementation")
print()
print("Example Trie with words: 'cat', 'car', 'card', 'dog'")
print()
print("                root")
print("               /    \\")
print("              c      d")
print("              |      |")
print("              a      o")
print("             / \\     |")
print("            t   r    g*")
print("           *    |")
print("                d")
print("                *")
print()
print("* = end of word marker")
print()
print("Path 'c→a→t' = 'cat'")
print("Path 'c→a→r' = 'car'")
print("Path 'c→a→r→d' = 'card'")
print()


class Trie:
    """Trie (Prefix Tree) implementation"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """
        Insert word into trie.
        
        How it works:
        1. Start at root
        2. For each character:
           - If child exists, move to it
           - If not, create new node
        3. Mark last node as end of word
        
        Time: O(m) where m = len(word)
        Space: O(m) worst case (new branch)
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.word_count += 1
    
    def search(self, word):
        """
        Check if exact word exists.
        
        How it works:
        1. Traverse trie following characters
        2. If path doesn't exist, return False
        3. If path exists, check is_end_of_word
        
        Time: O(m), Space: O(1)
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        """
        Check if any word starts with prefix.
        
        How it works:
        1. Try to traverse prefix path
        2. If successful, prefix exists
        
        Time: O(m), Space: O(1)
        """
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def delete(self, word):
        """
        Delete word from trie.
        
        How it works:
        1. Find the word
        2. Unmark end of word
        3. Remove unused nodes from bottom up
        
        Time: O(m), Space: O(m)
        """
        def delete_helper(node, word, index):
            if index == len(word):
                # Reached end of word
                if not node.is_end_of_word:
                    return False  # Word doesn't exist
                
                node.is_end_of_word = False
                node.word_count = 0
                
                # Delete node if it has no children
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False  # Word doesn't exist
            
            child = node.children[char]
            should_delete = delete_helper(child, word, index + 1)
            
            if should_delete:
                del node.children[char]
                # Delete current node if no children and not end of word
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        delete_helper(self.root, word, 0)
    
    def get_all_words(self):
        """
        Get all words in trie.
        
        How it works:
        1. DFS traversal
        2. Build word character by character
        3. When end marker found, add to results
        
        Time: O(n) where n = total characters
        """
        words = []
        
        def dfs(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child in node.children.items():
                dfs(child, current_word + char)
        
        dfs(self.root, "")
        return words
    
    def autocomplete(self, prefix):
        """
        Get all words starting with prefix.
        
        How it works:
        1. Navigate to prefix node
        2. DFS from that node
        3. Collect all words below
        
        Time: O(p + n) where p = prefix length, n = results
        """
        # Find prefix node
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words from this node
        words = []
        
        def dfs(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child in node.children.items():
                dfs(child, current_word + char)
        
        dfs(node, prefix)
        return words
    
    def count_words_with_prefix(self, prefix):
        """Count how many words start with prefix"""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        
        # Count all words below this node
        def count(node):
            total = node.word_count
            for child in node.children.values():
                total += count(child)
            return total
        
        return count(node)


print("=" * 60)
print("Trie Operations Demo")
print("=" * 60)
print()

trie = Trie()
words = ["cat", "car", "card", "dog", "door", "dodge"]

print(f"Inserting words: {words}")
for word in words:
    trie.insert(word)

print()
print("Search operations:")
print(f"  'car' exists? {trie.search('car')}")
print(f"  'care' exists? {trie.search('care')}")
print(f"  'ca' exists? {trie.search('ca')}")

print()
print("Prefix operations:")
print(f"  Words start with 'ca'? {trie.starts_with('ca')}")
print(f"  Words start with 'do'? {trie.starts_with('do')}")
print(f"  Words start with 'bat'? {trie.starts_with('bat')}")

print()
print("Autocomplete:")
print(f"  'ca' → {trie.autocomplete('ca')}")
print(f"  'do' → {trie.autocomplete('do')}")
print(f"  'car' → {trie.autocomplete('car')}")

print()
print(f"All words in trie: {trie.get_all_words()}")

print()
print("Delete 'car'...")
trie.delete('car')
print(f"  'car' exists? {trie.search('car')}")
print(f"  'card' exists? {trie.search('card')}")
print(f"  All words: {trie.get_all_words()}")

print()


# Visualize trie structure
print("=" * 60)
print("How Trie Stores Words")
print("=" * 60)
print()

print("Step-by-step insertion:")
print()

trie2 = Trie()

print("1. Insert 'cat':")
print("      root")
print("       |")
print("       c")
print("       |")
print("       a")
print("       |")
print("       t*")
print()

trie2.insert('cat')

print("2. Insert 'car':")
print("      root")
print("       |")
print("       c")
print("       |")
print("       a")
print("      / \\")
print("     t*  r*")
print()

trie2.insert('car')

print("3. Insert 'card':")
print("      root")
print("       |")
print("       c")
print("       |")
print("       a")
print("      / \\")
print("     t*  r*")
print("          |")
print("          d*")
print()

trie2.insert('card')

print("4. Insert 'dog':")
print("        root")
print("       /    \\")
print("      c      d")
print("      |      |")
print("      a      o")
print("     / \\     |")
print("    t*  r*   g*")
print("         |")
print("         d*")
print()

trie2.insert('dog')


# Trie vs Hash Table vs BST
print("=" * 60)
print("Trie vs Other Data Structures")
print("=" * 60)
print()
print("For string operations:")
print()
print("                Trie         Hash Table    BST")
print("-" * 60)
print("Insert          O(m)         O(m)          O(m log n)")
print("Search          O(m)         O(m)          O(m log n)")
print("Delete          O(m)         O(m)          O(m log n)")
print("Prefix search   O(m)         O(n*m)        O(m log n)")
print("Autocomplete    O(m+k)       O(n)          O(m log n + k)")
print("Sorted output   O(n)         O(n log n)    O(n)")
print()
print("m = word length, n = number of words, k = results")
print()
print("Space complexity:")
print("  Trie:       O(ALPHABET_SIZE × n × m)")
print("  Hash Table: O(n × m)")
print("  BST:        O(n × m)")
print()
print("Trie advantages:")
print("  ✓ Fast prefix operations")
print("  ✓ No hash collisions")
print("  ✓ Alphabetically ordered")
print("  ✓ Common prefixes share space")
print()
print("Trie disadvantages:")
print("  ✗ More memory (many pointers)")
print("  ✗ Cache unfriendly")
print("  ✗ Slower for exact match only")
print()


# Advanced Trie operations
print("=" * 60)
print("Advanced Trie Operations")
print("=" * 60)
print()


def longest_common_prefix(trie):
    """
    Find longest common prefix of all words.
    
    How it works:
    1. Traverse while only one child exists
    2. Stop at branch or end of word
    
    Time: O(m) where m = prefix length
    """
    if not trie.root.children:
        return ""
    
    prefix = []
    node = trie.root
    
    while len(node.children) == 1 and not node.is_end_of_word:
        char = list(node.children.keys())[0]
        prefix.append(char)
        node = node.children[char]
    
    return ''.join(prefix)


def word_break(s, word_dict):
    """
    Check if string can be segmented into dictionary words.
    
    How it works:
    1. Build trie from dictionary
    2. Use DP to check all possible segmentations
    
    Time: O(n²) where n = len(s)
    """
    # Build trie
    trie = Trie()
    for word in word_dict:
        trie.insert(word)
    
    # DP: can we segment s[0:i]?
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # Empty string
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and trie.search(s[j:i]):
                dp[i] = True
                break
    
    return dp[n]


def replace_words(dictionary, sentence):
    """
    Replace words with shortest root from dictionary.
    
    Example:
      dict = ["cat", "bat", "rat"]
      sentence = "the cattle was rattled by the battery"
      output = "the cat was rat by the bat"
    
    Time: O(n × m) where n = words, m = avg length
    """
    trie = Trie()
    for root in dictionary:
        trie.insert(root)
    
    def find_root(word):
        node = trie.root
        prefix = []
        
        for char in word:
            if char not in node.children:
                return word  # No root found
            node = node.children[char]
            prefix.append(char)
            if node.is_end_of_word:
                return ''.join(prefix)  # Found root
        
        return word
    
    words = sentence.split()
    return ' '.join(find_root(word) for word in words)


trie3 = Trie()
words3 = ["flower", "flow", "flight"]
for word in words3:
    trie3.insert(word)

print(f"Words: {words3}")
print(f"Longest common prefix: '{longest_common_prefix(trie3)}'")

print()
s = "leetcode"
word_dict = ["leet", "code"]
print(f"String: '{s}'")
print(f"Dictionary: {word_dict}")
print(f"Can segment? {word_break(s, word_dict)}")

print()
dictionary = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"
print(f"Dictionary: {dictionary}")
print(f"Sentence: '{sentence}'")
print(f"Replaced: '{replace_words(dictionary, sentence)}'")

print()


# Compressed Trie (Radix Tree)
print("=" * 60)
print("Compressed Trie (Radix Tree)")
print("=" * 60)
print()
print("Regular Trie for 'test', 'testing', 'tested':")
print()
print("        root")
print("         |")
print("         t")
print("         |")
print("         e")
print("         |")
print("         s")
print("         |")
print("         t*")
print("        / \\")
print("       e   i")
print("       |   |")
print("       d*  n")
print("           |")
print("           g*")
print()
print("Compressed Trie (Radix Tree):")
print()
print("        root")
print("         |")
print("        test*")
print("        /    \\")
print("      ed*    ing*")
print()
print("Benefits:")
print("  • Space efficient (fewer nodes)")
print("  • Used in routing tables")
print("  • IP lookup")
print("  • Inverted indexes")
print()


# Real-world applications
print("=" * 60)
print("Real-World Applications")
print("=" * 60)
print()
print("1. Autocomplete Systems:")
print("   • Google search suggestions")
print("   • IDE code completion")
print("   • Address autocomplete")
print()
print("2. Spell Checkers:")
print("   • Find words with typos")
print("   • Suggest corrections")
print("   • Dictionary lookups")
print()
print("3. IP Routing:")
print("   • Longest prefix match")
print("   • Router forwarding tables")
print("   • Network packet routing")
print()
print("4. Text Search:")
print("   • Pattern matching")
print("   • Full-text search engines")
print("   • Inverted indexes")
print()
print("5. DNA Sequencing:")
print("   • Store genetic sequences")
print("   • Find common patterns")
print("   • Genome analysis")
print()
print("6. Phone Directories:")
print("   • T9 predictive text")
print("   • Contact search")
print("   • Number prefix lookup")
print()


# Trie variants
print("=" * 60)
print("Trie Variants")
print("=" * 60)
print()
print("1. Suffix Trie:")
print("   • Store all suffixes of a string")
print("   • Used in pattern matching")
print("   • Example: 'banana' → 'banana', 'anana', 'nana', ...")
print()
print("2. Ternary Search Trie:")
print("   • Three children: less, equal, greater")
print("   • More space efficient than standard trie")
print("   • Faster than hash table for many operations")
print()
print("3. Compressed Trie (Radix Tree):")
print("   • Merge nodes with single child")
print("   • Store edge labels (not single characters)")
print("   • Used in routing, memory management")
print()
print("4. Patricia Trie:")
print("   • Radix tree with radix = 2 (binary)")
print("   • Used in IP routing")
print("   • Very space efficient")
print()


# Common patterns
print("=" * 60)
print("Common Trie Patterns")
print("=" * 60)
print()
print("Pattern 1: Word Search")
print("  • Insert all words into trie")
print("  • Search by following character paths")
print()
print("Pattern 2: Prefix Matching")
print("  • Navigate to prefix node")
print("  • Collect all words below that node")
print()
print("Pattern 3: Word Break")
print("  • Build trie from dictionary")
print("  • Use DP to check segmentation")
print()
print("Pattern 4: Longest Common Prefix")
print("  • Traverse while single child exists")
print("  • Stop at branch point")
print()
print("Pattern 5: Replace with Roots")
print("  • Find shortest matching prefix")
print("  • Replace word with root")
print()


# Time and space complexity
print("=" * 60)
print("Time & Space Complexity")
print("=" * 60)
print()
print("Given:")
print("  n = number of words")
print("  m = average word length")
print("  k = alphabet size (26 for lowercase English)")
print()
print("Time Complexity:")
print("  Insert:           O(m)")
print("  Search:           O(m)")
print("  Delete:           O(m)")
print("  Prefix search:    O(m)")
print("  Autocomplete:     O(m + results)")
print("  All words:        O(total chars)")
print()
print("Space Complexity:")
print("  Worst case:       O(k × n × m)")
print("  Best case:        O(n × m)  [one long chain]")
print("  Typical:          O(n × m)  [shared prefixes]")
print()
print("Per node:")
print("  Standard trie:    k pointers + 1 bool")
print("  Optimized:        map/dict + 1 bool")
print()
