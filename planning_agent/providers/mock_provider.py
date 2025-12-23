from __future__ import annotations

from planning_agent.providers.base import PlanProvider


class MockPlanProvider(PlanProvider):
    def generate_plan(self, requirement: str) -> str:
        return f"""# Implementation Plan

## Requirement
{requirement}

## Files
- `main.py` - Main application entry point
- `utils.py` - Utility functions
- `README.md` - Documentation

## Steps
1. Set up project structure.
2. Implement core functionality.
3. Add error handling and validation.
4. Add basic documentation.
5. Add tests and verify the workflow.

## Dependencies
- No external dependencies required for basic implementation.

## Open Questions
- Are there any constraints on libraries/frameworks?
- What is the target Python version and runtime environment?
"""


