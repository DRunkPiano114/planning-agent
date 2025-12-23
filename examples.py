"""
Example usage of the Planning Agent.

This script demonstrates how to use the Planning Agent programmatically.
"""

from planning_agent.agent import PlanningAgent
import os
import tempfile


def basic_example():
    """Basic usage example."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Initialize the agent with mock provider (no API key needed)
    agent = PlanningAgent(model_provider="mock")
    
    # Define the requirement
    requirement = "Create a simple Python calculator application"
    
    # Step 1: Generate plan
    print("\n1. Generating plan...")
    plan = agent.generate_plan(requirement)
    print("\nGenerated Plan:")
    print("-" * 60)
    print(plan)
    
    # Step 2: Approve the plan
    print("\n2. Approving plan...")
    agent.approve_plan()
    print("Plan approved!")
    
    # Step 3: Implement the plan
    print("\n3. Implementing plan...")
    with tempfile.TemporaryDirectory() as tmpdir:
        files = agent.implement_plan(output_dir=tmpdir)
        
        print(f"\nGenerated {len(files)} files:")
        for file in files:
            print(f"  - {file.path}")
            print(f"    Description: {file.description}")
        
        # Step 4: Write files
        print("\n4. Writing files...")
        agent.write_files(files)
        print("Files written successfully!")
        
        # Show file contents
        print("\n5. File contents:")
        for file in files:
            print(f"\n--- {os.path.basename(file.path)} ---")
            print(file.content[:200] + "..." if len(file.content) > 200 else file.content)


def workflow_with_rejection():
    """Example showing plan rejection and regeneration."""
    print("\n\n" + "=" * 60)
    print("Example 2: Workflow with Plan Rejection")
    print("=" * 60)
    
    agent = PlanningAgent(model_provider="mock")
    
    # First attempt
    print("\n1. First plan generation...")
    requirement = "Create a web scraper"
    plan1 = agent.generate_plan(requirement)
    print("Plan generated (truncated):")
    print(plan1[:200] + "...")
    
    # Reject the plan
    print("\n2. Rejecting plan...")
    agent.reject_plan()
    print("Plan rejected!")
    
    # Generate new plan
    print("\n3. Generating new plan...")
    plan2 = agent.generate_plan(requirement + " with error handling")
    print("New plan generated (truncated):")
    print(plan2[:200] + "...")
    
    # Approve and implement
    print("\n4. Approving and implementing...")
    agent.approve_plan()
    with tempfile.TemporaryDirectory() as tmpdir:
        files = agent.implement_plan(output_dir=tmpdir)
        agent.write_files(files)
        print(f"Successfully created {len(files)} files!")


def error_handling_example():
    """Example showing error handling."""
    print("\n\n" + "=" * 60)
    print("Example 3: Error Handling")
    print("=" * 60)
    
    agent = PlanningAgent(model_provider="mock")
    
    # Try to approve without plan
    print("\n1. Attempting to approve without generating plan...")
    try:
        agent.approve_plan()
    except ValueError as e:
        print(f"Error caught: {e}")
    
    # Try to implement without approval
    print("\n2. Attempting to implement without approval...")
    agent.generate_plan("Test requirement")
    try:
        agent.implement_plan()
    except ValueError as e:
        print(f"Error caught: {e}")
    
    # Try to write to existing file without overwrite
    print("\n3. Attempting to write to existing file...")
    with tempfile.TemporaryDirectory() as tmpdir:
        from planning_agent.agent import FileToGenerate
        
        # Create a file
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, 'w') as f:
            f.write("existing content")
        
        # Try to write without overwrite
        files = [FileToGenerate(
            path=test_file,
            content="new content",
            description="test"
        )]
        
        try:
            agent.write_files(files, overwrite=False)
        except FileExistsError as e:
            print(f"Error caught: {e}")
        
        # Write with overwrite
        print("\n4. Writing with overwrite=True...")
        agent.write_files(files, overwrite=True)
        print("Successfully overwritten!")


def custom_output_directory():
    """Example with custom output directory."""
    print("\n\n" + "=" * 60)
    print("Example 4: Custom Output Directory")
    print("=" * 60)
    
    agent = PlanningAgent(model_provider="mock")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a custom directory structure
        output_dir = os.path.join(tmpdir, "my_project", "src")
        
        print(f"\n1. Generating files in: {output_dir}")
        
        agent.generate_plan("Create a modular application")
        agent.approve_plan()
        
        files = agent.implement_plan(output_dir=output_dir)
        agent.write_files(files)
        
        print(f"\n2. Files created:")
        for file in files:
            relative_path = os.path.relpath(file.path, tmpdir)
            print(f"  - {relative_path}")
        
        # List directory structure
        print(f"\n3. Directory structure:")
        for root, dirs, files_list in os.walk(tmpdir):
            level = root.replace(tmpdir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files_list:
                print(f"{subindent}{file}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Planning Agent - Usage Examples" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        # Run all examples
        basic_example()
        workflow_with_rejection()
        error_handling_example()
        custom_output_directory()
        
        print("\n\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
