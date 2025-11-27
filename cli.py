import typer
from scallfold.compatibility import run as check_env

app = typer.Typer()

@app.callback()
def main():
    check_env() 
@app.command()
def create():
    """
    Creates a new project.
    """
    print(f"Creating project")

@app.command()
def hello():
    """
    Say hello.
    """
    print("Hello, world!")

if __name__ == "__main__":
    app()
