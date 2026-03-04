import pytest
from scallfold.utils.templating import get_template_path, render_template
from pathlib import Path


def test_get_template_path_exists():
    """Test getting path to existing template."""
    path = get_template_path("clean", "main.py.j2")
    assert path.exists()
    assert path.name == "main.py.j2"


def test_get_template_path_not_exists():
    """Test error for non-existing template."""
    with pytest.raises(FileNotFoundError):
        get_template_path("clean", "nonexistent.j2")


def test_render_template():
    """Test template rendering with a real template file."""
    path = get_template_path("clean", "main.py.j2")
    ctx = {"project_name": "testapp", "version": "0.1.0", "description": "test"}
    result = render_template(path, ctx)
    assert "FastAPI" in result