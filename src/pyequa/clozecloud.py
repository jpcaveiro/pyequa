"""Push generated Moodle XML to a clozecloud server.

Settings live under the ``clozecloud`` key of ``project.yaml``::

    clozecloud:
      url: https://clozecloud.example.org
      user_tag: jpcaveiro
      token_env: CLOZECLOUD_TOKEN   # name of the env var holding the API token

The token itself must never be committed. Failures only warn.
"""

import os
import urllib.parse
import urllib.request
import warnings
from pathlib import Path


def remote_path(exercise_folder, project_root):
    """Exercise folder relative to the project root, with forward slashes."""
    rel = Path(exercise_folder).resolve().relative_to(Path(project_root).resolve())
    return rel.as_posix()


def push(xml_path, config, exercise_folder, project_root, timeout=30):
    """PUT ``xml_path`` to ``{url}/users/{tag}/exercises/{path}``.

    Returns:
        True on success, False if skipped or failed (a warning is issued).
    """
    try:
        settings = config.get('clozecloud') or {}
        url = settings.get('url')
        tag = settings.get('user_tag')
        token_env = settings.get('token_env')
        if not (url and tag and token_env):
            warnings.warn("clozecloud: 'url', 'user_tag' and 'token_env' must be set in "
                          "project.yaml; nothing pushed.")
            return False
        token = os.getenv(token_env)
        if not token:
            warnings.warn(f"clozecloud: environment variable '{token_env}' is empty or unset; "
                          "nothing pushed.")
            return False

        xml_path = Path(xml_path)
        if not xml_path.is_file():
            warnings.warn(f"clozecloud: '{xml_path}' does not exist; nothing pushed.")
            return False

        path = urllib.parse.quote(remote_path(exercise_folder, project_root))
        endpoint = f"{url.rstrip('/')}/users/{urllib.parse.quote(str(tag))}/exercises/{path}"
        request = urllib.request.Request(
            endpoint,
            data=xml_path.read_bytes(),
            method="PUT",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/xml"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            print(f"clozecloud: pushed to {endpoint} (HTTP {response.status}).")
        return True
    except Exception as err:
        warnings.warn(f"clozecloud: push failed: {err}")
        return False
