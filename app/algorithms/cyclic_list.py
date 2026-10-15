from __future__ import annotations
from typing import Callable, Iterator, Optional
from app.algorithms.models import StayRecord

class _Node:
    __slots__ = ("data", "next")
    def __init__(self, data: StayRecord) -> None:
        self.data = data
        self.next: Optional[_Node] = None

def _hoare_partition(arr: list[StayRecord], low: int, high: int, key_fn: Callable[[StayRecord], str]) -> int:
    pivot = key_fn(arr[(low + high) // 2])
    i, j = low - 1, high + 1
    while True:
        while True:
            i += 1
            if key_fn(arr[i]) >= pivot: break
        while True:
            j -= 1
            if key_fn(arr[j]) <= pivot: break
        if i >= j: return j
        arr[i], arr[j] = arr[j], arr[i]

def quicksort_hoare(arr: list[StayRecord], key_fn: Callable[[StayRecord], str] = lambda r: r.room_number, low: int = 0, high: int | None = None) -> None:
    if high is None: high = len(arr) - 1
    if low >= high: return
    p = _hoare_partition(arr, low, high, key_fn)
    quicksort_hoare(arr, key_fn, low, p)
    quicksort_hoare(arr, key_fn, p + 1, high)

class CyclicStayList:
    def __init__(self) -> None:
        self._head: Optional[_Node] = None
        self._size = 0

    def __len__(self) -> int: return self._size
    def is_empty(self) -> bool: return self._head is None

    def _append_no_sort(self, record: StayRecord) -> None:
        new = _Node(record)
        if self._head is None:
            new.next = new
            self._head = new
        else:
            tail = self._head
            while tail.next is not self._head: tail = tail.next
            tail.next = new
            new.next = self._head
        self._size += 1

    def append(self, record: StayRecord) -> None:
        self._append_no_sort(record)
        self._sort_by_room()

    def _to_array(self) -> list[StayRecord]:
        if self._head is None: return []
        out: list[StayRecord] = []
        cur: Optional[_Node] = self._head
        while True:
            assert cur is not None
            out.append(cur.data)
            cur = cur.next
            if cur is self._head: break
        return out

    def _rebuild_from(self, items: list[StayRecord]) -> None:
        self._head = None
        self._size = 0
        for r in items: self._append_no_sort(r)

    def _sort_by_room(self) -> None:
        items = self._to_array()
        if len(items) <= 1: return
        quicksort_hoare(items, key_fn=lambda r: r.room_number)
        self._rebuild_from(items)

    def remove_if(self, predicate: Callable[[StayRecord], bool]) -> tuple[int, list[StayRecord]]:
        if self._head is None: return 0, []
        arr = self._to_array()
        removed = [r for r in arr if predicate(r)]
        kept = [r for r in arr if not predicate(r)]
        self._rebuild_from(kept)
        return len(removed), removed

    def iter_records(self) -> Iterator[StayRecord]:
        if self._head is None: return
        cur: Optional[_Node] = self._head
        while True:
            assert cur is not None
            yield cur.data
            cur = cur.next
            if cur is self._head: break

    def clear(self) -> None:
        self._head = None
        self._size = 0