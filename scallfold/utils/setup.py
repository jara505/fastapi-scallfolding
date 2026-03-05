import os
import subprocess
import sys
from pathlib import Path

import typer


def setup_project(project_path: Path):
    """Creates a venv, installs Poetry 1.8.3, and runs poetry install."""
    # Use .venv to match Poetry's default behavior
    venv_path = project_path / ".venv"
    python = sys.executable
    
    # Clean environment to avoid conflicts with active venv
    clean_env = os.environ.copy()
    clean_env.pop("VIRTUAL_ENV", None)
    clean_env["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"

    typer.secho("\n⚙ Setting up project...", fg=typer.colors.CYAN, bold=True)

    # Step 1: Create venv
    typer.echo("  Creating virtual environment...")
    try:
        result = subprocess.run(
            [python, "-m", "venv", str(venv_path)],
            capture_output=True, text=True,
            timeout=60,
            env=clean_env,
        )
    except subprocess.TimeoutExpired:
        typer.secho("  Failed to create venv: Timeout", fg=typer.colors.RED)
        return False
    except Exception as e:
        typer.secho(f"  Failed to create venv: {e}", fg=typer.colors.RED)
        return False
        
    if result.returncode != 0:
        typer.secho(f"  Failed to create venv: {result.stderr.strip()}", fg=typer.colors.RED)
        return False

    # Determine paths inside the venv
    if sys.platform == "win32":
        pip = str(venv_path / "Scripts" / "pip")
        poetry = str(venv_path / "Scripts" / "poetry")
    else:
        pip = str(venv_path / "bin" / "pip")
        poetry = str(venv_path / "bin" / "poetry")

    # Step 2: Install Poetry
    typer.echo("  Installing poetry==1.8.3...")
    try:
        result = subprocess.run(
            [pip, "install", "poetry==1.8.3", "-q"],
            capture_output=True, text=True,
            timeout=120,
            env=clean_env,
        )
    except subprocess.TimeoutExpired:
        typer.secho("  Failed to install Poetry: Timeout", fg=typer.colors.RED)
        return False
    except Exception as e:
        typer.secho(f"  Failed to install Poetry: {e}", fg=typer.colors.RED)
        return False
        
    if result.returncode != 0:
        typer.secho(f"  Failed to install Poetry: {result.stderr.strip()}", fg=typer.colors.RED)
        return False

    # Step 3: Poetry install
    typer.echo("  Installing dependencies...")
    try:
        result = subprocess.run(
            [poetry, "install"],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=300,
            env=clean_env,
        )
    except subprocess.TimeoutExpired:
        typer.secho("  Failed to install dependencies: Timeout", fg=typer.colors.RED)
        return False
    except Exception as e:
        typer.secho(f"  Failed to install dependencies: {e}", fg=typer.colors.RED)
        return False
        
    if result.returncode != 0:
        typer.secho(f"  Failed to install dependencies: {result.stderr.strip()}", fg=typer.colors.RED)
        typer.secho(f"  Stdout: {result.stdout.strip()}", fg=typer.colors.YELLOW)
        return False

    typer.secho("  ✔ Setup complete!", fg=typer.colors.GREEN, bold=True)
    return True
