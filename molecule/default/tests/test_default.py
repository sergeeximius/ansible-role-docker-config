import json
import os

import pytest

# Use Molecule managed hosts
testinfra_hosts = [
    f"ansible://instance?ansible_inventory={os.environ['MOLECULE_INVENTORY_FILE']}"
]


def test_daemon_json_exists(host):
    """Test that daemon.json exists and is a valid file."""
    daemon_json = host.file("/etc/docker/daemon.json")
    assert daemon_json.exists, "/etc/docker/daemon.json does not exist"
    assert daemon_json.is_file, "/etc/docker/daemon.json is not a file"


def test_daemon_json_valid(host):
    """Test that daemon.json contains valid JSON."""
    daemon_json = host.file("/etc/docker/daemon.json")
    try:
        data = json.loads(daemon_json.content_string)
    except json.JSONDecodeError as e:
        pytest.fail(f"daemon.json is not valid JSON: {e}")

    assert isinstance(data, dict), "daemon.json should be a JSON object"


def test_registry_mirrors_key(host):
    """Test that registry-mirrors key is present."""
    daemon_json = host.file("/etc/docker/daemon.json")
    data = json.loads(daemon_json.content_string)
    assert "registry-mirrors" in data, "registry-mirrors key not found in daemon.json"


def test_mirror_present(host):
    """Test that at least one expected mirror is configured."""
    daemon_json = host.file("/etc/docker/daemon.json")
    data = json.loads(daemon_json.content_string)
    mirrors = data.get("registry-mirrors", [])

    assert isinstance(mirrors, list), "registry-mirrors should be a list"
    assert len(mirrors) > 0, "registry-mirrors list is empty"
    assert any(
        "timeweb" in m or "dockerhub" in m for m in mirrors
    ), f"Expected mirror not found. Found: {mirrors}"
