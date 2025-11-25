# ansible-role-docker-config

Ansible role for managing Docker daemon configuration (`/etc/docker/daemon.json`).

## Requirements

- Ansible >= 2.12
- Target system with `/etc/docker` directory (created automatically if Docker is installed)

## Role Variables

| Name                                | Default                   | Description                                                       |
| ----------------------------------- | ------------------------- | ----------------------------------------------------------------- |
| `docker_config_enabled`             | `true`                    | Enable/disable role execution                                     |
| `docker_config_restart`             | `true`                    | Restart Docker service after config change                        |
| `docker_config_daemon_json_path`    | `/etc/docker/daemon.json` | Path to daemon configuration file                                 |
| `docker_config_mirror`              | `{}`                      | Docker registry mirror configuration (dict with `registry` key)   |
| `docker_config_daemon_json_mirrors` | `[]`                      | List of registry mirrors (deprecated, use `docker_config_mirror`) |

### Example Configuration

```yaml
# Modern approach (recommended)
docker_config_mirror:
  registry: "https://dockerhub.timeweb.cloud"

# Legacy approach (still supported)
docker_config_daemon_json_mirrors:
  - "https://dockerhub.timeweb.cloud"
```

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Configure Docker daemon
  hosts: docker_hosts
  become: true
  roles:
    - role: ansible-role-docker-config
      docker_config_mirror:
        registry: "https://dockerhub.timeweb.cloud"
      docker_config_restart: true
```

### Advanced Example

```yaml
---
- name: Configure Docker daemon with custom settings
  hosts: docker_hosts
  become: true
  roles:
    - role: ansible-role-docker-config
      docker_config_mirror:
        registry: "https://mirror.example.com"
      docker_config_restart: false # Disable restart if manual control needed
```

## Testing

### Prerequisites

- Docker installed and running on your system
- Python 3.9+ (tested with 3.13)

### Quick Start

```bash
# Install tox (if not installed)
pip install tox

# Run full test suite in isolated environment (recommended)
tox

# Run tests for specific Python version
tox -e py313

# Run only linting
tox -e lint
```

### Alternative: Direct Molecule Testing

```bash
# Create isolated virtual environment
python -m venv .venv-molecule
source .venv-molecule/bin/activate  # On macOS/Linux
# or
.venv-molecule\Scripts\activate  # On Windows

# Install dependencies
pip install 'molecule[docker]>=6.0' 'pytest-testinfra>=10.0' 'ansible-core>=2.12'

# Run full test cycle
molecule test

# Run individual steps
molecule converge  # Apply role
molecule verify    # Run tests only
molecule destroy   # Clean up
```

### Test Structure

The role includes 4 test cases validating:

1. `/etc/docker/daemon.json` file existence
2. Valid JSON structure
3. Presence of `registry-mirrors` key
4. Correct mirror URL configuration

### Important Notes

- **Environment Isolation**: This role uses `pytest-testinfra` for testing, which conflicts with `pytest-ansible` plugin on the `--connection` argument. The `tox.ini` configuration creates an isolated environment without `pytest-ansible` to avoid this conflict.
- **Test Approach**: Tests create a Docker container (Ubuntu 24.04 with Ansible pre-installed) and validate daemon.json configuration. No actual Docker daemon is started in the container.
- **Idempotency**: Tests verify that role execution is idempotent (second run produces no changes).

## License

MIT

## Author Information

Sergey Sedov
