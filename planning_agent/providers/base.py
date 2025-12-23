from __future__ import annotations

from abc import ABC, abstractmethod


class PlanProvider(ABC):
    @abstractmethod
    def generate_plan(self, requirement: str) -> str:
        """Return a Markdown plan for the given requirement."""
        raise NotImplementedError


