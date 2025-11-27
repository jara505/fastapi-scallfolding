import os
from jinja2 import Template
from pathlib import Path
from typing import Dict

BASE_TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"


def get_template_path(style: str, name: str) -> Path:
    """
    style = 'clean' | 'structured'
    name = file template name, e.g., 'pyproject.toml'
    """
    path = BASE_TEMPLATE_DIR / style / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path


def render_template(path: Path, ctx: Dict[str, str]) -> str:
    content = path.read_text()
    template = Template(content)
    return template.render(**ctx)


def ensure_empty_directory(path: Path):
    if path.exists():
        raise FileNotFoundError(f"Target directory already exists: {path}")
    path.mkdir(parents=True)


def create_project(meta: Dict[str, str]):
    project_name = meta["project_name"]
    style = meta["style"]
    root = Path(project_name)
    ensure_empty_directory(root)

    # src/<project_name>
    src_dir = root / "src" / project_name
    src_dir.mkdir(parents=True)

    # subfolders para structured
    if style == "structured":
        for subfolder in ["api", "core", "models"]:
            (src_dir / subfolder).mkdir()
            (src_dir / subfolder / "__init__.py").write_text("")

    # archivos a renderizar
    template_files = {
        "pyproject.toml.j2": root / "pyproject.toml",
        "README.md.j2": root / "README.md",
    }

    if style == "clean":
        template_files["package_init.py.j2"] = src_dir / "__init__.py"
        template_files[".gitignore"] = root / ".gitignore"
    elif style == "structured":
        template_files["main.py.j2"] = src_dir / "main.py"
        template_files["api/routes.py.j2"] = src_dir / "api/routes.py"
        template_files["core/config.py.j2"] = src_dir / "core/config.py"
        template_files["models/example.py.j2"] = src_dir / "models/example.py"
        template_files["requirements.txt"] = root / "requirements.txt"
        template_files[".env"] = root / ".env"

    for template_name, output_path in template_files.items():
        t_path = get_template_path(style, template_name)
        # solo render si es .j2, si no copiar literal
        if template_name.endswith(".j2"):
            output_path.write_text(render_template(t_path, meta))
        else:
            output_path.write_text(t_path.read_text())

    # tests
    if meta.get("include_tests"):
        tests_dir = root / "tests"
        tests_dir.mkdir()
        try:
            t_path = get_template_path(style, "test_basic.py")
            (tests_dir / "test_basic.py").write_text(
                render_template(t_path, meta))
        except FileNotFoundError:
            pass

    print(f"Project created at: {root.resolve()}")
