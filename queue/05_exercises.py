"""
Queue - Exercises
=================
Practice exercises to test your understanding.
Try solving these before looking at solutions!
"""

from collections import deque
from typing import List, Optional


# Exercise 1: Design Circular Deque
class MyCircularDeque:
    """
    Design circular double-ended queue.
    TODO: Implement insertFront, insertLast, deleteFront, deleteLast, getFront, getRear, isEmpty, isFull
    Hint: Use list with front and rear pointers
    """
    def __init__(self, k: int):
        pass
    
    def insertFront(self, value: int) -> bool:
        pass
    
    def insertLast(self, value: int) -> bool:
        pass
    
    def deleteFront(self) -> bool:
        pass
    
    def deleteLast(self) -> bool:
        pass
    
    def getFront(self) -> int:
        pass
    
    def getRear(self) -> int:
        pass
    
    def isEmpty(self) -> bool:
        pass
    
    def isFull(self) -> bool:
        pass


# Exercise 2: Moving Average from Data Stream
class MovingAverage:
    """
    Calculate moving average of last n values.
    Example: size=3, next(1)=1, next(10)=5.5, next(3)=4.67, next(5)=6
    TODO: Implement this class
    Hint: Use queue to maintain last n values
    """
    def __init__(self, size: int):
        pass
    
    def next(self, val: int) -> float:
        pass


# Exercise 3: Time Needed to Buy Tickets
def time_required_to_buy(tickets: List[int], k: int) -> int:
    """
    People in line to buy tickets. tickets[i] is number of tickets person i wants.
    Each person takes 1 second to buy 1 ticket, then goes to back of line if needs more.
    Return time for person at position k to finish buying.
    Example: tickets=[2,3,2], k=2 -> 6
    
    TODO: Implement this function
    Hint: Simulate the queue process
    """
    pass


# Exercise 4: Dota2 Senate
def predict_party_victory(senate: str) -> str:
    """
    Radiant (R) and Dire (D) senators vote to ban opponent. Each can ban one senator.
    Return "Radiant" or "Dire" for winner.
    Example: "RD" -> "Radiant", "RDD" -> "Dire"
    
    TODO: Implement this function
    Hint: Use two queues for R and D senators
    """
    pass


# Exercise 5: Design Hit Counter
class HitCounter:
    """
    Design hit counter that counts hits in past 5 minutes (300 seconds).
    TODO: Implement hit(timestamp) and getHits(timestamp)
    Hint: Use queue to store timestamps
    """
    def __init__(self):
        pass
    
    def hit(self, timestamp: int) -> None:
        """Record a hit at timestamp"""
        pass
    
    def getHits(self, timestamp: int) -> int:
        """Get hits in past 300 seconds"""
        pass


# Exercise 6: Reveal Cards in Increasing Order
def deck_revealed_increasing(deck: List[int]) -> List[int]:
    """
    Reveal cards in increasing order by: reveal top, move next to bottom, repeat.
    Return deck order that reveals in increasing order.
    Example: [17,13,11,2,3,5,7] -> [2,13,3,11,5,17,7]
    
    TODO: Implement this function
    Hint: Simulate the process in reverse using queue
    """
    pass


# Exercise 7: Shortest Path in Grid with Obstacles Elimination
def shortest_path(grid: List[List[int]], k: int) -> int:
    """
    Find shortest path from top-left to bottom-right, can eliminate up to k obstacles.
    Example: grid=[[0,1,1],[1,1,1],[1,0,0]], k=1 -> 6
    
    TODO: Implement this function
    Hint: BFS with state (row, col, obstacles_used)
    """
    pass


# Exercise 8: Snakes and Ladders
def snakes_and_ladders(board: List[List[int]]) -> int:
    """
    Find minimum moves to reach end of board game.
    Example: board=[[-1,-1],[-1,3]] -> 1
    
    TODO: Implement this function
    Hint: BFS treating board as graph
    """
    pass


# Exercise 9: Bus Routes
def num_buses_to_destination(routes: List[List[int]], source: int, target: int) -> int:
    """
    Find minimum number of buses to reach target from source.
    routes[i] is list of stops for bus i.
    Example: routes=[[1,2,7],[3,6,7]], source=1, target=6 -> 2
    
    TODO: Implement this function
    Hint: BFS on bus routes, not stops
    """
    pass


# Exercise 10: Cut Off Trees for Golf Event
def cut_off_tree(forest: List[List[int]]) -> int:
    """
    Cut trees in increasing height order. Return minimum steps, or -1 if impossible.
    0=obstacle, 1=ground, >1=tree with that height
    
    TODO: Implement this function
    Hint: BFS for each pair of trees
    """
    pass


# Exercise 11: Jump Game VI
def max_result(nums: List[int], k: int) -> int:
    """
    Start at index 0, each step jump to i+j where 1 <= j <= k.
    Maximize sum of values at visited indices.
    Example: nums=[1,-1,-2,4,-7,3], k=2 -> 7 (path: 1->-1->4->3)
    
    TODO: Implement this function
    Hint: Use monotonic deque for optimization
    """
    pass


# Exercise 12: Sliding Window Median
def median_sliding_window(nums: List[int], k: int) -> List[float]:
    """
    Find median of each sliding window of size k.
    Example: nums=[1,3,-1,-3,5,3,6,7], k=3 -> [1,-1,-1,3,5,6]
    
    TODO: Implement this function
    Hint: Use two heaps or balanced tree with deque for window
    """
    pass


# Exercise 13: Minimum Knight Moves
def min_knight_moves(x: int, y: int) -> int:
    """
    Find minimum moves for knight to reach (x, y) from (0, 0).
    Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular.
    
    TODO: Implement this function
    Hint: BFS with symmetry optimization
    """
    pass


# Exercise 14: Word Ladder II
def find_ladders(begin_word: str, end_word: str, word_list: List[str]) -> List[List[str]]:
    """
    Find all shortest transformation sequences from begin_word to end_word.
    Each step changes one letter, intermediate words must be in word_list.
    Example: begin="hit", end="cog", list=["hot","dot","dog","lot","log","cog"]
    Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
    
    TODO: Implement this function
    Hint: BFS to find distances, then DFS to build paths
    """
    pass


# Exercise 15: Maximum Candies You Can Get from Boxes
def max_candies(status: List[int], candies: List[int], keys: List[List[int]], 
                contained_boxes: List[List[int]], initial_boxes: List[int]) -> int:
    """
    Start with initial_boxes. Open boxes (if status[i]=1 or you have key).
    Get candies, keys, and contained boxes from opened boxes.
    Return maximum candies you can get.
    
    TODO: Implement this function
    Hint: Use queue to process boxes as they become available
    """
    pass


# Test your solutions
if __name__ == "__main__":
    print("Test your implementations here!")
    print("Uncomment the tests as you complete each exercise.\n")
    
    # Test Exercise 2
    # ma = MovingAverage(3)
    # print(f"Moving average: {ma.next(1)}, {ma.next(10)}, {ma.next(3)}, {ma.next(5)}")
    
    # Test Exercise 3
    # tickets = [2, 3, 2]
    # k = 2
    # print(f"Time to buy tickets: {time_required_to_buy(tickets, k)}")
    
    # Test Exercise 4
    # print(f"Senate winner: {predict_party_victory('RD')}")
    # print(f"Senate winner: {predict_party_victory('RDD')}")
    
    # Test Exercise 5
    # counter = HitCounter()
    # counter.hit(1)
    # counter.hit(2)
    # counter.hit(3)
    # print(f"Hits at 4: {counter.getHits(4)}")
    # counter.hit(300)
    # print(f"Hits at 300: {counter.getHits(300)}")
    # print(f"Hits at 301: {counter.getHits(301)}")
    
    # Test Exercise 6
    # deck = [17, 13, 11, 2, 3, 5, 7]
    # print(f"Deck order: {deck_revealed_increasing(deck)}")
    
    pass
