import typer
from InquirerPy import inquirer
from scallfold.compatibility import run as check_env
from scallfold.project.initializer import initialize_project
from scallfold.project.structure import create_basic_structure

app = typer.Typer()

@app.callback()
def main():
    check_env() 


@app.command()
def create():
    name = inquirer.text(
        message="Project name: ",
        validate=lambda x: len(x) > 0,
    ).execute()

    project_type = inquirer.select(
        message="select project type: ",
        choices = ["Empty project", "Structured FastAPI project"],
    ).execute()
    
    project_path = initialize_project(name)
    if project_type == "Structured FastAPI project":
        create_basic_structure(project_path)

    print(f"Project created in {project_path}")


if __name__ == "__main__":
    app()
