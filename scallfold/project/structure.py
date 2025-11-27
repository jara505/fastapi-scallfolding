from pathlib import Path

def create_basic_structure(project_path: Path):
    # /app
    app_path = project_path / "app"
    app_path.mkdir()

    # /app/main.py
    (app_path / "main.py").write_text('from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"message": "Hello World"}\n')
    
    # add __init__.py
    (app_path / "__init__.py").write_text("")
