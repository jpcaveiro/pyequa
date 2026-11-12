import os
import warnings

import pytest

os.environ.setdefault("PYEQUA_PROJECT_ROOT", ".")

from pyequa import config as cfg
from pyequa import clozecloud


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.setattr(cfg, "PYEQUA_PROJECT_ROOT", str(tmp_path))
    (tmp_path / "ex").mkdir()
    return tmp_path


def test_layers_closest_wins(project):
    (project / "project.yaml").write_text("author: proj\nglobal_tolerance: 0.5\n")
    (project / "ex" / "exercise.yaml").write_text("global_tolerance: 0.1\n")
    c = cfg.Config("ex").config
    assert c["author"] == "proj"
    assert c["global_tolerance"] == 0.1
    assert c["problem_word"] == "Problem"  # pyequa default


def test_legacy_config_warns(project):
    (project / "ex" / "config.yaml").write_text("author: old\n")
    with pytest.warns(DeprecationWarning):
        c = cfg.Config("ex").config
    assert c["author"] == "old"


def test_find_project_root_walks_up(project):
    (project / "project.yaml").write_text("{}\n")
    assert cfg.find_project_root(project / "ex") == project.resolve()


def test_push_failure_only_warns(project, monkeypatch):
    xml = project / "ex" / "a.xml"
    xml.write_text("<quiz/>")
    conf = {"clozecloud": {"url": "http://127.0.0.1:9", "user_tag": "u", "token_env": "TOK"}}
    monkeypatch.setenv("TOK", "secret")
    with pytest.warns(UserWarning, match="push failed"):
        assert clozecloud.push(xml, conf, project / "ex", project, timeout=1) is False


def test_push_missing_settings_warns(project):
    with pytest.warns(UserWarning):
        assert clozecloud.push(project / "x.xml", {}, project / "ex", project) is False


def test_remote_path_posix(project):
    assert clozecloud.remote_path(project / "ex", project) == "ex"
