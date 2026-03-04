from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, StrictUndefined

BASE_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(str(BASE_TEMPLATE_DIR)),
    undefined=StrictUndefined,
    keep_trailing_newline=True,
)


def get_template_path(style: str, name: str) -> Path:
    """
    Constructs the path to a template file.
    """
    path = BASE_TEMPLATE_DIR / style / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path


def render_template(path: Path, ctx: Dict[str, Any]) -> str:
    """
    Renders a Jinja2 template with the given context.
    """
    relative = path.relative_to(BASE_TEMPLATE_DIR)
    template = _env.get_template(str(relative))
    return template.render(**ctx)
