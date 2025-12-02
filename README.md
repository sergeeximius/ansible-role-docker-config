# ansible-role-docker-config

Ansible role for managing Docker daemon configuration (`/etc/docker/daemon.json`).
Supports registry mirrors, DNS servers, and IPv6 settings.

## Requirements

- Ansible >= 2.12
- Target system with `/etc/docker` directory (created automatically if Docker is installed)

## Role Variables

| Name                    | Default                                            | Description                                                     |
| ----------------------- | -------------------------------------------------- | --------------------------------------------------------------- |
| `docker_config_mirror`  | `{registry: "https://dockerhub.timeweb.cloud"}`    | Docker registry mirror configuration (dict with `registry` key) |
| `docker_config_dns`     | `["77.88.8.8", "77.88.8.1", "8.8.8.8", "1.1.1.1"]` | List of DNS servers for Docker containers                       |
| `docker_config_ipv6`    | `false`                                            | Enable or disable IPv6 in Docker                                |
| `docker_config_restart` | `true`                                             | Restart Docker service after config change                      |

### Example Configuration

```yaml
docker_config_mirror:
  registry: "https://dockerhub.timeweb.cloud"
docker_config_dns:
  - "77.88.8.8"
  - "77.88.8.1"
  - "8.8.8.8"
  - "1.1.1.1"
docker_config_ipv6: false
docker_config_restart: true
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
      vars:
        docker_config_mirror:
          registry: "https://dockerhub.timeweb.cloud"
        docker_config_dns:
          - "77.88.8.8"
          - "77.88.8.1"
        docker_config_ipv6: false
        docker_config_restart: true
```

### Advanced Example with Custom DNS and IPv6

```yaml
---
- name: Configure Docker daemon with full customization
  hosts: docker_hosts
  become: true
  roles:
    - role: ansible-role-docker-config
      vars:
        docker_config_mirror:
          registry: "https://mirror.example.com"
        docker_config_dns:
          - "8.8.8.8"
          - "8.8.4.4"
          - "1.1.1.1"
        docker_config_ipv6: true # Enable IPv6 if needed
        docker_config_restart: true
```

### Minimal Example (Using Defaults)

```yaml
---
- name: Configure Docker with defaults
  hosts: docker_hosts
  become: true
  roles:
    - role: ansible-role-docker-config
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
