"""
Core Planning Agent implementation.

This module implements the main planning agent workflow:
1. Receive user requirement
2. Generate a Markdown plan
3. Wait for user approval
4. Implement the files based on the approved plan
"""

import os
from typing import Any, List, Optional
from dataclasses import dataclass

from planning_agent.providers import AnthropicPlanProvider, MockPlanProvider, OpenAIPlanProvider, PlanProvider


@dataclass
class FileToGenerate:
    """Represents a file to be generated."""
    path: str
    content: str
    description: str


class PlanningAgent:
    """
    A coding agent that follows a planning workflow.
    
    The agent:
    1. Takes a user requirement
    2. Generates a Markdown plan
    3. Waits for user approval
    4. Implements files based on the plan
    """
    
    def __init__(
        self,
        model_provider: str = "mock",
        *,
        prompt_file: Optional[str] = None,
        system_prompt: Optional[str] = None,
        openai_model: Optional[str] = None,
        openai_temperature: float = 0.2,
        openai_client: Any = None,
        anthropic_model: Optional[str] = None,
    ):
        """
        Initialize the Planning Agent.
        
        Args:
            model_provider: The AI model provider to use ("openai", "anthropic", or "mock")
            prompt_file: Optional file path to a prompt override (string content used as system prompt)
            system_prompt: Optional system prompt override (ignored if prompt_file is provided)
            openai_model: Optional OpenAI model override (defaults to env OPENAI_MODEL or gpt-4o-mini)
            openai_temperature: OpenAI temperature
            openai_client: Optional injected OpenAI client (useful for tests)
            anthropic_model: Optional Anthropic model override (defaults to env ANTHROPIC_MODEL)
        """
        self.model_provider = model_provider
        self.current_plan = None
        self.plan_approved = False
        self.plan_provider: PlanProvider = self._build_plan_provider(
            model_provider=model_provider,
            prompt_file=prompt_file,
            system_prompt=system_prompt,
            openai_model=openai_model,
            openai_temperature=openai_temperature,
            openai_client=openai_client,
            anthropic_model=anthropic_model,
        )

    def _build_plan_provider(
        self,
        *,
        model_provider: str,
        prompt_file: Optional[str],
        system_prompt: Optional[str],
        openai_model: Optional[str],
        openai_temperature: float,
        openai_client: Any,
        anthropic_model: Optional[str],
    ) -> PlanProvider:
        if model_provider == "mock":
            return MockPlanProvider()
        if model_provider == "openai":
            return OpenAIPlanProvider(
                model=openai_model,
                temperature=openai_temperature,
                prompt_file=prompt_file,
                system_prompt=system_prompt,
                client=openai_client,
            )
        if model_provider == "anthropic":
            return AnthropicPlanProvider(
                model=anthropic_model,
                prompt_file=prompt_file,
                system_prompt=system_prompt,
            )
        raise ValueError(f"Unknown model provider: {model_provider}")
        
    def generate_plan(self, requirement: str) -> str:
        """
        Generate a Markdown plan based on the user requirement.
        
        Args:
            requirement: The user's coding requirement
            
        Returns:
            A Markdown-formatted plan
        """
        plan = self.plan_provider.generate_plan(requirement)
        self.current_plan = plan
        self.plan_approved = False
        return plan
    
    def approve_plan(self) -> None:
        """Mark the current plan as approved."""
        if not self.current_plan:
            raise ValueError("No plan to approve. Generate a plan first.")
        self.plan_approved = True
    
    def reject_plan(self) -> None:
        """Mark the current plan as rejected."""
        self.plan_approved = False
        self.current_plan = None
    
    def implement_plan(self, output_dir: str = ".") -> List[FileToGenerate]:
        """
        Implement the approved plan by generating files.
        
        Args:
            output_dir: Directory where files should be created
            
        Returns:
            List of FileToGenerate objects
            
        Raises:
            ValueError: If plan is not approved
        """
        if not self.plan_approved:
            raise ValueError("Plan must be approved before implementation")
        
        if not self.current_plan:
            raise ValueError("No plan to implement")
        
        # Generate files based on the plan
        files = self._generate_files_from_plan(self.current_plan, output_dir)
        
        return files
    
    def _generate_files_from_plan(self, plan: str, output_dir: str) -> List[FileToGenerate]:
        """
        Parse the plan and generate file contents.
        
        Args:
            plan: The approved plan
            output_dir: Output directory
            
        Returns:
            List of files to generate
        """
        # For mock implementation, generate basic files
        if self.model_provider == "mock":
            return self._generate_mock_files(output_dir)
        
        # For real LLM providers, we would parse the plan and generate actual content
        # This is a simplified implementation
        files = []
        
        # Extract file names from plan (basic parsing)
        import re
        file_pattern = r'`([^`]+\.(py|md|txt|json|yaml))`'
        matches = re.findall(file_pattern, plan)
        
        for match in matches:
            filename = match[0]
            filepath = os.path.join(output_dir, filename)
            
            # Generate basic content based on filename
            content = self._generate_file_content(filename, plan)
            
            files.append(FileToGenerate(
                path=filepath,
                content=content,
                description=f"Generated {filename}"
            ))
        
        return files
    
    def _generate_mock_files(self, output_dir: str) -> List[FileToGenerate]:
        """Generate mock files for testing."""
        return [
            FileToGenerate(
                path=os.path.join(output_dir, "main.py"),
                content='"""Main application entry point."""\n\ndef main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()\n',
                description="Main application file"
            ),
            FileToGenerate(
                path=os.path.join(output_dir, "utils.py"),
                content='"""Utility functions."""\n\ndef helper_function():\n    """A helpful utility function."""\n    pass\n',
                description="Utility functions"
            ),
            FileToGenerate(
                path=os.path.join(output_dir, "README.md"),
                content='# Project\n\nThis project was generated by the planning agent.\n\n## Usage\n\n```bash\npython main.py\n```\n',
                description="Project documentation"
            )
        ]
    
    def _generate_file_content(self, filename: str, plan: str) -> str:
        """
        Generate file content based on filename and plan.
        
        Args:
            filename: Name of the file
            plan: The implementation plan
            
        Returns:
            File content as string
        """
        # Basic content generation based on file type
        if filename.endswith('.py'):
            return f'"""Generated Python file: {filename}"""\n\n# TODO: Implement based on plan\n'
        elif filename.endswith('.md'):
            return f'# {filename}\n\nGenerated documentation.\n'
        elif filename.endswith('.json'):
            return '{}\n'
        elif filename.endswith('.yaml'):
            return '# YAML configuration\n'
        else:
            return '# Generated file\n'
    
    def write_files(self, files: List[FileToGenerate], overwrite: bool = False) -> None:
        """
        Write generated files to disk.
        
        Args:
            files: List of files to write
            overwrite: Whether to overwrite existing files
            
        Raises:
            FileExistsError: If file exists and overwrite is False
        """
        for file in files:
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(file.path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            # Check if file exists
            if os.path.exists(file.path) and not overwrite:
                raise FileExistsError(f"File already exists: {file.path}")
            
            # Write file
            with open(file.path, 'w') as f:
                f.write(file.content)
