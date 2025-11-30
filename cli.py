import typer
from InquirerPy import inquirer
from scallfold.compatibility import run as check_env
from scallfold.project.initializer import initialize_project
from scallfold.project.generator import create_project
from scallfold.utils.prompts import collect_project_meta

app = typer.Typer()


@app.callback()
def main():
    check_env()


@app.command()
def create():
    meta = collect_project_meta()
    try:
        create_project(meta)
    except FileExistsError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
