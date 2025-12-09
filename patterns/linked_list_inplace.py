"""
In-place Linked List Manipulation
================================
Modify linked lists without extra arrays; pointer juggling is key.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head):
    """
    Reverse a singly linked list in-place.
    Time: O(n) Space: O(1)
    """
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


def reverse_sublist(head, m, n):
    """
    Reverse sublist [m..n] (1-indexed) in-place.
    """
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(m - 1):
        prev = prev.next
    cur = prev.next
    for _ in range(n - m):
        move = cur.next
        cur.next = move.next
        move.next = prev.next
        prev.next = move
    return dummy.next


def reorder_list(head):
    """
    Reorder L0→L1→...→Ln-1→Ln into L0→Ln→L1→Ln-1→...
    """
    if not head or not head.next:
        return head
    # Find middle
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # Reverse second half
    second = reverse_list(slow.next)
    slow.next = None
    # Merge
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
    return head


if __name__ == "__main__":
    nodes = [ListNode(i) for i in range(1,6)]
    for i in range(4):
        nodes[i].next = nodes[i+1]
    h = reverse_list(nodes[0])
    # print reversed values
    cur, vals = h, []
    while cur:
        vals.append(cur.val); cur = cur.next
    print("reversed:", vals)
