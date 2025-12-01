from pathlib import Path
from typing import Dict, Any

from scallfold.compatibility import check_python_version
from scallfold.project.structure import STRUCTURES
from scallfold.utils.filesystem import ensure_empty_directory
from scallfold.utils.templating import get_template_path, render_template


def create_project(meta: Dict[str, Any]):
    """
    Generates a project structure based on metadata and a declarative structure map.
    """
    style = meta["style"]
    project_name = meta["project_name"]
    root = Path(project_name)

    ensure_empty_directory(root)

    base_structure = STRUCTURES.get(style)
    if not base_structure:
        raise ValueError(f"Unknown project style: {style}")

    # Make a copy to modify in-place
    structure = base_structure.copy()

    # If not including tests, remove test-related entries
    if not meta.get("include_tests"):
        if "tests" in structure.get("dirs", []):
            structure["dirs"] = [d for d in structure["dirs"] if d != "tests"]
        if "test_basic.py.j2" in structure.get("templates", {}):
            # Create a copy of the templates dict to modify it
            structure["templates"] = structure["templates"].copy()
            del structure["templates"]["test_basic.py.j2"]

    # Create directories
    for dir_path in structure.get("dirs", []):
        path = root / dir_path.format(**meta)
        path.mkdir(parents=True, exist_ok=True)

    # Render templates
    for template_name, output_path in structure.get("templates", {}).items():
        template_path = get_template_path(style, template_name)
        final_path = root / output_path.format(**meta)
        final_path.write_text(render_template(template_path, meta))

    # Copy static files
    for file_name, output_path in structure.get("files", {}).items():
        static_file_path = get_template_path(style, file_name)
        final_path = root / output_path.format(**meta)
        final_path.write_text(static_file_path.read_text())

    # Create empty __init__.py files
    for init_path in structure.get("init_files", []):
        path = root / init_path.format(**meta)
        path.touch()

    check_python_version()

    print(f"Project '{project_name}' created successfully at: {root.resolve()}")
