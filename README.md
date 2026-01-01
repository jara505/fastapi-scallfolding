# scallpy

[![PyPI version](https://img.shields.io/pypi/v/scallpy)](https://pypi.org/project/scallpy/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/jara505/fastapi-scallfolding/blob/main/LICENSE) [![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

A command-line tool to scaffold FastAPI projects, inspired by `vitejs`.

## Overview

`scallpy` helps you quickly set up new FastAPI projects with sensible defaults, providing both a "clean" and a "structured" project template. It follows a minimal philosophy: all features are opt-in. By default, you get a clean FastAPI project with no extras. Optional parameters include: `--use-db` (adds database support), `--use-orm` (adds ORM models), `--include-tests` (adds basic tests, default: yes), `--path` (custom output directory).

## Installation

### For Users

**Requirements:** Python 3.10 or higher.

## Compatibility

Scallpy is compatible with Linux and Windows operating systems.

To install `scallpy` and use it to create new projects:

```bash
pip install scallpy
```

After installation, you can use the `scallpy` command globally.

### For Developers (Contributing to scallpy)

If you want to contribute to `scallpy` or modify its source code:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jara505/fastapi-scallfolding.git
    cd fastapi-scallfolding
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install in editable mode with dev dependencies:**
    ```bash
    pip install -e ".[dev]"
    ```
4.  **Run tests:**
    ```bash
    pytest
    ```

**Note:** For stability, use Poetry 1.x (e.g., `pip install poetry==1.8.3`) when working with generated projects. Poetry 2.x may have compatibility issues.

## Usage

`scallpy` provides a `create` command to generate new FastAPI projects.

### Interactive Mode

To create a project interactively, simply run:

```bash
scallpy create
```
The CLI will guide you through selecting a project name, type, and other options.

### Non-Interactive Mode (with parameters)

You can also provide parameters directly to bypass interactive prompts, which is useful for scripting or quick setups.

```bash
scallpy create --name <project-name> --type <project-type> [--use-db] [--use-orm] [--path <output-path>]
```

### Quickstart

Get started quickly with a structured project including database and ORM:

```bash
scallpy create --name my-api --type structured --use-db --use-orm
cd my-api
pip install poetry==1.8.3
poetry install
poetry run uvicorn my-api.main:app --reload
```

Visit `http://127.0.0.1:8000` to see your API running!

**Parameters:**

*   `--name` or `-n`: The name of your new FastAPI project. This will also be the name of the directory created for your project.
*   `--type` or `-t`: The type of project structure to generate.
    *   `clean`: A minimal FastAPI project with a single `main.py` file.
    *   `structured`: A more organized FastAPI project with separate modules for API routes, core configuration, and models.
*   `--use-db` (Optional): Include database support in the project. Generates `core/database.py` with SQLAlchemy configuration, engine setup, and commented imports for models. Use as a flag (e.g., `--use-db`).
*   `--use-orm` (Optional): Include ORM (Object-Relational Mapper) support in the project. Generates `models/base.py` (Base class for SQLAlchemy models) and `models/user.py` (example User model with id, name, email fields). Requires `--use-db`. Use as a flag (e.g., `--use-orm`).
*   `--path` or `-p` (Optional): The directory where the new project folder will be created. If not specified, the project will be created in the current working directory. If `.` is provided, the project folder will be created inside the current directory.

**Example:**

```bash
scallpy create --name my-awesome-api --type structured --path ./projects
```

## Project Structures

### Clean Project
```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_basic.py
├── .gitignore
├── pyproject.toml
└── README.md
```

### Structured Project
```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── config.py
│       ├── main.py
│       └── models/
│           └── __init__.py
├── tests/
│   └── test_basic.py
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Running Your Generated Project

After `scallpy` creates your project, it will provide specific instructions. Generally, the steps are:

1.  **Navigate into your new project directory:**
    ```bash
    cd <your-project-name>
    ```
2.  **Install dependencies using Poetry:**
    ```bash
    pip install poetry==1.8.3
    poetry install
    ```
3.  **Run the FastAPI development server:**
    *   **For `clean` projects:**
        ```bash
        poetry run uvicorn <your-project-name>.main:app --reload
        ```
    *   **For `structured` projects:**
        ```bash
        poetry run uvicorn <your-project-name>.main:app --reload
        ```
    (Replace `<your-project-name>` with the actual name you gave your project).

Your FastAPI application will typically be available at `http://127.0.0.1:8000`.

**Note:** Generated projects use Poetry for dependency management. Install Poetry 1.8.3 (`pip install poetry==1.8.3`) to avoid compatibility issues with Poetry 2.x, which may cause errors in some environments. Poetry ensures reproducible builds and virtual environments.

## Contributing

We welcome contributions! Please feel free to open issues or submit pull requests.

## Testing

To run the test suite:
```bash
pytest
```

Ensure all tests pass before submitting pull requests.

## License

This project is licensed under the MIT License.
