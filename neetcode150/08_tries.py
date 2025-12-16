"""
NeetCode 150 - Tries
====================
Prefix tree data structure (3 problems).
"""


# PATTERN: Trie Data Structure
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    """
    Implement Trie (Prefix Tree).
    
    Pattern: Hash map for children
    
    Operations:
    - insert: O(m) where m = word length
    - search: O(m)
    - startsWith: O(m)
    Space: O(n * m) where n = number of words
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    
    def search(self, word):
        """Returns true if word is in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word
    
    def starts_with(self, prefix):
        """Returns true if there is a word with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


# PATTERN: Trie + DFS
class WordDictionary:
    """
    Design Add and Search Words Data Structure.
    Supports '.' wildcard matching any character.
    
    Pattern: Trie with DFS for wildcard search
    
    Operations:
    - addWord: O(m)
    - search: O(26^m) worst case with all dots
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def add_word(self, word):
        """Add a word to the data structure."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    
    def search(self, word):
        """Search for a word (supports '.' wildcard)."""
        def dfs(index, node):
            if index == len(word):
                return node.is_word
            
            char = word[index]
            if char == '.':
                # Try all possible children
                for child in node.children.values():
                    if dfs(index + 1, child):
                        return True
                return False
            else:
                if char not in node.children:
                    return False
                return dfs(index + 1, node.children[char])
        
        return dfs(0, self.root)


# PATTERN: Backtracking + Trie
def find_words(board, words):
    """
    Word Search II - find all words from list in 2D board.
    
    Pattern: Trie + DFS backtracking
    
    Algorithm Steps:
    1. Build trie from word list
    2. DFS from each cell
    3. Prune search using trie structure
    4. Mark visited cells during DFS
    5. Backtrack and unmark
    
    Why it works:
    - Trie allows efficient prefix checking (prune invalid paths early)
    - DFS explores all possible paths
    - Backtracking ensures all cells can be reused for different words
    
    Example:
    board = [['o','a','a','n'],
             ['e','t','a','e'],
             ['i','h','k','r'],
             ['i','f','l','v']]
    words = ["oath","pea","eat","rain"]
    → ["oath","eat"]
    
    Time: O(m * n * 4^L) where L = max word length
    Space: O(sum of all word lengths) for trie
    """
    # Build trie
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
        node.word = word
    
    rows, cols = len(board), len(board[0])
    result = set()
    
    def dfs(r, c, node):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        
        char = board[r][c]
        if char == '#' or char not in node.children:
            return
        
        node = node.children[char]
        
        # Found a word
        if node.is_word:
            result.add(node.word)
        
        # Mark as visited
        board[r][c] = '#'
        
        # Explore all 4 directions
        dfs(r + 1, c, node)
        dfs(r - 1, c, node)
        dfs(r, c + 1, node)
        dfs(r, c - 1, node)
        
        # Backtrack
        board[r][c] = char
    
    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    
    return list(result)


if __name__ == "__main__":
    print("=== NeetCode 150 - Tries ===\n")
    
    # Test Trie
    print("Test 1: Implement Trie")
    trie = Trie()
    trie.insert("apple")
    print(f"Search 'apple': {trie.search('apple')}")
    print(f"Search 'app': {trie.search('app')}")
    print(f"Starts with 'app': {trie.starts_with('app')}")
    trie.insert("app")
    print(f"Search 'app' after insert: {trie.search('app')}")
    
    # Test WordDictionary
    print("\nTest 2: Add and Search Words")
    wd = WordDictionary()
    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")
    print(f"Search 'pad': {wd.search('pad')}")
    print(f"Search 'bad': {wd.search('bad')}")
    print(f"Search '.ad': {wd.search('.ad')}")
    print(f"Search 'b..': {wd.search('b..')}")
    
    # Test Word Search II
    print("\nTest 3: Word Search II")
    board = [
        ['o', 'a', 'a', 'n'],
        ['e', 't', 'a', 'e'],
        ['i', 'h', 'k', 'r'],
        ['i', 'f', 'l', 'v']
    ]
    words = ["oath", "pea", "eat", "rain"]
    print(f"Board: {board}")
    print(f"Words: {words}")
    print(f"Found: {find_words(board, words)}")
