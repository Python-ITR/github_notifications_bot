from config import Config


def test_config_values():
    config = Config(yaml_path="./tests/test_config.yaml")
    assert config.repositories == ["VLZH/course-python-basics"]
    assert config.file_extensions == [".mdx", ".md"]
    assert config.token == "1234512345"


def test_config_values_without_token():
    config = Config(yaml_path="./tests/test_config_without_token.yaml")
    assert config.token is None


def test_config_values_from_environ(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv("GN_REPOSITORIES", "VLZH/course-python-basics,VLZH/some_repo")
        m.setenv("GN_FILE_EXTENSIONS", ".md")
        m.setenv("GN_TOKEN", "123456789")
        config = Config(yaml_path="./tests/test_config.yaml")
        assert config.repositories == ["VLZH/course-python-basics", "VLZH/some_repo"]
        assert config.file_extensions == [".md"]
        assert config.token == "123456789"
