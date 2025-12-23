from __future__ import annotations

import os
from typing import Any, Optional

from planning_agent.prompts import (
    DEFAULT_PLAN_SYSTEM_PROMPT,
    DEFAULT_PLAN_USER_TEMPLATE,
    load_prompt_text,
)
from planning_agent.providers.base import PlanProvider


class OpenAIPlanProvider(PlanProvider):
    """
    OpenAI-backed plan generator.

    Supports injecting a pre-built OpenAI client for tests.
    Prefers the modern Responses API when available, with a fallback to Chat Completions.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        prompt_file: Optional[str] = None,
        system_prompt: Optional[str] = None,
        client: Any = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key and client is None:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = temperature

        # Prompt override: if prompt_file is provided, it replaces the system prompt.
        # This makes it easy to tweak prompts without touching code.
        file_prompt = load_prompt_text(prompt_file)
        self.system_prompt = (file_prompt or system_prompt or DEFAULT_PLAN_SYSTEM_PROMPT).strip()
        self.user_template = DEFAULT_PLAN_USER_TEMPLATE

        self._client = client  # injected for tests; otherwise we create it lazily

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            import openai  # type: ignore
        except ImportError as e:
            raise ImportError("openai package not installed. Install with: pip install openai") from e
        self._client = openai.OpenAI(api_key=self.api_key)
        return self._client

    def generate_plan(self, requirement: str) -> str:
        client = self._get_client()
        user_text = self.user_template.format(requirement=requirement).strip()

        # Prefer Responses API (openai>=1.x)
        if hasattr(client, "responses") and hasattr(client.responses, "create"):
            resp = client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_text},
                ],
                temperature=self.temperature,
            )
            plan = getattr(resp, "output_text", None)
            if isinstance(plan, str) and plan.strip():
                return plan.strip()

        # Fallback: Chat Completions
        if hasattr(client, "chat") and hasattr(client.chat, "completions"):
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_text},
                ],
                temperature=self.temperature,
            )
            plan = resp.choices[0].message.content
            return (plan or "").strip()

        raise RuntimeError("OpenAI client does not support responses.create or chat.completions.create")


