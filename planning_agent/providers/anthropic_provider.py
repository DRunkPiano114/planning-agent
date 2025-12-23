from __future__ import annotations

import os
from typing import Optional

from planning_agent.prompts import DEFAULT_PLAN_USER_TEMPLATE, load_prompt_text
from planning_agent.providers.base import PlanProvider


class AnthropicPlanProvider(PlanProvider):
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        prompt_file: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
        self.max_tokens = max_tokens

        file_prompt = load_prompt_text(prompt_file)
        self.system_prompt = (file_prompt or system_prompt or "").strip() or None
        self.user_template = DEFAULT_PLAN_USER_TEMPLATE

    def generate_plan(self, requirement: str) -> str:
        try:
            import anthropic  # type: ignore
        except ImportError as e:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic") from e

        client = anthropic.Anthropic(api_key=self.api_key)
        user_text = self.user_template.format(requirement=requirement).strip()

        # Anthropic's messages API treats system as a top-level field.
        message = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_text}],
        )
        # message.content is a list of blocks
        text = getattr(message.content[0], "text", None) if message.content else None
        return (text or "").strip()


