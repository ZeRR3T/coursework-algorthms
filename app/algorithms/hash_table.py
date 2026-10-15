from __future__ import annotations
from typing import Generic, Iterator, Optional, TypeVar
from app.algorithms.models import Guest

T = TypeVar("T")

class _ListNode(Generic[T]):
    __slots__ = ("key", "value", "next")
    def __init__(self, key: str, value: T) -> None:
        self.key = key
        self.value = value
        self.next: Optional[_ListNode[T]] = None

def _hash_key(key: str, capacity: int) -> int:
    h = 0
    for ch in key:
        h = (h * 31 + ord(ch)) % (2**31)
    return h % capacity if capacity else 0

def _is_prime(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0: return False
        d += 2
    return True

def _next_prime_at_least(n: int) -> int:
    x = max(2, n)
    while not _is_prime(x): x += 1
    return x

class HashTableOpen:
    def __init__(self, capacity: int = 17, *, max_load_factor: float = 0.75) -> None:
        self._initial_capacity = max(1, capacity)
        self._capacity = self._initial_capacity
        self._max_load_factor = max_load_factor
        self._buckets: list[Optional[_ListNode[Guest]]] = [None] * self._capacity
        self._size = 0
        self._collisions_total = 0
        self._rehash_count = 0

    def __len__(self) -> int: return self._size
    @property
    def capacity(self) -> int: return self._capacity

    def _needs_rehash_for_insert(self) -> bool:
        if self._capacity == 0: return True
        return (self._size + 1) / self._capacity > self._max_load_factor

    def _rehash(self) -> None:
        entries = list(self.iter_all())
        new_cap = _next_prime_at_least(2 * self._capacity + 1)
        self._capacity = new_cap
        self._buckets = [None] * self._capacity
        self._size = 0
        self._rehash_count += 1
        for k, g in entries: self._insert_new_entry(k, g)

    def _insert_new_entry(self, key: str, guest: Guest) -> None:
        idx = _hash_key(key, self._capacity)
        new = _ListNode(key, guest)
        if self._buckets[idx] is None:
            self._buckets[idx] = new
        else:
            self._collisions_total += 1
            tail = self._buckets[idx]
            while tail.next is not None: tail = tail.next
            tail.next = new
        self._size += 1

    def _find_node(self, key: str) -> tuple[int, Optional[_ListNode[Guest]], Optional[_ListNode[Guest]]]:
        idx = _hash_key(key, self._capacity)
        prev: Optional[_ListNode[Guest]] = None
        cur = self._buckets[idx]
        while cur is not None:
            if cur.key == key: return idx, prev, cur
            prev = cur
            cur = cur.next
        return idx, prev, None

    def get(self, key: str) -> Optional[Guest]:
        _, _, node = self._find_node(key)
        return node.value if node else None

    def put(self, key: str, guest: Guest) -> None:
        _, _, node = self._find_node(key)
        if node is not None:
            node.value = guest
            return
        while self._needs_rehash_for_insert(): self._rehash()
        self._insert_new_entry(key, guest)

    def remove(self, key: str) -> bool:
        idx, prev, node = self._find_node(key)
        if node is None: return False
        if prev is None: self._buckets[idx] = node.next
        else: prev.next = node.next
        self._size -= 1
        return True

    def iter_all(self) -> Iterator[tuple[str, Guest]]:
        for i in range(self._capacity):
            cur = self._buckets[i]
            while cur is not None:
                yield cur.key, cur.value
                cur = cur.next