import copy

import typer
from pathlib import Path
from typing import Dict, Any, Optional

from scallfold.project.structure import STRUCTURES
from scallfold.utils.filesystem import ensure_empty_directory
from scallfold.utils.templating import get_template_path, render_template


def create_project(meta: Dict[str, Any], root_path: Optional[Path] = None, silent: bool = False):
    """
    Generates a project structure based on metadata and a declarative structure map.
    
    Args:
        meta: Project metadata dictionary
        root_path: Where to create the project
        silent: If True, skip printing the "Next steps" guide
    """
    style = meta["style"]
    project_name = meta["project_name"]
    # If a path is provided, use it as the base. Otherwise, use the current directory.
    # Use absolute path for consistent behavior with subprocess calls
    base_path = (root_path.resolve() if root_path else Path.cwd())
    root = base_path / project_name

    ensure_empty_directory(root)

    base_structure = STRUCTURES.get(style)
    if not base_structure:
        raise ValueError(f"Unknown project style: {style}")

    structure = copy.deepcopy(base_structure)

    if style == "structured":
        if meta.get("use_db"):
            structure["templates"]["core/database.py.j2"] = "src/{project_name}/core/database.py"

        if meta.get("use_orm"):
            # 'models/base.py.j2' is used by the ORM example
            structure["templates"]["models/base.py.j2"] = "src/{project_name}/models/base.py"
            structure["templates"]["models/user.py.j2"] = "src/{project_name}/models/user.py"

    # If not including tests, remove test-related entries
    if not meta.get("include_tests"):
        if "tests" in structure.get("dirs", []):
            structure["dirs"] = [d for d in structure["dirs"] if d != "tests"]
        test_templates = ["test_basic.py.j2", "conftest.py.j2"]
        structure["templates"] = {
            k: v for k, v in structure.get("templates", {}).items()
            if k not in test_templates
        }

    # Create directories
    for dir_path in structure.get("dirs", []):
        path = root / dir_path.format(**meta)
        path.mkdir(parents=True, exist_ok=True)

    # Render templates
    for template_name, output_path in structure.get("templates", {}).items():
        template_path = get_template_path(style, template_name)
        final_path = root / output_path.format(**meta)
        final_path.write_text(render_template(template_path, meta))

    # Copy static files
    for file_name, output_path in structure.get("files", {}).items():
        static_file_path = get_template_path(style, file_name)
        final_path = root / output_path.format(**meta)
        final_path.write_text(static_file_path.read_text())

    # Create empty __init__.py files
    for init_path in structure.get("init_files", []):
        path = root / init_path.format(**meta)
        path.touch()
    
    # Show next steps only when not in silent mode
    if not silent:
        typer.secho(f"\nProject '{project_name}' created successfully!", fg=typer.colors.GREEN, bold=True)
        typer.secho("\nNext steps:", bold=True)

        # Use relative path for cd command if possible
        try:
            cd_path = Path(root).relative_to(Path.cwd())
        except ValueError:
            cd_path = root.resolve()

        typer.echo(f"  cd {cd_path}")
        typer.echo("  pip install poetry==1.8.3")
        typer.echo("  poetry install")

        if style == "structured":
            run_command = f"poetry run uvicorn {project_name}.main:app --reload"
            typer.secho(f"  {run_command}", bold=True)
        else: # clean - now main.py is also inside src/{project_name}
            run_command = f"poetry run uvicorn {project_name}.main:app --reload"
            typer.secho(f"  {run_command}", bold=True)
    
    return root
