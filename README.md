# Planning Agent

A Python-based coding agent that follows a planning workflow. When a user provides a requirement, the agent first generates a Markdown plan, waits for user approval, and then proceeds to implement the files.

## Features

- **Planning Workflow**: Generates a detailed plan before implementation
- **User Approval**: Waits for explicit user approval before proceeding
- **File Generation**: Automatically creates files based on the approved plan
- **Multiple AI Providers**: Supports OpenAI, Anthropic, or mock mode for testing
- **CLI Interface**: Easy-to-use command-line interface with rich output
- **Extensible**: Easy to add new AI providers or customize the workflow

## Installation

### From Source

```bash
git clone https://github.com/DRunkPiano114/planning-agent.git
cd planning-agent
pip install -e .
```

### Using pip

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Basic Usage

Run the agent with a requirement:

```bash
planning-agent run "Create a simple calculator application"
```

This will:
1. Generate a plan based on your requirement
2. Display the plan and ask for approval
3. Generate and write files based on the approved plan

### Using Different AI Providers

#### Mock Mode (Default - No API Key Required)

```bash
planning-agent run "Create a TODO list application" --model mock
```

#### OpenAI

```bash
export OPENAI_API_KEY=your_api_key
planning-agent plan "Create a web scraper" --model openai
```

Notes:
- The plan output is **Markdown** and is printed to the terminal (it is **not** written to a `plans/` folder).
- You can override the model with `--openai-model` or via `OPENAI_MODEL`.

#### Anthropic Claude

```bash
export ANTHROPIC_API_KEY=your_api_key
planning-agent run "Create a REST API" --model anthropic
```

### Advanced Options

#### Specify Output Directory

```bash
planning-agent run "Create a blog engine" --output-dir ./my-project
```

#### Auto-approve Plan

```bash
planning-agent run "Create a game" --auto-approve
```

#### Overwrite Existing Files

```bash
planning-agent run "Create utilities" --overwrite
```

### Plan-Only Mode

Generate a plan without implementing it:

```bash
planning-agent plan "Create a machine learning pipeline"
```

### Prompt Iteration

You can override the system prompt from a file (easy to iterate without code changes):

```bash
planning-agent plan "Build a TODO app" --model openai --prompt-file ./my_prompt.txt
```

### Model Overrides

```bash
export OPENAI_API_KEY=your_api_key
export OPENAI_MODEL=gpt-4o-mini
planning-agent plan "Create a web scraper" --model openai
```

## Python API

You can also use the Planning Agent programmatically:

```python
from planning_agent.agent import PlanningAgent

# Initialize the agent
agent = PlanningAgent(model_provider="mock")

# Generate a plan
requirement = "Create a simple web server"
plan = agent.generate_plan(requirement)
print(plan)

# Approve the plan
agent.approve_plan()

# Implement the plan
files = agent.implement_plan(output_dir="./output")

# Write files to disk
agent.write_files(files)
```

## Project Structure

```
planning-agent/
├── planning_agent/
│   ├── __init__.py
│   ├── agent.py          # Core agent implementation
│   └── cli.py            # Command-line interface
├── tests/
│   ├── __init__.py
│   └── test_agent.py     # Test suite
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

## Development

### Running Tests

```bash
pytest tests/
```

### Running Tests with Coverage

```bash
pytest tests/ --cov=planning_agent --cov-report=html
```

## Architecture

The Planning Agent follows a simple three-step workflow:

1. **Plan Generation**: Takes a user requirement and generates a detailed Markdown plan
   - Uses configurable AI providers (OpenAI, Anthropic, or mock)
   - Structures the plan with clear sections and actionable items

2. **User Approval**: Displays the plan and waits for user confirmation
   - Interactive prompt in CLI mode
   - Can be bypassed with `--auto-approve` flag

3. **Implementation**: Generates files based on the approved plan
   - Parses the plan to identify files to create
   - Generates appropriate content for each file
   - Writes files to the specified output directory

## Examples

### Example 1: Simple Calculator

```bash
planning-agent run "Create a simple calculator with add, subtract, multiply, and divide functions"
```

### Example 2: Web Scraper

```bash
planning-agent run "Create a web scraper that extracts article titles from a news website" --output-dir ./scraper
```

### Example 3: REST API

```bash
planning-agent run "Create a REST API with Flask for managing a todo list" --model openai
```

## License

MIT License

## Author

DRunkPiano114
