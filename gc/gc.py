from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Obj:
    val: Any
    left: Obj | None = None
    right: Obj | None = None
    marked: bool = False

    def __repr__(self) -> str:
        return f"Obj({self.val})"


class VM:
    def __init__(self):
        self.stack: list[Obj] = []
        self.heap: list[Obj] = []
        self.max_objects: int = 8

    @property
    def num_objects(self) -> int:
        return len(self.heap)

    def push(self, Obj) -> None:
        self.stack.append(Obj)

    def pop(self) -> Obj:
        if not self.stack:
            raise IndexError("pop form empty stack")
        return self.stack.pop()

    def allocate(
        self, val: Any, left: Obj | None = None, right: Obj | None = None
    ) -> Obj:
        if self.num_objects >= self.max_objects:
            self.mark()
            self.sweep()

        _obj = Obj(val=val, left=left, right=right)
        self.heap.append(_obj)
        return _obj

    def sweep(self) -> None:
        survivor: list[Obj] = []
        for root in self.heap:
            if root.marked:
                root.marked = False
                survivor.append(root)
            else:
                root.left = None
                root.right = None
        self.heap = survivor

    def mark(self) -> None:

        def mark_object(obj: Obj) -> None:
            if obj.marked or obj is None:
                return

            obj.marked = True
            mark_object(obj.left)
            mark_object(obj.right)

        for root in self.stack:
            mark_object(root)
