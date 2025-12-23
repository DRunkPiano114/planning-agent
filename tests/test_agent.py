"""
Tests for the Planning Agent.
"""

import os
import tempfile
import pytest
from planning_agent.agent import PlanningAgent, FileToGenerate
from planning_agent.providers.openai_provider import OpenAIPlanProvider


class TestPlanningAgent:
    """Test suite for PlanningAgent class."""
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = PlanningAgent(model_provider="mock")
        assert agent.model_provider == "mock"
        assert agent.current_plan is None
        assert agent.plan_approved is False
    
    def test_generate_plan(self):
        """Test plan generation."""
        agent = PlanningAgent(model_provider="mock")
        requirement = "Create a simple calculator application"
        
        plan = agent.generate_plan(requirement)
        
        assert plan is not None
        assert isinstance(plan, str)
        assert len(plan) > 0
        assert "Implementation Plan" in plan
        assert requirement in plan
        assert agent.current_plan == plan
        assert agent.plan_approved is False
    
    def test_approve_plan(self):
        """Test plan approval."""
        agent = PlanningAgent(model_provider="mock")
        agent.generate_plan("Test requirement")
        
        agent.approve_plan()
        
        assert agent.plan_approved is True
    
    def test_approve_plan_without_generation_raises_error(self):
        """Test that approving without a plan raises an error."""
        agent = PlanningAgent(model_provider="mock")
        
        with pytest.raises(ValueError, match="No plan to approve"):
            agent.approve_plan()
    
    def test_reject_plan(self):
        """Test plan rejection."""
        agent = PlanningAgent(model_provider="mock")
        agent.generate_plan("Test requirement")
        
        agent.reject_plan()
        
        assert agent.plan_approved is False
        assert agent.current_plan is None
    
    def test_implement_plan_requires_approval(self):
        """Test that implementation requires plan approval."""
        agent = PlanningAgent(model_provider="mock")
        agent.generate_plan("Test requirement")
        
        with pytest.raises(ValueError, match="Plan must be approved"):
            agent.implement_plan()
    
    def test_implement_plan(self):
        """Test plan implementation."""
        agent = PlanningAgent(model_provider="mock")
        agent.generate_plan("Create a simple application")
        agent.approve_plan()
        
        files = agent.implement_plan()
        
        assert len(files) > 0
        assert all(isinstance(f, FileToGenerate) for f in files)
        assert all(hasattr(f, 'path') for f in files)
        assert all(hasattr(f, 'content') for f in files)
        assert all(hasattr(f, 'description') for f in files)
    
    def test_write_files(self):
        """Test writing files to disk."""
        agent = PlanningAgent(model_provider="mock")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            files = [
                FileToGenerate(
                    path=os.path.join(tmpdir, "test.py"),
                    content="print('hello')",
                    description="Test file"
                )
            ]
            
            agent.write_files(files)
            
            assert os.path.exists(os.path.join(tmpdir, "test.py"))
            with open(os.path.join(tmpdir, "test.py"), 'r') as f:
                content = f.read()
            assert content == "print('hello')"
    
    def test_write_files_creates_directories(self):
        """Test that write_files creates necessary directories."""
        agent = PlanningAgent(model_provider="mock")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "nested", "dir", "test.py")
            files = [
                FileToGenerate(
                    path=nested_path,
                    content="print('hello')",
                    description="Test file"
                )
            ]
            
            agent.write_files(files)
            
            assert os.path.exists(nested_path)
    
    def test_write_files_without_overwrite_raises_error(self):
        """Test that writing to existing file without overwrite raises error."""
        agent = PlanningAgent(model_provider="mock")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.py")
            
            # Create file first
            with open(filepath, 'w') as f:
                f.write("existing content")
            
            files = [
                FileToGenerate(
                    path=filepath,
                    content="new content",
                    description="Test file"
                )
            ]
            
            with pytest.raises(FileExistsError):
                agent.write_files(files, overwrite=False)
    
    def test_write_files_with_overwrite(self):
        """Test that overwrite flag allows overwriting files."""
        agent = PlanningAgent(model_provider="mock")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.py")
            
            # Create file first
            with open(filepath, 'w') as f:
                f.write("existing content")
            
            files = [
                FileToGenerate(
                    path=filepath,
                    content="new content",
                    description="Test file"
                )
            ]
            
            agent.write_files(files, overwrite=True)
            
            with open(filepath, 'r') as f:
                content = f.read()
            assert content == "new content"
    
    def test_full_workflow(self):
        """Test the complete workflow from requirement to file generation."""
        agent = PlanningAgent(model_provider="mock")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Generate plan
            requirement = "Create a simple web scraper"
            plan = agent.generate_plan(requirement)
            assert plan is not None
            
            # Approve plan
            agent.approve_plan()
            assert agent.plan_approved is True
            
            # Implement plan
            files = agent.implement_plan(output_dir=tmpdir)
            assert len(files) > 0
            
            # Write files
            agent.write_files(files)
            
            # Verify files exist
            for file in files:
                assert os.path.exists(file.path)


class TestFileToGenerate:
    """Test suite for FileToGenerate dataclass."""
    
    def test_file_to_generate_creation(self):
        """Test creating a FileToGenerate object."""
        file = FileToGenerate(
            path="/tmp/test.py",
            content="print('hello')",
            description="Test file"
        )
        
        assert file.path == "/tmp/test.py"
        assert file.content == "print('hello')"
        assert file.description == "Test file"


class TestOpenAIPlanProvider:
    def test_generate_plan_with_injected_responses_client(self):
        calls = {}

        class FakeResponse:
            output_text = "# Implementation Plan\n\n## Files\n- `a.py`\n\n## Steps\n1. Do it\n\n## Open Questions\n- None"

        class FakeResponses:
            def create(self, **kwargs):
                calls["kwargs"] = kwargs
                return FakeResponse()

        class FakeClient:
            responses = FakeResponses()

        provider = OpenAIPlanProvider(api_key="test", model="test-model", client=FakeClient())
        plan = provider.generate_plan("Build X")

        assert "Implementation Plan" in plan
        assert "Build X" in calls["kwargs"]["input"][1]["content"]

    def test_generate_plan_falls_back_to_chat_completions(self):
        class FakeChoiceMsg:
            content = "# Implementation Plan\n\n## Files\n- `b.py`\n\n## Steps\n1. Do it\n\n## Open Questions\n- None"

        class FakeChoice:
            message = FakeChoiceMsg()

        class FakeChatCompletions:
            def create(self, **kwargs):
                return type("Resp", (), {"choices": [FakeChoice()]})()

        class FakeChat:
            completions = FakeChatCompletions()

        class FakeClient:
            chat = FakeChat()

        provider = OpenAIPlanProvider(api_key="test", model="test-model", client=FakeClient())
        plan = provider.generate_plan("Build Y")
        assert "Implementation Plan" in plan
