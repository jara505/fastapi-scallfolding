import typer
from pathlib import Path
from typing import Optional
from InquirerPy import inquirer
from scallfold.compatibility import run as check_env
from scallfold.project.generator import create_project
from scallfold.utils.prompts import collect_project_meta

app = typer.Typer()


@app.callback()
def main():
    check_env()


@app.command()
def create(
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Name of the project."
    ),
    style: Optional[str] = typer.Option(
        None, "--type", "-t", help="Type of project structure ('clean' or 'structured')."
    ),
    use_db: Optional[bool] = typer.Option(
        None, "--use-db", help="Include database support."
    ),
    use_orm: Optional[bool] = typer.Option(
        None, "--use-orm", help="Include ORM support."
    ),
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Path to create the project in."
    ),
):
    """
    Creates a new FastAPI project.
    """
    if name and style:
        # If arguments are provided, bypass interactive prompts
        meta = {
            "project_name": name,
            "style": style,
            "use_db": use_db if use_db is not None else False,
            "use_orm": use_orm if use_orm is not None else False,
            "include_tests": True,
            "description": "",
            "version": "0.1.0",
        }
    else:
        # Otherwise, run the interactive prompts
        meta = collect_project_meta()

    if meta["style"] == "clean" and (meta.get("use_db") or meta.get("use_orm")):
        typer.secho(
            "Warning: --use-db and --use-orm flags have no effect with '--type clean'. "
            "They are only applicable to '--type structured' projects.",
            fg=typer.colors.YELLOW,
        )

    try:
        # Pass the path to the generator. If path is None, it defaults to the project name.
        create_project(meta, root_path=path)
    except FileExistsError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
