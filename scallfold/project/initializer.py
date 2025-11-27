import os
import re
from pathlib import Path


PROJECT_NAME_PATTERN = r"^[a-zA-Z_][a-zA-Z0-9_-]*$"

def validate_project_name(name: str) -> bool:
    if not re.match(PROJECT_NAME_PATTERN, name):
        raise ValueError(f"Invalid project name: {name}")
    return True

def create_project_directory(name: str) -> Path:
    project_path = Path(name)
    if project_path.exists():
        raise ValueError(f"Project directory already exists: {project_path}")
    project_path.mkdir(parents=True)
    return project_path


def initialize_project(name: str) -> Path:
    validate_project_name(name)
    project_dir = create_project_directory(name)
    return project_dir



