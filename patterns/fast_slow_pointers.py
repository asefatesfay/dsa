"""
Fast & Slow Pointers
====================
Two pointers moving at different speeds, typically on linked lists or arrays.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head):
    """
    Detect cycle in a linked list using Floyd's Tortoise and Hare.
    Time: O(n) Space: O(1)
    """
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


def middle_of_list(head):
    """
    Return middle node (second middle for even length).
    Time: O(n) Space: O(1)
    """
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


if __name__ == "__main__":
    # 1->2->3->4->5
    nodes = [ListNode(i) for i in range(1,6)]
    for i in range(4):
        nodes[i].next = nodes[i+1]
    print("middle:", middle_of_list(nodes[0]).val)  # 3
    print("cycle:", has_cycle(nodes[0]))  # False
    nodes[4].next = nodes[1]  # create cycle
    print("cycle:", has_cycle(nodes[0]))  # True
