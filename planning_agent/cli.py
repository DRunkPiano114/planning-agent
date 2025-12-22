"""
Command-line interface for the Planning Agent.
"""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from planning_agent.agent import PlanningAgent


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Planning Agent - A coding agent with a planning workflow."""
    pass


@cli.command()
@click.argument("requirement")
@click.option(
    "--model",
    "-m",
    type=click.Choice(["mock", "openai", "anthropic"]),
    default="mock",
    help="AI model provider to use",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Output directory for generated files",
)
@click.option(
    "--auto-approve",
    "-y",
    is_flag=True,
    help="Automatically approve the plan without confirmation",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Overwrite existing files",
)
def run(requirement: str, model: str, output_dir: str, auto_approve: bool, overwrite: bool):
    """
    Run the planning agent with a requirement.
    
    REQUIREMENT: The coding requirement to implement
    """
    console.print("\n[bold blue]🤖 Planning Agent[/bold blue]\n")
    
    # Initialize agent
    agent = PlanningAgent(model_provider=model)
    
    # Step 1: Generate plan
    console.print("[bold]Step 1: Generating plan...[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing requirement...", total=None)
        plan = agent.generate_plan(requirement)
        progress.update(task, completed=True)
    
    console.print("\n[bold green]✓ Plan generated![/bold green]\n")
    
    # Display the plan
    console.print(Panel(
        Markdown(plan),
        title="[bold]Implementation Plan[/bold]",
        border_style="green",
    ))
    
    # Step 2: Wait for approval
    console.print("\n[bold]Step 2: Plan approval[/bold]")
    
    if auto_approve:
        console.print("[yellow]Auto-approving plan...[/yellow]")
        approved = True
    else:
        approved = Confirm.ask("Do you approve this plan?", default=True)
    
    if not approved:
        agent.reject_plan()
        console.print("[red]Plan rejected. Exiting.[/red]")
        return
    
    agent.approve_plan()
    console.print("[bold green]✓ Plan approved![/bold green]\n")
    
    # Step 3: Implement files
    console.print("[bold]Step 3: Implementing files...[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating files...", total=None)
        files = agent.implement_plan(output_dir=output_dir)
        progress.update(task, completed=True)
    
    console.print(f"\n[bold green]✓ Generated {len(files)} file(s)![/bold green]\n")
    
    # Display files to be created
    console.print("[bold]Files to be created:[/bold]")
    for file in files:
        console.print(f"  • {file.path} - {file.description}")
    
    # Write files
    console.print("\n[bold]Writing files...[/bold]")
    
    try:
        agent.write_files(files, overwrite=overwrite)
        console.print("[bold green]✓ All files written successfully![/bold green]\n")
        console.print(f"[dim]Files created in: {output_dir}[/dim]")
    except FileExistsError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Use --overwrite flag to overwrite existing files[/yellow]")
        return
    except Exception as e:
        console.print(f"[red]Error writing files: {e}[/red]")
        return


@cli.command()
@click.argument("requirement")
@click.option(
    "--model",
    "-m",
    type=click.Choice(["mock", "openai", "anthropic"]),
    default="mock",
    help="AI model provider to use",
)
def plan(requirement: str, model: str):
    """
    Generate a plan without implementing it.
    
    REQUIREMENT: The coding requirement to plan for
    """
    console.print("\n[bold blue]🤖 Planning Agent - Plan Only Mode[/bold blue]\n")
    
    agent = PlanningAgent(model_provider=model)
    
    console.print("[bold]Generating plan...[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing requirement...", total=None)
        plan_text = agent.generate_plan(requirement)
        progress.update(task, completed=True)
    
    console.print("\n[bold green]✓ Plan generated![/bold green]\n")
    
    console.print(Panel(
        Markdown(plan_text),
        title="[bold]Implementation Plan[/bold]",
        border_style="green",
    ))


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
