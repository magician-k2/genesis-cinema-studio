import os
import json
from pathlib import Path
from .gemini_hub import gemini_hub
from .vault_service import vault_service

class CinemaRouter:
    @staticmethod
    def list_projects(vault_path: str) -> list:
        return vault_service.read_json(vault_path, default=[])

    @staticmethod
    def save_project(vault_path: str, project_data: dict) -> list:
        projects = vault_service.read_json(vault_path, default=[])
        pid = project_data.get("id")
        existing_idx = next((i for i, p in enumerate(projects) if p.get("id") == pid), -1)
        if existing_idx >= 0:
            projects[existing_idx] = project_data
        else:
            projects.insert(0, project_data)
        vault_service.write_json(vault_path, projects)
        return projects
