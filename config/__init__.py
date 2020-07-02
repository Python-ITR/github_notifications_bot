import yaml
import os
from typing import List, Optional

YAML_PATH = "./config.yml"


def parse_repositories_string(s: Optional[str]) -> List[str]:
    if not s:
        return []
    return list(map(lambda s: s.strip(), s.split(",")))


def parse_extensions_string(s: str) -> List[str]:
    return list(map(lambda s: s.strip(), s.split(",")))


class Config:
    repositories: List["str"]
    file_extensions: List["str"]
    token: Optional[str]

    def __init__(self, yaml_path: str = YAML_PATH):
        yaml_config = None
        with open(yaml_path) as f:
            yaml_config = yaml.safe_load(f)
        self.repositories = (
            parse_repositories_string(os.environ.get("GN_REPOSITORIES"))
            if "GN_REPOSITORIES" in os.environ
            else yaml_config.get("repositories")
        )
        self.file_extensions = (
            parse_repositories_string(os.environ.get("GN_FILE_EXTENSIONS"))
            if "GN_FILE_EXTENSIONS" in os.environ
            else yaml_config.get("file_extensions")
        )
        self.token = (
            os.environ.get("GN_TOKEN")
            if "GN_TOKEN" in os.environ
            else yaml_config.get("token")
        )
