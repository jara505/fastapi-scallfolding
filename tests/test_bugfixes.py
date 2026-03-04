import copy
import re
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from scallfold.project.structure import STRUCTURES
from scallfold.project.generator import create_project
from scallfold.cli import _validate_project_name
from scallfold.utils.prompts import PROJECT_NAME_PATTERN


class TestShallowCopyBug:
    """Bug 1: STRUCTURES must not be mutated after create_project calls."""

    def test_structures_not_mutated_after_db_project(self):
        original_templates = copy.deepcopy(STRUCTURES["structured"]["templates"])

        meta = {
            "project_name": "proj_a",
            "style": "structured",
            "use_db": True,
            "use_orm": True,
            "include_tests": True,
            "description": "",
            "version": "0.1.0",
        }

        with TemporaryDirectory() as tmp:
            create_project(meta, root_path=Path(tmp))

        assert STRUCTURES["structured"]["templates"] == original_templates

    def test_structures_not_mutated_after_no_tests(self):
        original_templates = copy.deepcopy(STRUCTURES["clean"]["templates"])

        meta = {
            "project_name": "proj_b",
            "style": "clean",
            "use_db": False,
            "use_orm": False,
            "include_tests": False,
            "description": "",
            "version": "0.1.0",
        }

        with TemporaryDirectory() as tmp:
            create_project(meta, root_path=Path(tmp))

        assert STRUCTURES["clean"]["templates"] == original_templates

    def test_consecutive_projects_independent(self):
        """Two consecutive structured+db projects should both succeed."""
        meta = {
            "project_name": "proj_first",
            "style": "structured",
            "use_db": True,
            "use_orm": False,
            "include_tests": True,
            "description": "",
            "version": "0.1.0",
        }

        with TemporaryDirectory() as tmp:
            create_project(meta, root_path=Path(tmp))

        meta["project_name"] = "proj_second"

        with TemporaryDirectory() as tmp:
            create_project(meta, root_path=Path(tmp))
            assert (Path(tmp) / "proj_second" / "src" / "proj_second" / "core" / "database.py").exists()


class TestNameValidationConsistency:
    """Bug 2: CLI and prompts must use the same validation pattern."""

    def test_hyphenated_name_valid_in_cli(self):
        result = _validate_project_name("my-project")
        assert result == "my-project"

    def test_hyphenated_name_valid_in_pattern(self):
        assert re.match(PROJECT_NAME_PATTERN, "my-project") is not None

    def test_invalid_name_sanitized_consistently(self):
        result = _validate_project_name("invalid name!")
        assert re.match(PROJECT_NAME_PATTERN, result) is not None

    def test_name_starting_with_digit_sanitized(self):
        result = _validate_project_name("123abc")
        assert result.startswith("_")
        assert re.match(PROJECT_NAME_PATTERN, result) is not None

    def test_valid_names_pass_both(self):
        valid_names = ["valid_name", "ValidName", "_private", "my-app"]
        for name in valid_names:
            assert _validate_project_name(name) == name
            assert re.match(PROJECT_NAME_PATTERN, name) is not None

    def test_none_returns_none(self):
        assert _validate_project_name(None) is None


class TestRedundantVersionCheck:
    """Bug 3: check_python_version should not be called inside create_project."""

    def test_generator_does_not_call_check_python_version(self):
        """Verify create_project does not import or call check_python_version."""
        import inspect
        source = inspect.getsource(create_project)
        assert "check_python_version" not in source


class TestReadmeCodeFence:
    """Bug 4: Clean README.md.j2 must have a properly closed code fence."""

    def test_clean_readme_has_closed_code_fence(self):
        template_path = (
            Path(__file__).resolve().parent.parent
            / "scallfold" / "templates" / "clean" / "README.md.j2"
        )
        content = template_path.read_text()
        open_fences = content.count("```")
        assert open_fences % 2 == 0, "Code fences are not properly closed"

    def test_clean_project_readme_renders_valid_markdown(self):
        meta = {
            "project_name": "test_readme",
            "style": "clean",
            "use_db": False,
            "use_orm": False,
            "include_tests": False,
            "description": "A test project",
            "version": "0.1.0",
        }

        with TemporaryDirectory() as tmp:
            create_project(meta, root_path=Path(tmp))
            readme = (Path(tmp) / "test_readme" / "README.md").read_text()
            assert readme.count("```") % 2 == 0
