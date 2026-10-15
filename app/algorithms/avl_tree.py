from __future__ import annotations
from typing import Callable, Iterator, Optional
from app.algorithms.boyer_moore import boyer_moore_contains
from app.algorithms.models import Room

class AVLNode:
    __slots__ = ("key", "room", "left", "right", "height")
    def __init__(self, key: str, room: Room) -> None:
        self.key = key
        self.room = room
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height = 1

def _height(n: Optional[AVLNode]) -> int: return n.height if n else 0
def _balance(n: Optional[AVLNode]) -> int: return _height(n.left) - _height(n.right) if n else 0
def _update_height(n: AVLNode) -> None: n.height = 1 + max(_height(n.left), _height(n.right))

def _rotate_right(y: AVLNode) -> AVLNode:
    x = y.left
    assert x is not None
    t2 = x.right
    x.right = y
    y.left = t2
    _update_height(y)
    _update_height(x)
    return x

def _rotate_left(x: AVLNode) -> AVLNode:
    y = x.right
    assert y is not None
    t2 = y.left
    y.left = x
    x.right = t2
    _update_height(x)
    _update_height(y)
    return y

def _rebalance(n: AVLNode) -> AVLNode:
    _update_height(n)
    bal = _balance(n)
    if bal > 1 and _balance(n.left) >= 0: return _rotate_right(n)
    if bal > 1 and n.left is not None and _balance(n.left) < 0:
        n.left = _rotate_left(n.left)
        return _rotate_right(n)
    if bal < -1 and _balance(n.right) <= 0: return _rotate_left(n)
    if bal < -1 and n.right is not None and _balance(n.right) > 0:
        n.right = _rotate_right(n.right)
        return _rotate_left(n)
    return n

class AVLTree:
    def __init__(self) -> None:
        self._root: Optional[AVLNode] = None

    def find(self, key: str) -> Optional[Room]:
        cur = self._root
        while cur is not None:
            if key == cur.key: return cur.room
            if key < cur.key: cur = cur.left
            else: cur = cur.right
        return None

    def insert(self, key: str, room: Room) -> bool:
        def _ins(n: Optional[AVLNode], k: str, r: Room) -> tuple[Optional[AVLNode], bool]:
            if n is None: return AVLNode(k, r), True
            if k == n.key: return n, False
            if k < n.key:
                n.left, ok = _ins(n.left, k, r)
                if not ok: return n, False
            else:
                n.right, ok = _ins(n.right, k, r)
                if not ok: return n, False
            return _rebalance(n), True
        self._root, ok = _ins(self._root, key, room)
        return ok

    def delete(self, key: str) -> bool:
        def _min_node(n: AVLNode) -> AVLNode:
            while n.left is not None: n = n.left
            return n
        def _del(n: Optional[AVLNode], k: str) -> tuple[Optional[AVLNode], bool]:
            if n is None: return None, False
            if k < n.key:
                n.left, ok = _del(n.left, k)
                if not ok: return n, False
            elif k > n.key:
                n.right, ok = _del(n.right, k)
                if not ok: return n, False
            else:
                if n.left is None: return n.right, True
                if n.right is None: return n.left, True
                succ = _min_node(n.right)
                n.key, n.room = succ.key, succ.room
                n.right, _ = _del(n.right, succ.key)
            return _rebalance(n), True
        self._root, ok = _del(self._root, key)
        return ok

    def clear(self) -> None: self._root = None

    def preorder(self, visit: Callable[[Room], None]) -> None:
        def _walk(n: Optional[AVLNode]) -> None:
            if n is None: return
            visit(n.room)
            _walk(n.left)
            _walk(n.right)
        _walk(self._root)

    def find_by_equipment_fragment(self, fragment: str) -> list[Room]:
        found: list[Room] = []
        def visit(room: Room) -> None:
            if boyer_moore_contains(room.equipment, fragment): found.append(room)
        self.preorder(visit)
        return found

    def build_layout(self, *, h_spacing: float = 88.0, v_spacing: float = 92.0) -> tuple[dict[str, tuple[float, float]], list[tuple[str, str]]]:
        if self._root is None: return {}, []
        inorder_index: dict[str, int] = {}
        counter = [0]
        def inorder(n: Optional[AVLNode]) -> None:
            if n is None: return
            inorder(n.left)
            inorder_index[n.key] = counter[0]
            counter[0] += 1
            inorder(n.right)
        inorder(self._root)

        depth_map: dict[str, int] = {}
        def set_depth(n: Optional[AVLNode], d: int) -> None:
            if n is None: return
            depth_map[n.key] = d
            set_depth(n.left, d + 1)
            set_depth(n.right, d + 1)
        set_depth(self._root, 0)

        edges: list[tuple[str, str]] = []
        def collect_edges(n: Optional[AVLNode]) -> None:
            if n is None: return
            if n.left is not None:
                edges.append((n.key, n.left.key))
                collect_edges(n.left)
            if n.right is not None:
                edges.append((n.key, n.right.key))
                collect_edges(n.right)
        collect_edges(self._root)

        pos: dict[str, tuple[float, float]] = {}
        for k, ix in inorder_index.items():
            pos[k] = (float(ix) * h_spacing + 50.0, float(depth_map[k]) * v_spacing + 45.0)
        return pos, edges