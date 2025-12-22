"""
Core Planning Agent implementation.

This module implements the main planning agent workflow:
1. Receive user requirement
2. Generate a Markdown plan
3. Wait for user approval
4. Implement the files based on the approved plan
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass


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
    
    def __init__(self, model_provider: str = "mock"):
        """
        Initialize the Planning Agent.
        
        Args:
            model_provider: The AI model provider to use ("openai", "anthropic", or "mock")
        """
        self.model_provider = model_provider
        self.current_plan = None
        self.plan_approved = False
        
    def generate_plan(self, requirement: str) -> str:
        """
        Generate a Markdown plan based on the user requirement.
        
        Args:
            requirement: The user's coding requirement
            
        Returns:
            A Markdown-formatted plan
        """
        # For now, use a simple template-based approach
        # In a full implementation, this would call an LLM
        plan = self._generate_plan_with_llm(requirement)
        self.current_plan = plan
        self.plan_approved = False
        return plan
    
    def _generate_plan_with_llm(self, requirement: str) -> str:
        """
        Generate plan using the configured LLM provider.
        
        Args:
            requirement: The user's requirement
            
        Returns:
            Markdown-formatted plan
        """
        if self.model_provider == "mock":
            return self._generate_mock_plan(requirement)
        elif self.model_provider == "openai":
            return self._generate_plan_openai(requirement)
        elif self.model_provider == "anthropic":
            return self._generate_plan_anthropic(requirement)
        else:
            raise ValueError(f"Unknown model provider: {self.model_provider}")
    
    def _generate_mock_plan(self, requirement: str) -> str:
        """Generate a mock plan for testing purposes."""
        return f"""# Implementation Plan

## Requirement
{requirement}

## Proposed Solution

### Files to Create
1. `main.py` - Main application entry point
2. `utils.py` - Utility functions
3. `README.md` - Documentation

### Implementation Steps
1. Set up project structure
2. Implement core functionality
3. Add error handling
4. Write documentation
5. Test the implementation

### Dependencies
- No external dependencies required for basic implementation

## Timeline
Estimated implementation time: 30 minutes
"""
    
    def _generate_plan_openai(self, requirement: str) -> str:
        """Generate plan using OpenAI API."""
        try:
            import openai
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful coding assistant. Generate a detailed Markdown plan for implementing the user's requirement. Include files to create, implementation steps, and dependencies."
                    },
                    {
                        "role": "user",
                        "content": f"Create a detailed implementation plan for: {requirement}"
                    }
                ],
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
    
    def _generate_plan_anthropic(self, requirement: str) -> str:
        """Generate plan using Anthropic Claude API."""
        try:
            import anthropic
            
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            
            client = anthropic.Anthropic(api_key=api_key)
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a helpful coding assistant. Generate a detailed Markdown plan for implementing the following requirement. Include files to create, implementation steps, and dependencies.\n\nRequirement: {requirement}"
                    }
                ]
            )
            
            return message.content[0].text
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
    
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
            os.makedirs(os.path.dirname(file.path) or ".", exist_ok=True)
            
            # Check if file exists
            if os.path.exists(file.path) and not overwrite:
                raise FileExistsError(f"File already exists: {file.path}")
            
            # Write file
            with open(file.path, 'w') as f:
                f.write(file.content)
