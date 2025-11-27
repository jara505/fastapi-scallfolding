import typer
from InquirerPy import inquirer
from scallfold.compatibility import run as check_env
from scallfold.project.initializer import initialize_project
from scallfold.project.generator import create_project

app = typer.Typer()

@app.callback()
def main():
    check_env() 


@app.command()
def create():
    # prompts (TUI-style)
    name = inquirer.text(message="Project name:", validate=lambda s: len(s.strip()) > 0).execute()

    style = inquirer.select(message="Project type:", choices=["clean", "structured"]).execute()

    include_tests = inquirer.confirm(message="Include tests?", default=False).execute()

    description = inquirer.text(message="Description (optional):", default="").execute()

    version = inquirer.text(message="Version:", default="0.1.0").execute()

    meta = {
        "project_name": name,
        "style": style,
        "include_tests": include_tests,
        "description": description,
        "version": version,
    }
    try:
        create_project(meta)
    except FileExistsError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
