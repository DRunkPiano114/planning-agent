from setuptools import setup, find_packages

setup(
    name="planning-agent",
    version="0.1.0",
    description="A coding agent with a planning workflow",
    author="DRunkPiano114",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.18.0",
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "planning-agent=planning_agent.cli:main",
        ],
    },
    python_requires=">=3.8",
)
