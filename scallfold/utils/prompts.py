from typing import Dict
from InquirerPy import inquirer


def collect_project_meta() -> Dict[str, str]:
    name = inquirer.text(message="Project name:",
                         validate=lambda s: len(s.strip()) > 0).execute()
    
    style = inquirer.select(message="Project type:",
                            choices=["clean", "structured"]).execute()
    
    include_tests = inquirer.confirm(message="Include tests?", default=False).execute()
    
    description = inquirer.text(message="Description (optional):", default="").execute()
    
    version = inquirer.text(message="Version: ", default="0.1.0").execute()
    
    use_db = False
    use_orm = False
    if style != "clean":
        use_db = inquirer.confirm(message="Include database?: ", default=False).execute()
        use_orm = inquirer.confirm(message="Include ORM?: ", default=False).execute()
    
    return {
        "project_name": name,
        "style": style,
        "use_db": use_db,
        "use_orm": use_orm,
        "include_tests": include_tests,
        "description": description,
        "version": version,
    }
