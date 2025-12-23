"""
Prompt templates for plan generation.

Keep prompts in one place so they can be swapped without touching core logic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


DEFAULT_PLAN_SYSTEM_PROMPT = """You are a senior software engineer and technical PM.
You write crisp, actionable implementation plans in Markdown.

Hard requirements for the plan output:
- Output MUST be valid Markdown.
- Include a section named "## Files" listing files to create/update, one per line, with backticks around paths (e.g. `app/main.py`).
- Include "## Steps" as an ordered list with concrete actions.
- Include "## Open Questions" listing anything you need to clarify.
- Do not include any code implementation; this is planning only.
"""


DEFAULT_PLAN_USER_TEMPLATE = """Create an implementation plan for the following user requirement.

User requirement:
{requirement}
"""


def load_prompt_text(prompt_file: Optional[str]) -> Optional[str]:
    """
    Load a prompt override from a file path.

    If prompt_file is None, returns None.
    """
    if not prompt_file:
        return None
    return Path(prompt_file).read_text(encoding="utf-8")


