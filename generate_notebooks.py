"""
Notebook generator for:
    Python for CloudOps + DevOps + DevSecOps + Monitoring

Run: python generate_notebooks.py

Sources cited inline from official docs:
  - Python subprocess: https://docs.python.org/3/library/subprocess.html
  - Python pathlib:    https://docs.python.org/3/library/pathlib.html
  - boto3 quickstart:  https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html
  - boto3 paginators:  https://docs.aws.amazon.com/boto3/latest/guide/paginators.html
  - Prometheus client: https://github.com/prometheus/client_python
  - Grafana API:       https://grafana.com/docs/grafana/latest/developers/http_api/
  - OpenTelemetry:     https://opentelemetry-python.readthedocs.io/
  - Bandit:            https://bandit.readthedocs.io/
  - Click:             https://click.palletsprojects.com/
  - structlog:         https://www.structlog.org/
"""

import nbformat
from pathlib import Path

BASE = Path(r"c:\Users\eaklamav\Documents\github_repo\AIOps\Tutorials\python-for-devops\study-plan\topic-python-cloudops-devops-devsecops-monitoring")


# ─── helpers ────────────────────────────────────────────────────────────────

def md(src: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_markdown_cell(src)

def code(src: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_code_cell(src)

def notebook(cells: list) -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    nb.cells = cells
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"}
    }
    return nb

def save(nb: nbformat.NotebookNode, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"  wrote {path.relative_to(BASE)}")


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 1 — Python Automation Foundations
# ═══════════════════════════════════════════════════════════════════════════

def lesson_1_1():
    """DevOps Environment Setup"""
    cells = [
        md("""# Lesson 1.1 — DevOps Environment Setup

**Level: Beginner**

## Learning Objectives
- Create and activate Python virtual environments
- Understand the recommended project layout for ops automation scripts
- Manage dependencies with `pip`, `requirements.txt`, and `pyproject.toml`
- Verify your environment is ready for the course

**Produces:** `ops-platform/` project skeleton with all dependencies installed."""),

        md("""## Concepts

### Why Virtual Environments?

A **virtual environment** gives every project its own isolated Python interpreter and package set.
Without it, installing `boto3==1.30` for one project can silently break another that needs `boto3==1.26`.

```
project-a/.venv/  ← boto3==1.30, requests==2.31
project-b/.venv/  ← boto3==1.26, requests==2.28   (no conflict)
```

Create and activate with:
```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\\Scripts\\activate           # Windows
```

### Recommended Project Layout
```
ops-platform/
├── .venv/                  # virtual environment (never commit)
├── src/ops_platform/       # source code
│   ├── __init__.py
│   ├── cloud/              # AWS / Azure / GCP modules
│   ├── security/           # DevSecOps modules
│   ├── monitoring/         # Prometheus / OTel / alerting
│   └── cli.py              # Click CLI entry point
├── tests/
├── configs/
├── .env                    # secrets (NEVER commit)
├── .env.example            # safe template (commit this)
├── requirements.txt        # pinned production deps
└── pyproject.toml          # package metadata & entry points
```

*Reference: [Python Packaging User Guide](https://packaging.python.org/)*"""),

        code("""# Step 1 — verify Python version and virtual-environment status
import sys, subprocess

print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")

result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                        capture_output=True, text=True)
print(f"pip: {result.stdout.strip()}")

in_venv = sys.prefix != sys.base_prefix
print(f"\\nRunning inside venv: {in_venv}")
if not in_venv:
    print("  ⚠  Recommendation: activate a virtual environment first.")
    print("     python -m venv .venv && source .venv/bin/activate  (Linux/macOS)")
    print("     python -m venv .venv && .venv\\\\Scripts\\\\activate   (Windows)")
else:
    print(f"  ✓  venv path: {sys.prefix}")"""),

        md("## Code-Along: Step 1 — Scaffold the Project"),

        code("""from pathlib import Path

root = Path("ops-platform")

dirs = [
    root / "src" / "ops_platform" / "cloud",
    root / "src" / "ops_platform" / "security",
    root / "src" / "ops_platform" / "monitoring",
    root / "tests",
    root / "configs",
]
for d in dirs:
    d.mkdir(parents=True, exist_ok=True)
    (d / "__init__.py").touch()          # marks as Python package
    print(f"  created {d}")

print("\\n✓ Directory tree created.")"""),

        md("## Code-Along: Step 2 — Create Bootstrap Files"),

        code("""# .env.example — safe template (commit this, never .env itself)
(root / ".env.example").write_text(
    "# Copy to .env and fill in real values.  NEVER commit .env\\n"
    "AWS_ACCESS_KEY_ID=\\n"
    "AWS_SECRET_ACCESS_KEY=\\n"
    "AWS_DEFAULT_REGION=us-east-1\\n"
    "SLACK_WEBHOOK_URL=\\n"
    "LOG_LEVEL=INFO\\n"
)

# requirements.txt
(root / "requirements.txt").write_text(
    "boto3>=1.28.0\\n"
    "python-dotenv>=1.0.0\\n"
    "pyyaml>=6.0.1\\n"
    "click>=8.1.7\\n"
    "rich>=13.7.0\\n"
    "structlog>=24.1.0\\n"
    "prometheus_client>=0.19.0\\n"
    "requests>=2.31.0\\n"
)

# .gitignore
(root / ".gitignore").write_text(
    ".venv/\\n__pycache__/\\n*.pyc\\n.env\\ndist/\\nbuild/\\n"
)

print("✓ Bootstrap files written:")
for f in sorted(root.rglob("*")):
    if f.is_file():
        print(f"  {f}")"""),

        md("## Code-Along: Step 3 — Install & Verify Dependencies"),

        code("""import subprocess, sys, importlib

subprocess.run(
    [sys.executable, "-m", "pip", "install",
     "boto3", "python-dotenv", "pyyaml", "click", "rich", "structlog",
     "prometheus_client", "requests", "--quiet"],
    capture_output=True
)

packages = [
    ("boto3",             "AWS SDK"),
    ("dotenv",            "python-dotenv"),
    ("yaml",              "PyYAML"),
    ("click",             "Click CLI"),
    ("rich",              "Rich terminal output"),
    ("structlog",         "Structured logging"),
    ("prometheus_client", "Prometheus client"),
    ("requests",          "HTTP library"),
]

print("Dependency verification:")
all_ok = True
for pkg, desc in packages:
    try:
        mod = importlib.import_module(pkg)
        ver = getattr(mod, "__version__", "installed")
        print(f"  ✓  {desc:<28} {ver}")
    except ImportError:
        print(f"  ✗  {desc}: NOT INSTALLED")
        all_ok = False

print("\\n✓ All dependencies ready." if all_ok else "\\n✗ Some packages missing.")"""),

        md("""## Exercise

Extend the scaffold with a `monitoring/` sub-module.

**Your task:**
1. Create `ops-platform/src/ops_platform/monitoring/`
2. Add `__init__.py` with docstring `\"\"\"Monitoring and observability.\"\"\"`
3. Add `prometheus_client>=0.19.0` to `requirements.txt`
4. Print the contents of `requirements.txt` to verify"""),

        code("""# TODO: create the monitoring directory
# TODO: write __init__.py
# TODO: append prometheus_client to requirements.txt
# TODO: print requirements.txt
"""),

        md("""## Key Takeaways
- Always use virtual environments — prevents dependency conflicts between projects
- `.env` for secrets, `.env.example` as the committed template
- `requirements.txt` is the standard for reproducible installs in ops scripts
- Structure source code under `src/` to avoid import shadowing

---
**Next:** [Lesson 1.2 — OS & Process Automation](lesson-1.2-os-process-automation.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-1-python-automation-foundations" / "lesson-1.1-devops-environment-setup.ipynb")


def lesson_1_2():
    """OS & Process Automation"""
    cells = [
        md("""# Lesson 1.2 — OS & Process Automation

**Level: Beginner**

## Learning Objectives
- Run shell commands safely with `subprocess.run()` and capture output
- Read and set environment variables via `os.environ`
- Navigate file paths with `pathlib.Path` (cross-platform)
- Copy, move, and inspect files with `shutil`
- Write a system health-check script

**Produces:** `system_health.py` — a reusable health-check script.

*Official refs:*
- *[subprocess — Subprocess management](https://docs.python.org/3/library/subprocess.html)*
- *[pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)*"""),

        md("""## Concepts

### `subprocess.run()` — the Right Way to Run Commands

The `subprocess` module is Python's gateway to the OS shell.  
Always prefer `subprocess.run()` over `os.system()` — it gives you full control
over stdin/stdout/stderr and lets you inspect the return code.

```python
# Official example (subprocess docs):
import subprocess
result = subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
# → CompletedProcess(args=['ls', ...], returncode=0, stdout=b'...', stderr=b'')
```

Key parameters from the [official docs](https://docs.python.org/3/library/subprocess.html#subprocess.run):

| Parameter | Effect |
|-----------|--------|
| `capture_output=True` | Sets `stdout=PIPE, stderr=PIPE` |
| `text=True` | Decodes bytes → str automatically |
| `check=True` | Raises `CalledProcessError` on non-zero exit |
| `timeout=30` | Kills the process after 30 s |

### `pathlib.Path` — Cross-Platform File Paths

From the [pathlib docs](https://docs.python.org/3/library/pathlib.html):

> *"Path classes are divided between pure paths, which provide purely
> computational operations without I/O, and concrete paths, which also
> provide I/O operations."*

The `/` operator builds paths:
```python
from pathlib import Path
p = Path('/etc') / 'init.d' / 'reboot'   # PosixPath('/etc/init.d/reboot')
```

**Security note (subprocess docs):** Using `shell=True` exposes your script to
shell injection. Always pass commands as a **list**, never a formatted string with
user input."""),

        code("""import subprocess, sys, os, shutil, platform
from pathlib import Path

print(f"Platform : {sys.platform}")
print(f"Python   : {sys.version.split()[0]}")
print(f"cwd      : {Path.cwd()}")"""),

        md("## Code-Along: Step 1 — Safe Command Execution"),

        code("""def run_command(cmd: list[str], timeout: int = 30) -> dict:
    \"\"\"Run a shell command and return a structured result dict.

    Based on subprocess.run() — see:
    https://docs.python.org/3/library/subprocess.html#subprocess.run

    Args:
        cmd: Command as a list, e.g. ['git', 'status']
             NEVER pass a single string with shell=True unless you trust
             the entire string (subprocess security note).
        timeout: Seconds before killing the process.

    Returns:
        {'success': bool, 'stdout': str, 'stderr': str, 'returncode': int}
    \"\"\"
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,   # captures both stdout and stderr
            text=True,             # decodes bytes to str
            timeout=timeout,
        )
        return {
            "success":    result.returncode == 0,
            "stdout":     result.stdout.strip(),
            "stderr":     result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Timed out", "returncode": -1}
    except FileNotFoundError as e:
        return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}

# Verify Python version via subprocess
r = run_command([sys.executable, "--version"])
print(f"success  : {r['success']}")
print(f"output   : {r['stdout']}")
print(f"returncode: {r['returncode']}")"""),

        md("## Code-Along: Step 2 — Environment Variables"),

        code("""# os.environ behaves like a dict (PEP 3137)
# Reference: https://docs.python.org/3/library/os.html#os.environ

def require_env(name: str) -> str:
    \"\"\"Return an env var or raise EnvironmentError if missing.\"\"\"
    val = os.environ.get(name)
    if val is None:
        raise EnvironmentError(
            f"Required env var '{name}' is not set. "
            "Check your .env file or CI/CD secrets configuration."
        )
    return val

def optional_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)

# Read common DevOps env vars
region = optional_env("AWS_DEFAULT_REGION", "us-east-1")
log_level = optional_env("LOG_LEVEL", "INFO")
env_name  = optional_env("ENVIRONMENT", "development")

print(f"AWS Region  : {region}")
print(f"Log Level   : {log_level}")
print(f"Environment : {env_name}")

# Set a var for this process only
os.environ["DEMO_VAR"] = "ops-bot"
print(f"\\nDEMO_VAR set to: {os.environ['DEMO_VAR']}")"""),

        md("""## Code-Along: Step 3 — pathlib and shutil

From the [pathlib docs](https://docs.python.org/3/library/pathlib.html#basic-use):

```python
from pathlib import Path

p = Path('.')
[x for x in p.iterdir() if x.is_dir()]   # list subdirectories
list(p.glob('**/*.py'))                   # recursive glob
```
"""),

        code("""import tempfile

with tempfile.TemporaryDirectory() as tmp:
    workspace = Path(tmp)

    # Build a directory tree
    (workspace / "configs" / "dev").mkdir(parents=True)
    (workspace / "configs" / "prod").mkdir(parents=True)
    (workspace / "logs").mkdir()

    # Write files
    dev_cfg  = workspace / "configs" / "dev"  / "app.yaml"
    prod_cfg = workspace / "configs" / "prod" / "app.yaml"
    dev_cfg.write_text("environment: development\\nlog_level: DEBUG\\nreplicas: 1\\n")
    prod_cfg.write_text("environment: production\\nlog_level: WARNING\\nreplicas: 3\\n")

    # Recursive listing (pathlib.rglob)
    print("Workspace tree:")
    for f in sorted(workspace.rglob("*")):
        rel = f.relative_to(workspace)
        indent = "  " * (len(rel.parts) - 1)
        icon = "📁" if f.is_dir() else "📄"
        print(f"  {indent}{icon} {rel.name}")

    # Read + stat
    content = dev_cfg.read_text()
    print(f"\\ndev config ({dev_cfg.stat().st_size} bytes):\\n{content}")

    # shutil.copy2 — preserves metadata
    backup = workspace / "configs" / "dev" / "app.yaml.bak"
    shutil.copy2(dev_cfg, backup)
    print(f"Backup created: {backup.name}")"""),

        md("## Code-Along: Step 4 — System Health Check Script"),

        code("""def check_disk(path: str = "/") -> dict:
    \"\"\"Return disk usage for a path using shutil.disk_usage.\"\"\"
    if sys.platform == "win32":
        path = "C:\\\\"
    usage = shutil.disk_usage(path)
    pct = usage.used / usage.total * 100
    return {
        "path": path,
        "total_gb":    round(usage.total / 1024**3, 1),
        "used_gb":     round(usage.used  / 1024**3, 1),
        "free_gb":     round(usage.free  / 1024**3, 1),
        "percent_used": round(pct, 1),
        "healthy":     pct < 80,
    }

def tool_available(name: str) -> bool:
    \"\"\"Return True if a CLI tool exists on PATH.\"\"\"
    which = "where" if sys.platform == "win32" else "which"
    return run_command([which, name])["success"]

disk = check_disk()
print("=== System Health Report ===")
print(f"Host     : {platform.node()}")
print(f"OS       : {platform.system()} {platform.release()}")
print(f"Python   : {platform.python_version()}")
print()
print(f"Disk ({disk['path']}): {disk['used_gb']}GB / {disk['total_gb']}GB "
      f"({disk['percent_used']}%) — {'✓ Healthy' if disk['healthy'] else '⚠ >80% used'}")
print()
print("DevOps tools:")
for tool in ["git", "docker", "kubectl", "helm", "terraform"]:
    icon = "✓" if tool_available(tool) else "✗"
    print(f"  {icon}  {tool}")
print("========================="""),

        md("""## Exercise

Extend the health check to detect open ports.

**Your task:**
1. Write `check_port(host: str, port: int) -> bool` using `socket.create_connection`
2. Check ports 80, 443, and 8080 on `localhost`
3. Print `OPEN` or `CLOSED` for each"""),

        code("""import socket

# TODO: implement check_port(host, port) -> bool
# Hint: use socket.create_connection((host, port), timeout=1) inside try/except

def check_port(host: str, port: int) -> bool:
    pass   # ← your implementation here

# TODO: test it
for port in [80, 443, 8080]:
    status = "OPEN" if check_port("localhost", port) else "CLOSED"
    print(f"  localhost:{port:5}  {status}")
"""),

        md("""## Key Takeaways
- Pass commands as **lists** to `subprocess.run()` — never use `shell=True` with user input ([security note](https://docs.python.org/3/library/subprocess.html#security-considerations))
- `pathlib.Path` works identically on Windows, macOS, and Linux — prefer it over `os.path` string manipulation
- `shutil.disk_usage()` returns a quick disk health check without any external tools
- Health-check scripts like this become building blocks for your Prometheus exporter in Phase 5

---
**Next:** [Lesson 1.3 — Configuration Management](lesson-1.3-configuration-management.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-1-python-automation-foundations" / "lesson-1.2-os-process-automation.ipynb")


def lesson_1_3():
    cells = [
        md("""# Lesson 1.3 — Configuration Management

**Level: Beginner**

## Learning Objectives
- Load environment variables from `.env` files with `python-dotenv`
- Parse and write YAML configuration with `PyYAML`
- Work with JSON configs using Python's built-in `json` module
- Apply the base-config + environment-overlay pattern
- Build a typed `AppConfig` dataclass

**Produces:** `config_loader.py` — a multi-environment config loader.

*Official refs:*
- *[python-dotenv](https://saurabh-kumar.com/python-dotenv/)*
- *[PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)*"""),

        md("""## Concepts

### The 12-Factor App Rule for Config

> *"Store config in the environment"* — [12factor.net/config](https://12factor.net/config)

This means:
- **Secrets** → `.env` files (or a secret manager — covered in Phase 4)
- **Structured non-secret config** → YAML/JSON files
- **Never** hardcode environment-specific values (database URLs, API endpoints) in code

### Config Priority Stack (higher overrides lower)

```
Hardcoded defaults
    ↓
Base config YAML       (configs/base.yaml)
    ↓
Env-specific YAML      (configs/staging.yaml)
    ↓
Environment variables  (.env file or shell)    ← highest priority
```

This pattern is used by Kubernetes (Kustomize base + overlay), Helm (values.yaml + env values), and most frameworks."""),

        code("""import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install",
                "python-dotenv", "pyyaml", "--quiet"], capture_output=True)

import os, json, yaml
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv, dotenv_values

print(f"pyyaml version   : {yaml.__version__}")
print(f"dotenv installed : OK")"""),

        md("## Code-Along: Step 1 — python-dotenv"),

        code("""# Write a sample .env file
env_file = Path("sample.env")
env_file.write_text(
    "# App config\\n"
    "ENVIRONMENT=development\\n"
    "LOG_LEVEL=DEBUG\\n"
    "AWS_DEFAULT_REGION=us-east-1\\n"
    "SLACK_CHANNEL=#ops-alerts\\n"
)

# load_dotenv() reads the file and injects values into os.environ
load_dotenv(env_file, override=True)

print("Loaded from .env:")
for key in ["ENVIRONMENT", "LOG_LEVEL", "AWS_DEFAULT_REGION", "SLACK_CHANNEL"]:
    print(f"  {key:<25} = {os.environ.get(key)}")

# dotenv_values() reads WITHOUT touching os.environ (safe for testing)
vals = dotenv_values(env_file)
print(f"\\ndotenv_values keys: {list(vals.keys())}")
env_file.unlink()"""),

        md("## Code-Along: Step 2 — YAML Configuration"),

        code("""# Base config — shared across all environments
base = {
    "app": {"name": "ops-automation-platform", "version": "1.0.0"},
    "aws": {"region": "us-east-1", "services": ["ec2", "s3", "cloudwatch"]},
    "monitoring": {
        "prometheus_port": 9090,
        "scrape_interval_seconds": 15,
        "thresholds": {"cpu_pct": 80, "disk_pct": 85, "memory_pct": 90},
    },
    "logging": {"level": "INFO", "format": "json"},
}

# Write to disk
cfg_path = Path("config.base.yaml")
with open(cfg_path, "w") as f:
    yaml.dump(base, f, default_flow_style=False, sort_keys=False)

print("Written config.base.yaml:")
print(cfg_path.read_text())
cfg_path.unlink()"""),

        code("""# Environment overlays — only the fields that differ
overlays = {
    "development": {
        "monitoring": {"scrape_interval_seconds": 5},   # faster in dev
        "logging": {"level": "DEBUG"},
    },
    "production": {
        "monitoring": {"scrape_interval_seconds": 30},
        "logging": {"level": "WARNING"},
    },
}

def deep_merge(base: dict, override: dict) -> dict:
    \"\"\"Recursively merge override into base (override wins).\"\"\"
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

env = os.environ.get("ENVIRONMENT", "development")
final = deep_merge(base, overlays.get(env, {}))

print(f"Final config for '{env}':")
print(f"  scrape_interval_seconds : {final['monitoring']['scrape_interval_seconds']}")
print(f"  log level               : {final['logging']['level']}")"""),

        md("## Code-Along: Step 3 — Typed AppConfig with Dataclasses"),

        code("""@dataclass
class AWSConfig:
    region: str = "us-east-1"
    account_id: str = ""

@dataclass
class MonitoringConfig:
    prometheus_port: int = 9090
    scrape_interval_seconds: int = 15
    cpu_threshold: float = 80.0
    disk_threshold: float = 85.0

@dataclass
class AppConfig:
    environment: str = "development"
    log_level: str = "INFO"
    aws: AWSConfig = field(default_factory=AWSConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    slack_webhook_url: str = ""

def load_config() -> AppConfig:
    \"\"\"Load AppConfig from environment variables.\"\"\"
    return AppConfig(
        environment=os.environ.get("ENVIRONMENT", "development"),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
        aws=AWSConfig(
            region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
            account_id=os.environ.get("AWS_ACCOUNT_ID", ""),
        ),
        monitoring=MonitoringConfig(
            prometheus_port=int(os.environ.get("PROMETHEUS_PORT", "9090")),
            scrape_interval_seconds=int(os.environ.get("SCRAPE_INTERVAL", "15")),
        ),
        slack_webhook_url=os.environ.get("SLACK_WEBHOOK_URL", ""),
    )

cfg = load_config()
print("AppConfig:")
print(f"  environment        : {cfg.environment}")
print(f"  log_level          : {cfg.log_level}")
print(f"  aws.region         : {cfg.aws.region}")
print(f"  prometheus_port    : {cfg.monitoring.prometheus_port}")
print(f"  scrape_interval    : {cfg.monitoring.scrape_interval_seconds}s")
print(f"  slack configured   : {'Yes' if cfg.slack_webhook_url else 'No'}")"""),

        md("""## Exercise

Build an environment-aware loader that merges YAML + JSON.

**Your task:**
1. Write a base YAML to `config.base.yaml`  (keys: `app_name`, `replicas`, `log_level`)
2. Write a staging overlay to `config.staging.json` (overrides: `replicas=2`, `log_level=WARNING`)
3. Implement `load_config(env: str) -> dict` that deep-merges them
4. Test with `load_config("staging")`"""),

        code("""# TODO: write config.base.yaml
# TODO: write config.staging.json
# TODO: implement load_config(env) -> dict
def load_config_env(env: str) -> dict:
    pass

result = load_config_env("staging")
print(result)
# Expected: {'app_name': '...', 'replicas': 2, 'log_level': 'WARNING'}
"""),

        md("""## Key Takeaways
- `python-dotenv` injects `.env` into `os.environ` — same interface as CI/CD secrets
- YAML is the DevOps-standard human-readable config format; JSON for machine-generated payloads
- Base-config + overlay pattern is used in Kubernetes (Kustomize), Helm, and Terraform
- Python dataclasses give you typed, IDE-friendly configuration objects

---
**Next:** [Lesson 1.4 — CLI Tools for Ops](lesson-1.4-cli-tools.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-1-python-automation-foundations" / "lesson-1.3-configuration-management.ipynb")


def lesson_1_4():
    cells = [
        md("""# Lesson 1.4 — CLI Tools for Ops

**Level: Beginner**

## Learning Objectives
- Build multi-command CLIs with **Click** (the industry standard for Python CLIs)
- Use **Rich** to produce structured, colorized terminal output
- Add sub-commands, options, arguments, and choices
- Test CLI commands with `click.testing.CliRunner`
- Write a CLI to disk as a standalone script

**Produces:** `ops_cli.py` — a multi-command ops CLI.

*Official refs:*
- *[Click documentation](https://click.palletsprojects.com/en/8.x/)*
- *[Rich documentation](https://rich.readthedocs.io/)*"""),

        md("""## Concepts

### Why Click?

Python's built-in `argparse` is powerful but verbose. **Click** decorators turn
a plain function into a CLI command with zero boilerplate:

```python
@click.command()
@click.option("--name", default="World")
def hello(name):
    click.echo(f"Hello, {name}!")
```

### Click Anatomy

```
@click.group()     → creates a command group  (like: git, docker, kubectl)
@cli.command()     → adds a sub-command       (like: git commit, docker ps)
@click.option()    → named flag               --env staging
@click.argument()  → positional arg           deploy web-api
@click.pass_context→ share state between commands
```

From the [Click quickstart](https://click.palletsprojects.com/en/8.x/quickstart/):

> *"Click tries to make the experience of writing command line tools fun and profitable
> while also preventing any frustration caused by the inability to implement an
> intended CLI API."*"""),

        code("""import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "click", "rich", "--quiet"],
               capture_output=True)

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from click.testing import CliRunner

console = Console()
print(f"click version: {click.__version__}")"""),

        md("## Code-Along: Step 1 — Rich Terminal Output"),

        code("""# Rich produces beautiful terminal output with zero effort
# Reference: https://rich.readthedocs.io/en/stable/

# Colored status messages
console.print("[bold green]✓ Deployment succeeded[/bold green]")
console.print("[bold yellow]⚠ Warning: CPU at 82%[/bold yellow]")
console.print("[bold red]✗ Error: Connection refused[/bold red]")

# Rich Table — perfect for resource inventories
table = Table(title="EC2 Inventory", header_style="bold cyan")
table.add_column("Instance ID", style="dim")
table.add_column("Name")
table.add_column("State")
table.add_column("Type")
table.add_column("Region")

table.add_row("i-0abc1234", "web-server-1", "[green]running[/green]", "t3.micro",  "us-east-1")
table.add_row("i-0def5678", "worker-1",     "[green]running[/green]", "t3.small",  "us-east-1")
table.add_row("i-0ghi9012", "db-backup",    "[yellow]stopped[/yellow]","r6i.large","us-east-1")

console.print(table)

# Rich Panel — for highlighted summaries
console.print(Panel(
    "[bold]3[/bold] instances | [yellow]1 stopped[/yellow] needs attention.",
    title="[bold cyan]Health Summary[/bold cyan]", border_style="cyan"
))"""),

        md("## Code-Along: Step 2 — Click CLI Group with Sub-Commands"),

        code("""@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def ops_cli(ctx, verbose):
    \"\"\"Ops Automation Platform CLI.\"\"\"
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

@ops_cli.command()
@click.option("--env", "-e", default="development",
              type=click.Choice(["development", "staging", "production"]),
              help="Target environment")
@click.pass_context
def status(ctx, env):
    \"\"\"Show deployment status for an environment.\"\"\"
    verbose = ctx.obj.get("verbose", False)
    console.print(f"[bold cyan]Status: {env}[/bold cyan]")
    if verbose:
        console.print("  [dim]Fetching from AWS...[/dim]")
    console.print("  [green]✓ api-server  : running[/green]")
    console.print("  [green]✓ worker      : running[/green]")
    console.print("  [yellow]⚠ cache       : 0/3 ready[/yellow]")

# Test with CliRunner (no real shell needed)
runner = CliRunner()
result = runner.invoke(ops_cli, ["--verbose", "status", "--env", "staging"])
print(result.output)"""),

        code("""@ops_cli.command()
@click.argument("service")                    # positional, required
@click.option("--env",   "-e", default="development",
              type=click.Choice(["development", "staging", "production"]))
@click.option("--tag",   "-t", default="latest", help="Docker image tag")
@click.option("--dry-run",     is_flag=True,  help="Print plan, no changes")
def deploy(service, env, tag, dry_run):
    \"\"\"Deploy a service to the target environment.\"\"\"
    if dry_run:
        console.print(Panel(
            f"DRY RUN: deploy [bold]{service}:{tag}[/bold] → [italic]{env}[/italic]\\n"
            "No changes were made.",
            title="Deploy Plan", border_style="yellow"
        ))
        return
    console.print(f"[green]Deploying {service}:{tag} → {env}[/green]")
    for step in ["Pulling image", "Stopping old containers",
                 "Starting new containers", "Health check"]:
        console.print(f"  [dim]{step}...[/dim]")
    console.print("[bold green]✓ Deployment complete.[/bold green]")

result = runner.invoke(ops_cli,
    ["deploy", "web-api", "--env", "production", "--tag", "v1.2.3", "--dry-run"])
print(result.output)"""),

        md("## Code-Along: Step 3 — Write the CLI as a Standalone Script"),

        code('''%%writefile ops_cli.py
"""Ops Automation Platform CLI.

Usage:
    python ops_cli.py status --env staging
    python ops_cli.py deploy web-api --tag v1.2.3 --dry-run
    python ops_cli.py scan --target src/
"""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

@click.group()
@click.option("--verbose", "-v", is_flag=True)
@click.pass_context
def cli(ctx, verbose):
    """Ops Automation Platform CLI."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

@cli.command()
@click.option("--env", "-e", default="development",
              type=click.Choice(["development", "staging", "production"]))
def status(env):
    """Show deployment status."""
    console.print(f"[bold cyan]Status for: {env}[/bold cyan]")
    table = Table()
    table.add_column("Service")
    table.add_column("Status")
    table.add_row("api-server", "[green]running[/green]")
    table.add_row("worker",     "[green]running[/green]")
    table.add_row("cache",      "[yellow]degraded[/yellow]")
    console.print(table)

@cli.command()
@click.argument("service")
@click.option("--env", "-e", default="development",
              type=click.Choice(["development", "staging", "production"]))
@click.option("--tag", "-t", default="latest")
@click.option("--dry-run", is_flag=True)
def deploy(service, env, tag, dry_run):
    """Deploy a service."""
    if dry_run:
        console.print(Panel(f"DRY RUN: {service}:{tag} → {env}", border_style="yellow"))
        return
    console.print(f"[green]Deploying {service}:{tag} → {env}[/green]")

@cli.command()
@click.argument("service")
@click.option("--lines", "-n", default=50, type=int)
def logs(service, lines):
    """Fetch service logs."""
    console.print(f"Fetching last {lines} lines from '{service}'...")

if __name__ == "__main__":
    cli()
'''),

        code("""# Verify the script works
import subprocess, sys
r = subprocess.run([sys.executable, "ops_cli.py", "--help"],
                   capture_output=True, text=True)
print(r.stdout)"""),

        md("""## Exercise

Add a `scan` sub-command to `ops_cli.py`.

**Your task:**
1. Add `@cli.command()` for `scan`
2. Accept `--target` (default: `.`) and `--port` (default: `80`) options
3. Use `socket.create_connection` to check if the port is open
4. Test it: `runner.invoke(cli, ["scan", "--target", "google.com", "--port", "443"])`"""),

        code("""import socket

# TODO: add @ops_cli.command() for 'scan'
# @ops_cli.command()
# @click.option("--target", default="localhost")
# @click.option("--port", default=80, type=int)
# def scan(target, port):
#     ...

# TODO: test with CliRunner
"""),

        md("""## Key Takeaways
- Click's `@group` + `@command` pattern mirrors how professional CLIs (kubectl, docker, aws) work
- Always use `click.Choice()` to validate enum-like options — gives free `--help` text
- `Rich` tables and panels require zero formatting logic on your part
- Use `CliRunner` to unit-test CLI commands without a real shell or subprocess

---
**Next:** [Lesson 1.5 — Logging & Structured Logging](lesson-1.5-logging-structured.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-1-python-automation-foundations" / "lesson-1.4-cli-tools.ipynb")


def lesson_1_5():
    cells = [
        md("""# Lesson 1.5 — Logging & Structured Logging

**Level: Beginner → Intermediate**

## Learning Objectives
- Configure Python's `logging` module for DevOps scripts
- Use `structlog` to emit JSON-structured log entries
- Bind persistent context (service, env, trace_id) to every log entry
- Understand why structured logging is required by CloudWatch, ELK, and Loki
- Write a reusable `logger.py` module

**Produces:** `logger.py` — a portable structured-logging module.

*Official refs:*
- *[Python logging HOWTO](https://docs.python.org/3/howto/logging.html)*
- *[structlog documentation](https://www.structlog.org/en/stable/)*"""),

        md("""## Concepts

### Why Structured Logging?

**Unstructured log** (human-readable, machine-unfriendly):
```
2025-01-15 10:23 ERROR Failed to connect to database after 3 retries
```

**Structured (JSON) log** (machine-parseable by every log aggregator):
```json
{"timestamp": "2025-01-15T10:23:00Z", "level": "error",
 "event": "db_connection_failed", "retries": 3,
 "service": "api", "env": "production", "trace_id": "abc-123"}
```

With structured logs you can:
- **Filter**: `level=error AND service=api`
- **Aggregate**: count errors per service per hour in CloudWatch Insights
- **Alert**: trigger PagerDuty when `retries > 5`
- **Trace**: correlate logs across services with `trace_id`

### structlog Processor Pipeline

```
log.info("event", key=value)
      ↓
[stdlib.add_log_level]   → adds "level": "info"
[processors.TimeStamper] → adds "timestamp": "2025-..."
[contextvars.merge]      → merges bound context vars
[JSONRenderer]           → serialises to JSON string
      ↓
output
```

*Reference: [structlog docs — processors](https://www.structlog.org/en/stable/processors.html)*"""),

        code("""import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "structlog", "--quiet"],
               capture_output=True)
import structlog, logging
print(f"structlog version: {structlog.__version__}")"""),

        md("## Code-Along: Step 1 — stdlib logging"),

        code("""# Python stdlib logging — foundational knowledge
# Reference: https://docs.python.org/3/howto/logging.html

def configure_stdlib_logging(level: str = "INFO") -> logging.Logger:
    \"\"\"Configure the root logger with a timestamp formatter.\"\"\"
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        handlers=[handler],
        force=True,
    )
    return logging.getLogger("ops")

logger = configure_stdlib_logging("DEBUG")
logger.debug("checking_credentials")
logger.info("inventory_scan_started — region=us-east-1")
logger.warning("rate_limit_approaching — requests_remaining=50")
logger.error("ec2_api_error — region=eu-west-1 — AccessDenied")"""),

        md("## Code-Along: Step 2 — structlog with JSON Output"),

        code("""import os

# Configure structlog once at startup
def configure_structlog(level: str = "INFO", environment: str = "development") -> None:
    \"\"\"Set up structlog processor pipeline.

    Reference: https://www.structlog.org/en/stable/getting-started.html
    \"\"\"
    processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.set_exc_info,  # adds traceback to log on exception
    ]
    # Dev: colored, human-readable.  Production: compact JSON.
    if environment in ("production", "staging", "ci"):
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

os.environ["ENVIRONMENT"] = "development"  # pretty output in the notebook
configure_structlog(environment="development")

log = structlog.get_logger()
log.info("deployment_started", service="web-api", tag="v1.2.3", env="staging")
log.warning("high_cpu", instance_id="i-0abc123", cpu_percent=82.5)
log.error("connection_failed", host="db.internal", port=5432, retries=3)"""),

        md("## Code-Along: Step 3 — Bound Loggers with Persistent Context"),

        code("""import uuid

# Bind service-level context once; it appears in every log entry
service_log = structlog.get_logger().bind(
    service="ops-automation-platform",
    environment="production",
    version="1.0.0",
)

def run_ec2_inventory(region: str, trace_id: str | None = None) -> None:
    \"\"\"Simulate inventory with structured trace-correlated logging.\"\"\"
    op_log = service_log.bind(
        operation="ec2_inventory",
        region=region,
        trace_id=trace_id or str(uuid.uuid4())[:8],
    )
    op_log.info("scan_started")
    op_log.info("instances_found", count=5, running=4, stopped=1)
    op_log.warning("stopped_instance_found",
                   instance_id="i-0abc123", stopped_since="2025-01-10")
    op_log.info("scan_completed", duration_ms=142)

run_ec2_inventory("us-east-1")
print()
run_ec2_inventory("eu-west-1", trace_id="req-xyz-999")"""),

        md("## Code-Along: Step 4 — Write the Reusable Logger Module"),

        code('''%%writefile logger.py
"""Reusable structured logging module for ops-automation-platform.

Usage:
    from logger import configure_logging, get_logger

    configure_logging()                            # call once at startup
    log = get_logger("my_module", env="production")
    log.info("task_started", task_id="abc-123")

Reference: https://www.structlog.org/en/stable/
"""
import os
import structlog

def configure_logging(level: str | None = None) -> None:
    """Configure structlog processor pipeline from environment variables."""
    environment = os.environ.get("ENVIRONMENT", "development")
    processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.set_exc_info,
    ]
    if environment in ("production", "staging", "ci"):
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

def get_logger(name: str = "ops", **context) -> structlog.stdlib.BoundLogger:
    """Get a bound logger with the given persistent context fields."""
    return structlog.get_logger(name).bind(**context)
'''),

        code("""from logger import configure_logging, get_logger

configure_logging()
log = get_logger("ec2_module", service="ops-platform", env="development")

log.debug("checking_aws_credentials")
log.info("scan_started", region="us-east-1")

try:
    raise ConnectionError("Endpoint unreachable")
except ConnectionError:
    log.error("aws_connection_failed", region="us-east-1")"""),

        md("""## Exercise

Extend `logger.py` to optionally write JSON logs to a file.

**Your task:**
1. Add `log_file: str | None = None` to `configure_logging()`
2. When provided, also write all logs to the file in JSON format
3. Verify both stdout and the file receive the same entries

**Hint:** Integrate with Python's `logging` module. See
[structlog stdlib integration](https://www.structlog.org/en/stable/standard-library.html)."""),

        code("""# TODO: modify configure_logging() to accept log_file=
# TODO: call configure_logging(log_file="ops.log")
# TODO: write a few log entries
# TODO: read and print ops.log to confirm JSON format
"""),

        md("""## Key Takeaways
- JSON logs are the production standard — CloudWatch Insights, ELK, and Loki all ingest JSON natively
- `structlog.get_logger().bind(...)` attaches persistent context once, appears in every line
- Always set log level from `LOG_LEVEL` env var — never hardcode it
- The `logger.py` module from this lesson is imported by every Phase 2–5 lesson

---
**Phase 1 Complete!**

**Next Phase:** [Phase 2 — Cloud Automation (CloudOps)](../phase-2-cloud-automation-cloudops/lesson-2.1-boto3-basics.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-1-python-automation-foundations" / "lesson-1.5-logging-structured.ipynb")


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 2 — Cloud Automation (CloudOps)
# ═══════════════════════════════════════════════════════════════════════════

def lesson_2_1():
    cells = [
        md("""# Lesson 2.1 — AWS boto3 Basics & Authentication

**Level: Beginner**

## Learning Objectives
- Install and configure boto3 (the official AWS SDK for Python)
- Understand the three authentication methods used in DevOps
- Create boto3 `Session`, `client`, and `resource` objects
- Verify credentials safely with `sts:GetCallerIdentity`
- Handle boto3 errors with `ClientError`

**Produces:** `aws_client.py` — a reusable authenticated session factory.

*Official refs:*
- *[boto3 Quickstart](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html)*
- *[boto3 Credentials](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html)*"""),

        md("""## Concepts

### What is boto3?

**boto3** is the official AWS SDK for Python, composed of two packages:
- **Botocore** — low-level foundation (also used by the AWS CLI)
- **Boto3** — higher-level SDK built on top of Botocore

From the [boto3 quickstart](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html):
```python
import boto3
# Use Amazon S3
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)
```

### boto3 Authentication — Credential Chain

boto3 looks for credentials in this order (first match wins):

| Priority | Source | How to set |
|----------|--------|-----------|
| 1 | Env vars | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| 2 | AWS credentials file | `~/.aws/credentials` (via `aws configure`) |
| 3 | AWS config file | `~/.aws/config` |
| 4 | IAM Role (instance / task) | **Automatic** on EC2, ECS, Lambda |

**Security rule:** Use IAM roles (option 4) in production.
Never hardcode access keys in code — they can be committed to Git.

### `client` vs `resource`

| Interface | Level | Use when |
|-----------|-------|----------|
| `client` | Low-level (mirrors raw API) | Full feature access |
| `resource` | High-level (OOP) | Simpler common operations |

*Rule of thumb: prefer `client` — all features, always available.*"""),

        code("""import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install",
                "boto3", "botocore", "--quiet"], capture_output=True)

import boto3, botocore, os
from botocore.exceptions import ClientError, NoCredentialsError

print(f"boto3    version: {boto3.__version__}")
print(f"botocore version: {botocore.__version__}")"""),

        md("## Code-Along: Step 1 — Create a boto3 Session"),

        code("""def create_session(region: str | None = None,
                   profile: str | None = None) -> boto3.Session:
    \"\"\"Create an authenticated boto3 Session.

    Best practice from boto3 docs: always create a Session explicitly
    rather than using module-level globals (boto3.client / boto3.resource).
    This makes your code testable and thread-safe.

    Reference: https://docs.aws.amazon.com/boto3/latest/guide/session.html
    \"\"\"
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    kwargs = {"region_name": region}
    if profile:
        kwargs["profile_name"] = profile
    return boto3.Session(**kwargs)

session = create_session()
print(f"Session region  : {session.region_name}")
print(f"Session profile : {session.profile_name}")"""),

        md("## Code-Along: Step 2 — Verify Credentials with STS"),

        code("""def verify_credentials(session: boto3.Session) -> dict | None:
    \"\"\"Return the caller's AWS identity using sts:GetCallerIdentity.

    This API call is ALWAYS allowed regardless of IAM permissions —
    it is the safest way to confirm credentials are valid.

    Reference: https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html
    \"\"\"
    try:
        sts = session.client("sts")
        r = sts.get_caller_identity()
        return {"account": r["Account"], "user_id": r["UserId"], "arn": r["Arn"]}
    except NoCredentialsError:
        print("✗ No AWS credentials configured.")
        print("  Set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY, or run: aws configure")
        return None
    except ClientError as e:
        print(f"✗ Credential error: {e.response['Error']['Message']}")
        return None

identity = verify_credentials(session)
if identity:
    print("✓ AWS credentials verified:")
    print(f"  Account: {identity['account']}")
    print(f"  ARN    : {identity['arn']}")
else:
    print("ℹ  No credentials — remaining cells show patterns only.")"""),

        md("## Code-Along: Step 3 — Create Service Clients"),

        code("""def get_client(service: str, session: boto3.Session, region: str | None = None):
    \"\"\"Create a boto3 low-level client for the given service.

    Always create clients from a Session, not from the boto3 module directly.
    Reference: https://docs.aws.amazon.com/boto3/latest/guide/clients.html
    \"\"\"
    kwargs = {}
    if region:
        kwargs["region_name"] = region
    return session.client(service, **kwargs)

ec2 = get_client("ec2", session)
s3  = get_client("s3",  session)
cw  = get_client("cloudwatch", session)

print("Created clients:")
for name, client in [("EC2", ec2), ("S3", s3), ("CloudWatch", cw)]:
    svc = client.meta.service_model.service_name
    rgn = client.meta.region_name
    print(f"  {name:<12}: {svc} in {rgn}")"""),

        md("## Code-Along: Step 4 — boto3 Error Handling"),

        code("""from botocore.exceptions import ClientError

def handle_client_error(error: ClientError, operation: str) -> None:
    \"\"\"Parse a boto3 ClientError and print actionable advice.

    ClientError.response['Error']['Code'] contains the AWS error code.
    Reference: https://docs.aws.amazon.com/boto3/latest/guide/error-handling.html
    \"\"\"
    code = error.response["Error"]["Code"]
    msg  = error.response["Error"]["Message"]
    advice = {
        "AccessDenied":              "Check your IAM permissions for this action.",
        "AuthFailure":               "Credentials are invalid or expired.",
        "InvalidInstanceID.NotFound":"Instance does not exist in this region.",
        "NoSuchBucket":              "S3 bucket does not exist.",
        "Throttling":                "Rate-limited — implement exponential backoff.",
    }.get(code, "See AWS documentation for this error code.")

    print(f"AWS Error in '{operation}':")
    print(f"  Code   : {code}")
    print(f"  Message: {msg}")
    print(f"  Advice : {advice}")

# Simulate an AccessDenied error
try:
    raise ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}},
        "GetObject"
    )
except ClientError as e:
    handle_client_error(e, "S3 GetObject")"""),

        md("## Code-Along: Step 5 — Write the AWS Client Module"),

        code('''%%writefile aws_client.py
"""Reusable AWS session and client factory.

Reference: https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html
"""
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

class AWSClientFactory:
    """Thread-safe factory for boto3 clients."""

    def __init__(self, region: str | None = None, profile: str | None = None):
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self._session = boto3.Session(
            region_name=self.region,
            profile_name=profile,
        )
        self._clients: dict = {}   # cache to avoid re-creation overhead

    def get_client(self, service: str, region: str | None = None):
        """Get or create a boto3 client for the given service."""
        key = f"{service}:{region or self.region}"
        if key not in self._clients:
            self._clients[key] = self._session.client(
                service, region_name=region or self.region
            )
        return self._clients[key]

    def get_identity(self) -> dict | None:
        """Return caller identity or None if credentials are invalid."""
        try:
            r = self.get_client("sts").get_caller_identity()
            return {"account": r["Account"], "user_id": r["UserId"], "arn": r["Arn"]}
        except (NoCredentialsError, ClientError):
            return None

    @property
    def is_authenticated(self) -> bool:
        return self.get_identity() is not None
'''),

        md("""## Exercise

Extend `AWSClientFactory` with cross-account role assumption.

**Your task:**
1. Add `from_role(cls, role_arn: str, region: str) -> "AWSClientFactory"` classmethod
2. Inside: call `sts.assume_role()`, extract `Credentials`, build a new `Session`
3. Wrap in try/except — print a helpful message if the role assumption fails
4. Test: `AWSClientFactory.from_role("arn:aws:iam::123456789012:role/ops", "us-east-1")`
   should fail gracefully without real credentials"""),

        code("""# TODO: Add from_role classmethod to AWSClientFactory
# Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role.html

# Expected usage:
# factory = AWSClientFactory.from_role("arn:aws:iam::123456789012:role/ops-role")
# ec2 = factory.get_client("ec2")
"""),

        md("""## Key Takeaways
- Always create a `boto3.Session()` explicitly — avoids global state and makes code testable
- `sts:GetCallerIdentity` is free, always allowed, and the correct way to verify credentials
- `ClientError.response['Error']['Code']` gives you the specific AWS error type
- Cache clients within a session — avoid re-creating them on every call
- In production: use IAM roles (EC2 instance profile, ECS task role, Lambda role) — never hardcode keys

---
**Next:** [Lesson 2.2 — AWS EC2, S3 & CloudWatch](lesson-2.2-ec2-s3-cloudwatch.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-2-cloud-automation-cloudops" / "lesson-2.1-boto3-basics.ipynb")


def lesson_2_2():
    cells = [
        md("""# Lesson 2.2 — AWS EC2, S3 & CloudWatch Automation

**Level: Intermediate**

## Learning Objectives
- List EC2 instances with full **pagination** (never miss page 2+)
- Start, stop, and tag EC2 resources programmatically
- Manage S3: create, upload, download, lifecycle rules
- Publish custom metrics to CloudWatch from Python
- Describe and create CloudWatch alarms

**Produces:** `aws_resources.py` — EC2 / S3 / CloudWatch automation module.

*Official refs:*
- *[boto3 Paginators](https://docs.aws.amazon.com/boto3/latest/guide/paginators.html)*
- *[boto3 EC2 Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)*
- *[boto3 S3 Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)*
- *[boto3 CloudWatch Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html)*"""),

        md("""## Concepts

### Why Paginators?

Many AWS APIs return at most 1,000 items per request (e.g., `describe_instances`, `list_objects_v2`).
If you only call the API once, you silently miss all pages beyond the first.

From the [boto3 paginators guide](https://docs.aws.amazon.com/boto3/latest/guide/paginators.html):

> *"Paginators are a feature of boto3 that act as an abstraction over the process
> of iterating over an entire result set of a truncated API operation."*

```python
# BAD — only first page
response = ec2.describe_instances()

# GOOD — all pages automatically
paginator = ec2.get_paginator("describe_instances")
for page in paginator.paginate():
    for reservation in page["Reservations"]:
        ...
```

### Tags Are the Foundation of AWS Automation

Tags let you:
- **Filter**: find all instances with `Environment=production`
- **Cost-allocate**: AWS bills broken down by tag
- **Automate**: ops scripts that act on resources by tag"""),

        code("""import boto3, json, os
from datetime import datetime, timezone
from botocore.exceptions import ClientError

session = boto3.Session(region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))

# Simulated EC2 instances for demo (replace with real API calls)
SAMPLE_INSTANCES = [
    {"InstanceId": "i-0abc1234567", "State": {"Name": "running"},
     "InstanceType": "t3.micro",  "PrivateIpAddress": "10.0.1.10",
     "LaunchTime": datetime(2025, 1, 10, 8, 0, tzinfo=timezone.utc),
     "Tags": [{"Key": "Name", "Value": "web-server-1"},
               {"Key": "Environment", "Value": "production"}]},
    {"InstanceId": "i-0def5678901", "State": {"Name": "running"},
     "InstanceType": "t3.small",  "PrivateIpAddress": "10.0.1.11",
     "LaunchTime": datetime(2025, 1, 12, 9, 0, tzinfo=timezone.utc),
     "Tags": [{"Key": "Name", "Value": "worker-1"},
               {"Key": "Environment", "Value": "production"}]},
    {"InstanceId": "i-0ghi9012345", "State": {"Name": "stopped"},
     "InstanceType": "r6i.large",  "PrivateIpAddress": "10.0.2.5",
     "LaunchTime": datetime(2025, 1, 1,  0, 0, tzinfo=timezone.utc),
     "Tags": [{"Key": "Name", "Value": "db-backup"},
               {"Key": "Environment", "Value": "production"}]},
]
print(f"Loaded {len(SAMPLE_INSTANCES)} simulated instances.")"""),

        md("## Code-Along: Step 1 — EC2 Inventory with Pagination"),

        code("""def parse_instance(inst: dict, region: str = "us-east-1") -> dict:
    \"\"\"Normalise a raw EC2 instance dict into a flat record.\"\"\"
    tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
    return {
        "instance_id": inst["InstanceId"],
        "name":        tags.get("Name", "(unnamed)"),
        "state":       inst["State"]["Name"],
        "type":        inst.get("InstanceType", ""),
        "private_ip":  inst.get("PrivateIpAddress", ""),
        "launch_time": inst.get("LaunchTime", ""),
        "region":      region,
        "tags":        tags,
    }

def list_ec2_instances(ec2_client, filters: list | None = None) -> list[dict]:
    \"\"\"List all EC2 instances using paginators.

    From the boto3 paginators guide:
    https://docs.aws.amazon.com/boto3/latest/guide/paginators.html

    Uses get_paginator("describe_instances") so ALL pages are fetched
    regardless of how many instances exist in the account.
    \"\"\"
    paginator = ec2_client.get_paginator("describe_instances")
    kwargs = {}
    if filters:
        kwargs["Filters"] = filters
    instances = []
    for page in paginator.paginate(**kwargs):
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                instances.append(parse_instance(inst))
    return instances

# Demo with sample data
instances = [parse_instance(i) for i in SAMPLE_INSTANCES]
print(f"{'ID':<20} {'Name':<20} {'State':<10} {'Type':<12} {'Tags'}")
print("-" * 80)
for i in instances:
    tags = ", ".join(f"{k}={v}" for k, v in i['tags'].items())
    print(f"{i['instance_id']:<20} {i['name']:<20} {i['state']:<10} {i['type']:<12} {tags}")"""),

        md("## Code-Along: Step 2 — EC2 Lifecycle & Tagging"),

        code("""def get_stopped_instances(instances: list[dict]) -> list[dict]:
    return [i for i in instances if i["state"] == "stopped"]

def tag_instances(ec2_client, instance_ids: list[str], tags: dict) -> None:
    \"\"\"Apply tags to EC2 instances.

    Tags are the foundation of AWS cost allocation and automation.
    Reference: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html
    \"\"\"
    tag_list = [{"Key": k, "Value": v} for k, v in tags.items()]
    ec2_client.create_tags(Resources=instance_ids, Tags=tag_list)
    print(f"Tagged {len(instance_ids)} instance(s): {tags}")

stopped = get_stopped_instances(instances)
print(f"Stopped instances: {len(stopped)}")
for i in stopped:
    print(f"  {i['instance_id']} — {i['name']} (stopped since approx {i['launch_time']})")
print()
print("With real credentials, you would call:")
print("  stop_instances(ec2, ['i-0abc1234567'])")
print("  tag_instances(ec2, ['i-0abc1234567'], {'Patched': '2025-01-15', 'PatchedBy': 'ops-bot'})")"""),

        md("## Code-Along: Step 3 — S3 Operations"),

        code("""def upload_json_to_s3(s3_client, bucket: str, key: str, data: dict) -> str:
    \"\"\"Upload a JSON object to S3. Returns the s3:// URI.

    Reference: https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/put_object.html
    \"\"\"
    body = json.dumps(data, indent=2, default=str).encode()
    s3_client.put_object(
        Bucket=bucket, Key=key, Body=body,
        ContentType="application/json",
    )
    return f"s3://{bucket}/{key}"

def list_s3_buckets(s3_client) -> list[dict]:
    \"\"\"List all S3 buckets in the account.\"\"\"
    response = s3_client.list_buckets()
    return [{"name": b["Name"], "created": b["CreationDate"].isoformat()}
            for b in response.get("Buckets", [])]

# Demonstrate the report structure that would be uploaded
report = {
    "scan_date": datetime.utcnow().isoformat() + "Z",
    "total_instances": len(instances),
    "stopped_count": len(get_stopped_instances(instances)),
    "instances": instances,
}
print("Sample report that would be uploaded to S3:")
print(json.dumps(report, indent=2, default=str)[:500] + "...")"""),

        md("## Code-Along: Step 4 — CloudWatch Custom Metrics"),

        code("""def put_inventory_metrics(cw_client, instances: list[dict], region: str) -> None:
    \"\"\"Publish EC2 inventory metrics to CloudWatch.

    Custom metrics allow you to track operational data that AWS does not
    measure natively (e.g., number of stopped instances per region).

    Reference: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html
    Namespace: OpsAutomation/Resources
    \"\"\"
    now = datetime.now(timezone.utc)
    running = sum(1 for i in instances if i["state"] == "running")
    stopped = sum(1 for i in instances if i["state"] != "running")

    metric_data = [
        {"MetricName": "TotalInstances",   "Value": float(len(instances)),
         "Unit": "Count", "Timestamp": now,
         "Dimensions": [{"Name": "Region", "Value": region}]},
        {"MetricName": "RunningInstances", "Value": float(running),
         "Unit": "Count", "Timestamp": now,
         "Dimensions": [{"Name": "Region", "Value": region}]},
        {"MetricName": "StoppedInstances", "Value": float(stopped),
         "Unit": "Count", "Timestamp": now,
         "Dimensions": [{"Name": "Region", "Value": region}]},
    ]
    cw_client.put_metric_data(Namespace="OpsAutomation/Resources",
                              MetricData=metric_data)

print("CloudWatch metrics that WOULD be published (Namespace: OpsAutomation/Resources):")
for name, value in [("TotalInstances", 3), ("RunningInstances", 2), ("StoppedInstances", 1)]:
    print(f"  {name:<22} = {value}  [Region=us-east-1]")"""),

        code('''%%writefile aws_resources.py
"""AWS EC2, S3, and CloudWatch automation.

Reference:
  EC2:        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
  S3:         https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
  CloudWatch: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
"""
import json
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def list_ec2_instances(ec2_client, filters=None) -> list[dict]:
    """List EC2 instances using pagination (all pages)."""
    paginator = ec2_client.get_paginator("describe_instances")
    kwargs = {"Filters": filters} if filters else {}
    instances = []
    for page in paginator.paginate(**kwargs):
        for r in page["Reservations"]:
            for inst in r["Instances"]:
                tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
                instances.append({
                    "instance_id": inst["InstanceId"],
                    "name":        tags.get("Name", "(unnamed)"),
                    "state":       inst["State"]["Name"],
                    "type":        inst.get("InstanceType", ""),
                    "private_ip":  inst.get("PrivateIpAddress", ""),
                    "tags":        tags,
                })
    return instances

def upload_report_s3(s3_client, bucket: str, key: str, data: dict) -> str:
    """Upload a JSON report to S3. Returns the s3:// URI."""
    body = json.dumps(data, indent=2, default=str).encode()
    s3_client.put_object(Bucket=bucket, Key=key, Body=body,
                         ContentType="application/json")
    return f"s3://{bucket}/{key}"

def put_inventory_metrics(cw_client, instances: list[dict], region: str) -> None:
    """Publish EC2 inventory counts to CloudWatch."""
    now = datetime.now(timezone.utc)
    dims = [{"Name": "Region", "Value": region}]
    running = sum(1 for i in instances if i["state"] == "running")
    stopped = sum(1 for i in instances if i["state"] != "running")
    cw_client.put_metric_data(
        Namespace="OpsAutomation/Resources",
        MetricData=[
            {"MetricName": "TotalInstances",   "Value": float(len(instances)),
             "Unit": "Count", "Timestamp": now, "Dimensions": dims},
            {"MetricName": "RunningInstances", "Value": float(running),
             "Unit": "Count", "Timestamp": now, "Dimensions": dims},
            {"MetricName": "StoppedInstances", "Value": float(stopped),
             "Unit": "Count", "Timestamp": now, "Dimensions": dims},
        ]
    )
'''),

        md("""## Exercise

Write `find_untagged_instances(instances, required_tag="Environment") -> list[dict]`.

**Your task:**
1. Filter instances that are missing the `required_tag` key in their `tags` dict
2. Return `[{instance_id, name}]`
3. Test against `SAMPLE_INSTANCES` — add one instance with empty tags first"""),

        code("""# Add an untagged instance to the sample
untagged_sample = instances + [
    {"instance_id": "i-0mystery", "name": "mystery-box",
     "state": "running", "type": "t2.micro",
     "private_ip": "10.0.3.1", "region": "us-east-1", "tags": {}}
]

# TODO: implement find_untagged_instances
def find_untagged_instances(instances: list[dict], required_tag: str = "Environment") -> list[dict]:
    pass

untagged = find_untagged_instances(untagged_sample)
print(f"Untagged instances: {len(untagged)}")
for i in untagged:
    print(f"  {i['instance_id']} — {i.get('name','(unnamed)')}")
"""),

        md("""## Key Takeaways
- Always use `get_paginator()` for list operations — a single call only returns the first page
- Tags are the foundation of AWS automation: filter, group, cost-allocate, and automate by tag
- CloudWatch custom metrics allow you to push any operational data from Python scripts
- `datetime.now(timezone.utc)` — always use UTC for AWS timestamps

---
**Next:** [Lesson 2.3 — Azure SDK for Python](lesson-2.3-azure-sdk.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-2-cloud-automation-cloudops" / "lesson-2.2-ec2-s3-cloudwatch.ipynb")


def stub_notebook(title: str, phase_dir: str, filename: str,
                  prev_link: str, next_link: str,
                  topics: list[str],
                  exercise: str,
                  refs: list[tuple[str, str]]) -> None:
    """Generate a well-structured stub notebook for remaining lessons."""
    ref_table = "\n".join(f"- *[{name}]({url})*" for name, url in refs)
    topic_list = "\n".join(f"- {t}" for t in topics)
    cells = [
        md(f"""# {title}

**Level: Intermediate**

## Learning Objectives

{topic_list}

*Official references:*
{ref_table}"""),

        md("## Concepts\n\n> Run the setup cell below, then read through each concept section."),

        code("import subprocess, sys\n# Install required packages\n# subprocess.run([sys.executable, '-m', 'pip', 'install', '...', '--quiet'], capture_output=True)\nprint('Setup complete.')"),

        md("## Code-Along: Step 1\n\n> Complete this section by running each cell top-to-bottom."),

        code("# Step 1 — implement here\npass"),

        md("## Code-Along: Step 2"),

        code("# Step 2 — implement here\npass"),

        md("## Code-Along: Step 3"),

        code("# Step 3 — implement here\npass"),

        md(f"## Exercise\n\n{exercise}"),

        code("# TODO: implement the exercise\npass"),

        md(f"""## Key Takeaways

- Review the official references linked above for authoritative details.
- Run each code cell top-to-bottom before attempting the exercise.

---
**Previous:** [{prev_link}]({prev_link})  
**Next:** [{next_link}]({next_link})"""),
    ]
    save(notebook(cells), BASE / phase_dir / filename)


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 5 — Monitoring
# ═══════════════════════════════════════════════════════════════════════════

def lesson_5_1():
    cells = [
        md("""# Lesson 5.1 — Prometheus Custom Metrics & Exporters

**Level: Intermediate**

## Learning Objectives
- Understand the four Prometheus metric types: Counter, Gauge, Histogram, Summary
- Use `prometheus_client` to define metrics with labels
- Build a custom Prometheus exporter that exposes a `/metrics` HTTP endpoint
- Understand label cardinality constraints
- Stream live metrics to a Prometheus scrape target

**Produces:** `prometheus_exporter.py` — a standalone metrics exporter.

*Official refs:*
- *[Prometheus Python Client](https://github.com/prometheus/client_python)*
- *[Prometheus Data Model](https://prometheus.io/docs/concepts/data_model/)*
- *[Prometheus Metric Types](https://prometheus.io/docs/concepts/metric_types/)*"""),

        md("""## Concepts

### Prometheus Pull Model

Prometheus **pulls** (scrapes) metrics from an HTTP endpoint on your service every N seconds:

```
Prometheus Server
    └── every 15s: GET http://my-service:9090/metrics
            └── Returns text/plain in Prometheus exposition format
                    └── Stored in time-series DB → Grafana → alerts
```

Install the Python client:
```bash
pip install prometheus-client
```

### Four Metric Types

| Type | Goes up/down? | Use case | Example |
|------|--------------|----------|---------|
| **Counter** | Only up | Total events | Requests, errors, scans |
| **Gauge** | Up & down | Current state | CPU %, instance count |
| **Histogram** | N/A | Distribution of values | Request duration |
| **Summary** | N/A | Pre-computed quantiles | p50/p95/p99 latency |

### Labels — Multi-Dimensional Metrics

Labels add dimensions to a metric:
```
ops_instances_total{region="us-east-1", state="running"} 5
ops_instances_total{region="eu-west-1", state="running"} 3
ops_instances_total{region="us-east-1", state="stopped"} 1
```

**Label cardinality rule:** Only use labels with a **small, finite** set of values
(region, state, environment). Never use user IDs, request IDs, or timestamps as labels —
each unique label combination creates a new time series in the database."""),

        code("""import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install",
                "prometheus_client", "--quiet"], capture_output=True)

import prometheus_client as prom
from prometheus_client import (
    Counter, Gauge, Histogram, Summary,
    CollectorRegistry, generate_latest,
)
print(f"prometheus_client version: {prom.__version__}")"""),

        md("## Code-Along: Step 1 — Define Metrics"),

        code("""# Use a custom registry so this notebook doesn't collide with the default
registry = CollectorRegistry()

# COUNTER: total scans — monotonically increasing
ops_scans_total = Counter(
    name="ops_scans_total",
    documentation="Total number of resource inventory scans performed.",
    labelnames=["provider", "region", "status"],
    registry=registry,
)

# GAUGE: current instance count — goes up and down
ops_instances_total = Gauge(
    name="ops_instances_total",
    documentation="Current number of cloud instances by state.",
    labelnames=["provider", "region", "state"],
    registry=registry,
)

ops_stopped_instances = Gauge(
    name="ops_stopped_instances_count",
    documentation="Number of stopped/terminated instances (potential cost waste).",
    labelnames=["provider", "region"],
    registry=registry,
)

ops_compliance_score = Gauge(
    name="ops_compliance_score_percent",
    documentation="CIS compliance score as a percentage (0–100).",
    labelnames=["account", "framework"],
    registry=registry,
)

# HISTOGRAM: scan duration — buckets in seconds
ops_scan_duration = Histogram(
    name="ops_scan_duration_seconds",
    documentation="Time taken to complete a resource scan.",
    labelnames=["provider", "scan_type"],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
    registry=registry,
)

# COUNTER: security findings
ops_security_findings = Counter(
    name="ops_security_findings_total",
    documentation="Total security findings detected by automated scans.",
    labelnames=["tool", "severity"],
    registry=registry,
)

print("Metrics registered:")
for metric in [
    "ops_scans_total", "ops_instances_total",
    "ops_stopped_instances_count", "ops_compliance_score_percent",
    "ops_scan_duration_seconds", "ops_security_findings_total",
]:
    print(f"  {metric}")"""),

        md("## Code-Along: Step 2 — Recording Metric Values"),

        code("""import time, random

def simulate_inventory_scan(provider: str, region: str) -> dict:
    \"\"\"Simulate an inventory scan and record Prometheus metrics.\"\"\"
    start = time.monotonic()

    running = random.randint(3, 10)
    stopped = random.randint(0, 3)

    # Record current state (Gauge)
    ops_instances_total.labels(provider=provider, region=region, state="running").set(running)
    ops_instances_total.labels(provider=provider, region=region, state="stopped").set(stopped)
    ops_stopped_instances.labels(provider=provider, region=region).set(stopped)

    # Increment scan counter
    ops_scans_total.labels(provider=provider, region=region, status="success").inc()

    # Observe scan duration
    duration = time.monotonic() - start + random.uniform(0.05, 1.5)
    ops_scan_duration.labels(provider=provider, scan_type="inventory").observe(duration)

    return {"running": running, "stopped": stopped, "duration_s": round(duration, 3)}

# Record compliance score
ops_compliance_score.labels(account="123456789012", framework="CIS-AWS").set(82.5)

# Simulate security findings (Counter: can only inc, never dec)
ops_security_findings.labels(tool="bandit",    severity="HIGH").inc(2)
ops_security_findings.labels(tool="trivy",     severity="CRITICAL").inc(0)
ops_security_findings.labels(tool="pip-audit", severity="HIGH").inc(1)

# Run scans
for provider, regions in [("aws", ["us-east-1", "eu-west-1"]), ("gcp", ["us-central1"])]:
    for region in regions:
        r = simulate_inventory_scan(provider, region)
        print(f"  {provider}/{region}: running={r['running']}, stopped={r['stopped']}, "
              f"duration={r['duration_s']}s")
print("\\nMetrics recorded.")"""),

        md("## Code-Along: Step 3 — View the /metrics Output"),

        code("""# generate_latest() produces the text that the /metrics endpoint returns
output = generate_latest(registry).decode("utf-8")
lines = output.splitlines()
print(f"Total lines in /metrics output: {len(lines)}")
print()

# Filter out comment lines to see just the values
data_lines = [l for l in lines if l and not l.startswith("#")]
print(f"Data lines (non-comment metric values):")
for line in data_lines[:20]:
    print(f"  {line}")
if len(data_lines) > 20:
    print(f"  ... ({len(data_lines) - 20} more)")"""),

        md("## Code-Along: Step 4 — Write the Prometheus Exporter"),

        code('''%%writefile prometheus_exporter.py
"""Custom Prometheus exporter for the Ops Automation Platform.

Exposes cloud resource, security, and compliance metrics at /metrics.

Usage:
    python prometheus_exporter.py
    # then: curl http://localhost:9090/metrics

Prometheus scrape config (prometheus.yml):
    scrape_configs:
      - job_name: ops-platform
        static_configs:
          - targets: [localhost:9090]

Reference: https://github.com/prometheus/client_python
"""
import os, time, random
from prometheus_client import (
    Counter, Gauge, Histogram,
    CollectorRegistry, start_http_server, generate_latest,
)

registry = CollectorRegistry()

instances_gauge = Gauge(
    "ops_ec2_instances", "EC2 instance count by state.",
    ["region", "state"], registry=registry,
)
scan_counter = Counter(
    "ops_inventory_scans_total", "Total inventory scans performed.",
    ["provider", "status"], registry=registry,
)
scan_duration = Histogram(
    "ops_scan_duration_seconds", "Duration of inventory scans.",
    ["provider"], buckets=[0.1, 0.5, 1.0, 5.0, 30.0], registry=registry,
)
compliance_score = Gauge(
    "ops_compliance_score", "CIS compliance score (0–100).",
    ["account", "framework"], registry=registry,
)
security_findings = Gauge(
    "ops_security_findings", "Active security findings by severity.",
    ["tool", "severity"], registry=registry,
)


def collect_metrics() -> None:
    """Collect current metrics. Replace stubs with real API calls."""
    with scan_duration.labels(provider="aws").time():
        time.sleep(random.uniform(0.05, 0.5))   # simulate API latency
        instances_gauge.labels(region="us-east-1", state="running").set(random.randint(3, 10))
        instances_gauge.labels(region="us-east-1", state="stopped").set(random.randint(0, 3))
    scan_counter.labels(provider="aws", status="success").inc()
    compliance_score.labels(account="123456789012", framework="CIS-AWS").set(
        random.uniform(75, 95)
    )
    security_findings.labels(tool="bandit",    severity="HIGH").set(random.randint(0, 3))
    security_findings.labels(tool="trivy",     severity="CRITICAL").set(0)


if __name__ == "__main__":
    port     = int(os.environ.get("METRICS_PORT",    "9090"))
    interval = int(os.environ.get("SCRAPE_INTERVAL", "30"))

    start_http_server(port, registry=registry)
    print(f"✓  Prometheus exporter started  →  http://0.0.0.0:{port}/metrics")
    print(f"   Collecting metrics every {interval}s.  Press Ctrl+C to stop.")

    collect_metrics()   # first collection immediately
    while True:
        time.sleep(interval)
        collect_metrics()
        print(f"   metrics refreshed at {time.strftime('%H:%M:%S')}")
'''),

        md("## Code-Along: Step 5 — Quick HTTP Test"),

        code("""import threading, time, urllib.request
from prometheus_client import start_http_server

start_http_server(9092, registry=registry)
time.sleep(0.3)

try:
    with urllib.request.urlopen("http://localhost:9092/metrics", timeout=3) as resp:
        body = resp.read().decode()
    values = [l for l in body.splitlines() if l and not l.startswith("#")]
    print(f"✓  /metrics endpoint is live  ({len(values)} value lines)")
    for line in values[:8]:
        print(f"   {line}")
except Exception as e:
    print(f"Could not reach endpoint: {e}")
    print("Run 'python prometheus_exporter.py' manually to test.")"""),

        md("""## Exercise

Add a `ops_last_scan_timestamp_seconds` Gauge metric.

**Your task:**
1. Define `Gauge("ops_last_scan_timestamp_seconds", ..., ["provider"])`
2. In `collect_metrics()`, call `.set(time.time())` after each successful scan
3. In Prometheus/Grafana, the expression `time() - ops_last_scan_timestamp_seconds`
   tells you how many seconds ago the last scan ran — useful for "no-data" alerts

Verify it appears in `generate_latest(registry)`."""),

        code("""# TODO: define ops_last_scan_timestamp_seconds Gauge
# last_scan_ts = Gauge("ops_last_scan_timestamp_seconds", "...", ["provider"], registry=registry)

# TODO: set it in simulate_inventory_scan()
# last_scan_ts.labels(provider=provider).set(time.time())

# TODO: verify
# print(generate_latest(registry).decode())
"""),

        md("""## Key Takeaways
- Use **Gauge** for values that go up/down; **Counter** for cumulative totals
- Labels must be **low-cardinality** — region, state, environment (not request IDs)
- `start_http_server(port, registry=registry)` is all you need to expose `/metrics`
- Use `with histogram.time():` to automatically observe the duration of a code block
- The exporter pattern (background collection loop + HTTP endpoint) is the standard

---
**Next:** [Lesson 5.2 — OpenTelemetry Python](lesson-5.2-opentelemetry-python.ipynb)"""),
    ]
    save(notebook(cells),
         BASE / "phase-5-monitoring-observability-alerting" / "lesson-5.1-prometheus-custom-metrics.ipynb")


# ═══════════════════════════════════════════════════════════════════════════
# Remaining lessons — structured stubs grounded in official docs
# ═══════════════════════════════════════════════════════════════════════════

def generate_remaining():
    lessons = [
        # Phase 2
        ("lesson-2.3-azure-sdk.ipynb",
         "phase-2-cloud-automation-cloudops",
         "Lesson 2.3 — Azure SDK for Python",
         [
             "Authenticate to Azure using `DefaultAzureCredential` (the modern approach)",
             "List and manage Azure Resource Groups and Virtual Machines",
             "Work with Azure Blob Storage (`azure-storage-blob`)",
             "Query Azure Monitor metrics for VMs",
         ],
         "Write `find_vms_without_tags(vms, required_tags)` that returns VMs missing any required tag.",
         [
             ("Azure SDK for Python", "https://learn.microsoft.com/en-us/azure/developer/python/"),
             ("DefaultAzureCredential", "https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential"),
             ("azure-storage-blob", "https://learn.microsoft.com/en-us/python/api/azure-storage-blob/"),
         ]),
        ("lesson-2.4-gcp-sdk.ipynb",
         "phase-2-cloud-automation-cloudops",
         "Lesson 2.4 — GCP SDK for Python",
         [
             "Authenticate with Application Default Credentials (ADC) — `gcloud auth application-default login`",
             "List and manage Compute Engine instances using `google-cloud-compute`",
             "Upload/download objects with `google-cloud-storage`",
             "Write custom metrics to Cloud Monitoring",
         ],
         "Write `find_terminated_instances(instances)` that returns GCE instances with status `TERMINATED`.",
         [
             ("GCP Python Client Libraries", "https://cloud.google.com/python/docs/reference"),
             ("ADC documentation", "https://cloud.google.com/docs/authentication/application-default-credentials"),
             ("google-cloud-storage", "https://cloud.google.com/python/docs/reference/storage/latest"),
         ]),
        ("lesson-2.5-multi-cloud-patterns.ipynb",
         "phase-2-cloud-automation-cloudops",
         "Lesson 2.5 — Multi-Cloud Patterns",
         [
             "Design a cloud-provider abstraction using Python `typing.Protocol`",
             "Implement AWS, Azure, and GCP adapters that normalise to a shared `CloudInstance` dataclass",
             "Aggregate multi-cloud inventory into a single list",
             "Generate and save a cross-cloud JSON report",
         ],
         "Write `find_untagged_across_clouds(instances, required_tag='env')` and print a summary per provider.",
         [
             ("typing.Protocol (PEP 544)", "https://docs.python.org/3/library/typing.html#typing.Protocol"),
             ("dataclasses module", "https://docs.python.org/3/library/dataclasses.html"),
         ]),
        # Phase 3
        ("lesson-3.1-docker-sdk.ipynb",
         "phase-3-cicd-container-automation",
         "Lesson 3.1 — Docker SDK for Python",
         [
             "Connect to the Docker daemon with `docker.from_env()`",
             "Build Docker images programmatically from a `Dockerfile`",
             "Run, stop, and remove containers; stream container logs",
             "List images and containers; handle `NotFound` and `APIError`",
         ],
         "Add `run_one_shot(image, command) -> str` that runs a container, waits for exit, and returns stdout.",
         [
             ("Docker SDK for Python (docker-py)", "https://docker-py.readthedocs.io/en/stable/"),
             ("docker.from_env()", "https://docker-py.readthedocs.io/en/stable/client.html#docker.from_env"),
         ]),
        ("lesson-3.2-kubernetes-client.ipynb",
         "phase-3-cicd-container-automation",
         "Lesson 3.2 — Kubernetes Python Client",
         [
             "Connect to a cluster via `config.load_kube_config()` or `load_incluster_config()`",
             "List Pods, Deployments, and Services with `CoreV1Api` and `AppsV1Api`",
             "Create Deployments with resource requests/limits",
             "Create ConfigMaps and Secrets programmatically",
         ],
         "Write `get_unhealthy_pods(pods)` that returns pods where `ready=False` or `phase != Running`.",
         [
             ("Kubernetes Python Client", "https://github.com/kubernetes-client/python"),
             ("Kubernetes API Reference", "https://kubernetes.io/docs/reference/kubernetes-api/"),
         ]),
        ("lesson-3.3-github-actions-pygithub.ipynb",
         "phase-3-cicd-container-automation",
         "Lesson 3.3 — GitHub Actions & PyGitHub",
         [
             "Authenticate to GitHub with `PyGitHub` using a Personal Access Token",
             "List repositories, branches, and open PRs",
             "Trigger `workflow_dispatch` events via the API",
             "Write a GitHub Actions workflow YAML that runs Python ops scripts",
         ],
         "Write `wait_for_workflow_completion(client, repo, workflow_id, timeout=300) -> str` that polls every 10 s.",
         [
             ("PyGitHub documentation", "https://pygithub.readthedocs.io/"),
             ("GitHub REST API", "https://docs.github.com/en/rest"),
             ("workflow_dispatch event", "https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_dispatch"),
         ]),
        ("lesson-3.4-pipeline-scripting-patterns.ipynb",
         "phase-3-cicd-container-automation",
         "Lesson 3.4 — Pipeline Scripting Patterns",
         [
             "Write idempotent pipeline steps (check-before-create)",
             "Implement retry with exponential backoff and jitter using a decorator",
             "Run independent steps in parallel with `concurrent.futures.ThreadPoolExecutor`",
             "Build a `Pipeline` orchestrator with fail-fast semantics",
         ],
         "Extend `Pipeline` with `skip_if: Callable` per step and `on_failure` / `on_success` callbacks.",
         [
             ("concurrent.futures", "https://docs.python.org/3/library/concurrent.futures.html"),
             ("functools.wraps", "https://docs.python.org/3/library/functools.html#functools.wraps"),
         ]),
        ("lesson-3.5-gitops-helm-automation.ipynb",
         "phase-3-cicd-container-automation",
         "Lesson 3.5 — GitOps & Helm Automation",
         [
             "Automate `helm list`, `helm upgrade --install`, and `helm template` via `subprocess`",
             "Generate environment-specific `values.yaml` files programmatically",
             "Interact with the ArgoCD REST API to list apps and trigger sync",
             "Detect configuration drift between Git and the running cluster",
         ],
         "Write `sync_out_of_sync_apps(argocd_client, dry_run=True)` that syncs all OutOfSync applications.",
         [
             ("Helm documentation", "https://helm.sh/docs/"),
             ("ArgoCD REST API", "https://argo-cd.readthedocs.io/en/stable/developer-guide/api-docs/"),
         ]),
        # Phase 4
        ("lesson-4.1-static-analysis.ipynb",
         "phase-4-security-automation-devsecops",
         "Lesson 4.1 — Static Analysis & Dependency Scanning",
         [
             "Run Bandit SAST with `-f json` and parse findings by severity",
             "Scan dependencies for known CVEs with `pip-audit --format json`",
             "Understand CVSS severity levels (Critical, High, Medium, Low)",
             "Generate a structured Markdown security report",
         ],
         "Write `generate_markdown_report(bandit_result, pip_result) -> str` and save it to `security_report.md`.",
         [
             ("Bandit documentation", "https://bandit.readthedocs.io/en/latest/"),
             ("pip-audit", "https://pypi.org/project/pip-audit/"),
             ("OWASP Python Security", "https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html"),
         ]),
        ("lesson-4.2-container-security.ipynb",
         "phase-4-security-automation-devsecops",
         "Lesson 4.2 — Container & Image Security",
         [
             "Run Trivy image scans via `subprocess` and parse CVEs from JSON output",
             "Implement a Python Dockerfile linter for common security issues",
             "Build a `SecurityGate` class that blocks on critical CVEs",
             "Scan multiple images in parallel with `ThreadPoolExecutor`",
         ],
         "Write `scan_all_images(images: list[str]) -> dict` that scans images in parallel and returns a summary.",
         [
             ("Trivy documentation", "https://aquasecurity.github.io/trivy/"),
             ("CIS Docker Benchmark", "https://www.cisecurity.org/benchmark/docker"),
             ("Docker security best practices", "https://docs.docker.com/develop/security-best-practices/"),
         ]),
        ("lesson-4.3-secrets-management.ipynb",
         "phase-4-security-automation-devsecops",
         "Lesson 4.3 — Secrets Management",
         [
             "Read secrets from AWS Secrets Manager using boto3",
             "Interact with HashiCorp Vault KV v2 using the `hvac` library",
             "Build a `SecretStore` class that routes to the right backend by environment",
             "Detect hardcoded credentials with `detect-secrets`",
         ],
         "Write `rotate_secret(name, new_value, backend)` and `verify_rotation(name, expected_value, backend) -> bool`.",
         [
             ("AWS Secrets Manager developer guide", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/"),
             ("HVAC (Vault Python client)", "https://hvac.readthedocs.io/en/stable/"),
             ("detect-secrets", "https://github.com/Yelp/detect-secrets"),
         ]),
        ("lesson-4.4-compliance-as-code.ipynb",
         "phase-4-security-automation-devsecops",
         "Lesson 4.4 — Compliance as Code",
         [
             "Understand CIS AWS Foundations Benchmark controls",
             "Write Python checks for CIS 1.4, 1.5, and 4.1 using boto3",
             "Build a `ComplianceReport` with pass/fail counts and a compliance score",
             "Implement `check_s3_public_access` (CIS 2.1.5)",
         ],
         "Add `check_s3_public_access(self) -> list[ComplianceFinding]` to `AWSComplianceChecker`.",
         [
             ("CIS AWS Foundations Benchmark", "https://www.cisecurity.org/benchmark/amazon_web_services"),
             ("AWS Security Hub CIS controls", "https://docs.aws.amazon.com/securityhub/latest/userguide/cis-aws-foundations-benchmark.html"),
         ]),
        ("lesson-4.5-security-gates-cicd.ipynb",
         "phase-4-security-automation-devsecops",
         "Lesson 4.5 — Security Gates in CI/CD",
         [
             "Combine Bandit, pip-audit, Trivy, and compliance checks into a unified gate",
             "Configure environment-specific thresholds (dev=warn, prod=block)",
             "Write a GitHub Actions DevSecOps workflow YAML",
             "Build a `security_gate.py` CLI with Click",
         ],
         "Add Trivy scanning to `security_gate.py`: `--image` option that fails on CRITICAL CVEs.",
         [
             ("OWASP DevSecOps Guideline", "https://owasp.org/www-project-devsecops-guideline/"),
             ("GitHub Actions security hardening", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions"),
         ]),
        # Phase 5
        ("lesson-5.2-opentelemetry-python.ipynb",
         "phase-5-monitoring-observability-alerting",
         "Lesson 5.2 — OpenTelemetry Python",
         [
             "Configure `TracerProvider` with `BatchSpanProcessor` and OTLP exporter",
             "Create spans and child spans with `start_as_current_span()`",
             "Add attributes, events, and exception recording to spans",
             "Propagate trace context across service boundaries with `inject` / `extract`",
         ],
         "Instrument a function with the `@traced` decorator from `traced_ops.py` and verify span output.",
         [
             ("OpenTelemetry Python docs", "https://opentelemetry-python.readthedocs.io/"),
             ("OpenTelemetry Getting Started", "https://opentelemetry.io/docs/getting-started/"),
             ("W3C Trace Context spec", "https://www.w3.org/TR/trace-context/"),
         ]),
        ("lesson-5.3-cloud-native-monitoring.ipynb",
         "phase-5-monitoring-observability-alerting",
         "Lesson 5.3 — Cloud-Native Monitoring",
         [
             "Publish custom metrics to CloudWatch with `put_metric_data` (batch up to 20)",
             "Create and describe CloudWatch alarms with `put_metric_alarm`",
             "Send metrics to the Datadog v2 Metrics API via `requests`",
             "Build `publish_ops_dashboard_metrics(inventory)` that publishes per-provider counts",
         ],
         "Write `get_firing_alarms(region) -> list[dict]` that returns all CloudWatch alarms in ALARM state.",
         [
             ("CloudWatch PutMetricData API", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricData.html"),
             ("Datadog Metrics API", "https://docs.datadoghq.com/api/latest/metrics/"),
         ]),
        ("lesson-5.4-structured-logging-aggregation.ipynb",
         "phase-5-monitoring-observability-alerting",
         "Lesson 5.4 — Structured Logging & Log Aggregation",
         [
             "Use `structlog.contextvars.bind_contextvars` to inject trace IDs into every log entry",
             "Push JSON logs to Grafana Loki via the HTTP push API",
             "Index log documents in Elasticsearch with `elasticsearch-py`",
             "Implement log sampling: always log ERROR+; sample INFO at configurable rate",
         ],
         "Write `LogSampler(backend, sample_rate=0.1)` that drops INFO/DEBUG at the configured rate but always forwards WARNING+.",
         [
             ("Loki HTTP API", "https://grafana.com/docs/loki/latest/reference/loki-http-api/"),
             ("Elasticsearch Python client", "https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/"),
             ("structlog contextvars", "https://www.structlog.org/en/stable/contextvars.html"),
         ]),
        ("lesson-5.5-alerting-incident-automation.ipynb",
         "phase-5-monitoring-observability-alerting",
         "Lesson 5.5 — Alerting & Incident Automation",
         [
             "Send formatted alerts to Slack via Incoming Webhooks with Block Kit",
             "Trigger, acknowledge, and resolve PagerDuty incidents with Events v2 API",
             "Implement alert deduplication with a TTL-based in-memory cache",
             "Build an `AlertRouter` that routes info→Slack, critical→Slack+PagerDuty",
         ],
         "Add OpsGenie support to `AlertRouter`: `trigger_opsgenie(api_key, message, severity, alias, details)`.",
         [
             ("Slack Incoming Webhooks", "https://api.slack.com/messaging/webhooks"),
             ("PagerDuty Events API v2", "https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview"),
             ("OpsGenie Alert API", "https://docs.opsgenie.com/docs/alert-api"),
         ]),
        ("lesson-5.6-dashboards-as-code.ipynb",
         "phase-5-monitoring-observability-alerting",
         "Lesson 5.6 — Dashboards as Code",
         [
             "Create Grafana dashboards via the HTTP API (`POST /api/dashboards/db`)",
             "Build Stat, Timeseries, and Table panels in Python dicts",
             "Provision a Prometheus datasource programmatically",
             "Save dashboards to Git for version-controlled, repeatable deployment",
         ],
         "Write `provision_prometheus_datasource(grafana, prometheus_url)` and test it.",
         [
             ("Grafana Dashboard HTTP API", "https://grafana.com/docs/grafana/latest/developers/http_api/dashboard/"),
             ("Grafana Dashboard JSON model", "https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/view-dashboard-json-model/"),
         ]),
    ]

    for info in lessons:
        fname, phase_dir, title, topics, exercise, refs = info
        stub_notebook(title, phase_dir, fname,
                      prev_link=fname, next_link=fname,
                      topics=topics, exercise=exercise, refs=refs)


# ═══════════════════════════════════════════════════════════════════════════
# CAPSTONE
# ═══════════════════════════════════════════════════════════════════════════

def capstone():
    cells = [
        md("""# Capstone Project — Python Ops Automation Platform

**Level: Intermediate**

## Objective

Build a production-ready **`ops-bot`** CLI tool that integrates every phase of this course.

### What You Will Build

A Python CLI (`ops-bot`) with four commands:

| Command | What it does | Phases used |
|---------|-------------|-------------|
| `ops-bot inventory` | List AWS EC2 instances with Rich table output | 1, 2 |
| `ops-bot scan` | Run Bandit + pip-audit; exit 1 on HIGH findings | 1, 4 |
| `ops-bot report` | Run inventory + scan; publish Prometheus metrics; send Slack alert | 1–5 |
| `ops-bot serve` | Start Prometheus metrics HTTP server | 5 |

The platform is also packaged as a Docker container with a `docker-compose.yml`
that spins up `ops-bot + Prometheus + Grafana`.

### Rules
- Work through steps **in order** — each builds on the previous
- Refer to lessons when stuck, but try to implement first
- Complete the verification checklist before moving to stretch goals

**Estimated time:** 6–10 hours"""),

        md("""## Prerequisites

Before starting, verify you have:

- [ ] Python 3.10+ and a virtual environment activated
- [ ] Docker Desktop running
- [ ] AWS credentials configured (`aws sts get-caller-identity` works), OR LocalStack for simulation
- [ ] All Phase 1–5 lessons completed or reviewed
- [ ] Slack incoming webhook URL (optional — alerts can be simulated)

**Reference lessons:**

| Step | Lesson |
|------|--------|
| Project structure | 1.1 |
| Config & .env | 1.3 |
| Click CLI | 1.4 |
| Structured logging | 1.5 |
| boto3 / EC2 | 2.1, 2.2 |
| Security scanning | 4.1, 4.2 |
| Prometheus metrics | 5.1 |
| Slack alerting | 5.5 |"""),

        md("## Step 1: Create the Project Structure\n\n*Refer to: Lesson 1.1*"),

        code("""from pathlib import Path
import subprocess, sys

root = Path("ops-bot")
dirs = [
    root / "src" / "ops_bot" / "cloud",
    root / "src" / "ops_bot" / "security",
    root / "src" / "ops_bot" / "monitoring",
    root / "src" / "ops_bot" / "alerting",
    root / "tests",
    root / "configs",
    root / "dashboards",
]
for d in dirs:
    d.mkdir(parents=True, exist_ok=True)
    (d / "__init__.py").touch()

print("Project structure created:")
for f in sorted(root.rglob("*")):
    rel = f.relative_to(root)
    print(f"  {'  ' * (len(rel.parts)-1)}{'📁' if f.is_dir() else '📄'} {rel.name}")"""),

        md("## Step 2: Install Dependencies"),

        code("""reqs = (
    "boto3>=1.28.0\\n"
    "python-dotenv>=1.0.0\\n"
    "pyyaml>=6.0.1\\n"
    "click>=8.1.7\\n"
    "rich>=13.7.0\\n"
    "structlog>=24.1.0\\n"
    "prometheus_client>=0.19.0\\n"
    "requests>=2.31.0\\n"
)
(root / "requirements.txt").write_text(reqs)

subprocess.run(
    [sys.executable, "-m", "pip", "install"] +
    [l for l in reqs.splitlines() if l and not l.startswith("#")] +
    ["--quiet"],
    capture_output=True
)
print("Dependencies installed.")"""),

        md("## Step 3: Configuration Module\n\n*Refer to: Lesson 1.3*"),

        code("""%%writefile ops-bot/src/ops_bot/config.py
\"\"\"Application configuration loaded from environment variables.

Reference: https://12factor.net/config
\"\"\"
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root (won't override existing env vars)
load_dotenv(Path(__file__).parents[3] / ".env", override=False)

@dataclass
class AlertThresholds:
    stopped_instances: int = 1     # alert if >= N stopped instances
    security_findings_high: int = 0  # alert if > N HIGH findings

@dataclass
class AppConfig:
    environment: str = "development"
    log_level: str = "INFO"
    aws_region: str = "us-east-1"
    aws_account_id: str = ""
    slack_webhook_url: str = ""
    prometheus_port: int = 9090
    scrape_interval_seconds: int = 30
    thresholds: AlertThresholds = field(default_factory=AlertThresholds)

def load_config() -> AppConfig:
    \"\"\"Load AppConfig from environment variables.\"\"\"
    return AppConfig(
        environment=os.environ.get("ENVIRONMENT", "development"),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
        aws_region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        aws_account_id=os.environ.get("AWS_ACCOUNT_ID", ""),
        slack_webhook_url=os.environ.get("SLACK_WEBHOOK_URL", ""),
        prometheus_port=int(os.environ.get("PROMETHEUS_PORT", "9090")),
        scrape_interval_seconds=int(os.environ.get("SCRAPE_INTERVAL", "30")),
    )
"""),

        md("## Step 4: Logging Module\n\n*Refer to: Lesson 1.5*"),

        code("""%%writefile ops-bot/src/ops_bot/logger.py
\"\"\"Structured logging for ops-bot.

Reference: https://www.structlog.org/en/stable/
\"\"\"
import os
import structlog

def configure_logging(level: str = "INFO") -> None:
    environment = os.environ.get("ENVIRONMENT", "development")
    procs = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.set_exc_info,
    ]
    if environment in ("production", "staging", "ci"):
        procs.append(structlog.processors.JSONRenderer())
    else:
        procs.append(structlog.dev.ConsoleRenderer())
    structlog.configure(
        processors=procs,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

def get_logger(name: str = "ops-bot", **ctx) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name).bind(**ctx)
"""),

        md("## Step 5: AWS Inventory Module\n\n*Refer to: Lessons 2.1 – 2.2*"),

        code("""%%writefile ops-bot/src/ops_bot/cloud/aws.py
\"\"\"AWS cloud inventory using boto3.

Reference:
  Quickstart:  https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html
  Paginators:  https://docs.aws.amazon.com/boto3/latest/guide/paginators.html
  EC2:         https://docs.aws.amazon.com/boto3/latest/guide/ec2-example-managing-instances.html
\"\"\"
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

class AWSInventory:
    \"\"\"EC2 and S3 inventory using boto3 with full pagination.\"\"\"

    def __init__(self, region: str | None = None, session: boto3.Session | None = None):
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self._session = session or boto3.Session(region_name=self.region)
        self._ec2 = self._session.client("ec2")
        self._s3  = self._session.client("s3")

    def list_ec2_instances(self, filters: list | None = None) -> list[dict]:
        \"\"\"List ALL EC2 instances using pagination.

        Uses get_paginator() so every page is fetched automatically.
        Reference: https://docs.aws.amazon.com/boto3/latest/guide/paginators.html
        \"\"\"
        paginator = self._ec2.get_paginator("describe_instances")
        kwargs = {"Filters": filters} if filters else {}
        instances = []
        for page in paginator.paginate(**kwargs):
            for r in page["Reservations"]:
                for inst in r["Instances"]:
                    tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
                    instances.append({
                        "instance_id": inst["InstanceId"],
                        "name":        tags.get("Name", "(unnamed)"),
                        "state":       inst["State"]["Name"],
                        "type":        inst.get("InstanceType", ""),
                        "private_ip":  inst.get("PrivateIpAddress", ""),
                        "tags":        tags,
                        "region":      self.region,
                    })
        return instances

    def list_s3_buckets(self) -> list[dict]:
        \"\"\"List all S3 buckets.\"\"\",
        r = self._s3.list_buckets()
        return [{"name": b["Name"],
                 "created": b["CreationDate"].isoformat()}
                for b in r.get("Buckets", [])]

    def get_stopped_instances(self) -> list[dict]:
        return [i for i in self.list_ec2_instances()
                if i["state"] not in ("running", "pending")]
"""),

        md("## Step 6: Security Scanner\n\n*Refer to: Lessons 4.1 – 4.2*"),

        code("""%%writefile ops-bot/src/ops_bot/security/scanner.py
\"\"\"SAST and dependency vulnerability scanning.

Reference:
  Bandit:    https://bandit.readthedocs.io/en/latest/
  pip-audit: https://pypi.org/project/pip-audit/
\"\"\"
import subprocess, json, re
from pathlib import Path

class OpsSecurityScanner:
    \"\"\"Runs Bandit SAST + pip-audit CVE scanning.\"\"\"

    def run_bandit(self, target: str) -> dict:
        \"\"\"Run Bandit SAST scanner and return parsed results.\"\"\",
        r = subprocess.run(
            ["bandit", "-r", "-ll", "-f", "json", target],
            capture_output=True, text=True,
        )
        try:
            raw = json.loads(r.stdout)
        except json.JSONDecodeError:
            return {"error": r.stderr, "total": 0, "high": 0, "issues": []}
        issues = raw.get("results", [])
        return {
            "total": len(issues),
            "high":  sum(1 for i in issues if i["issue_severity"] == "HIGH"),
            "medium":sum(1 for i in issues if i["issue_severity"] == "MEDIUM"),
            "issues": [{"id": i["test_id"], "severity": i["issue_severity"],
                        "text": i["issue_text"], "file": i["filename"],
                        "line": i["line_number"]} for i in issues],
        }

    def run_pip_audit(self, requirements_file: str | None = None) -> dict:
        \"\"\"Run pip-audit CVE scanner.\"\"\",
        cmd = ["pip-audit", "--format", "json", "--progress-spinner", "off"]
        if requirements_file:
            cmd.extend(["-r", requirements_file])
        r = subprocess.run(cmd, capture_output=True, text=True)
        try:
            raw = json.loads(r.stdout)
        except json.JSONDecodeError:
            return {"error": r.stderr, "cve_count": 0, "cves": []}
        cves = [{"pkg": d["name"], "ver": d["version"],
                 "id": v["id"], "fix": v.get("fix_versions", [])}
                for d in raw.get("dependencies", [])
                for v in d.get("vulns", [])]
        return {"cve_count": len(cves), "cves": cves}

    def has_blocking_issues(self, bandit: dict, audit: dict,
                            environment: str = "development") -> bool:
        \"\"\"Return True if findings should block a deployment.\"\"\",
        if environment == "development":
            return bool(bandit.get("high", 0) > 5 or audit.get("cve_count", 0) > 10)
        # staging / production: stricter
        return bool(bandit.get("high", 0) > 0 or audit.get("cve_count", 0) > 0)
"""),

        md("## Step 7: Prometheus Metrics Module\n\n*Refer to: Lesson 5.1*"),

        code("""%%writefile ops-bot/src/ops_bot/monitoring/metrics.py
\"\"\"Prometheus custom metrics for ops-bot.

Reference: https://github.com/prometheus/client_python
\"\"\"
import time
from prometheus_client import (
    Counter, Gauge, Histogram,
    CollectorRegistry, start_http_server,
)

class OpsMetrics:
    \"\"\"Defines and exposes Prometheus metrics for the ops platform.\"\"\",

    def __init__(self, port: int = 9090):
        self.port = port
        self.registry = CollectorRegistry()

        self.instances = Gauge(
            "ops_instances_total", "Cloud instances by provider/region/state.",
            ["provider", "region", "state"], registry=self.registry,
        )
        self.stopped = Gauge(
            "ops_stopped_instances", "Stopped instance count.",
            ["provider", "region"], registry=self.registry,
        )
        self.scans = Counter(
            "ops_scans_total", "Total inventory scans performed.",
            ["provider", "status"], registry=self.registry,
        )
        self.security = Gauge(
            "ops_security_findings", "Security findings by tool/severity.",
            ["tool", "severity"], registry=self.registry,
        )
        self.compliance = Gauge(
            "ops_compliance_score", "Compliance score (0-100).",
            ["account", "framework"], registry=self.registry,
        )

    def update_instance_metrics(self, instances: list[dict], provider: str = "aws") -> None:
        running = sum(1 for i in instances if i.get("state") == "running")
        stopped = sum(1 for i in instances if i.get("state") != "running")
        region  = instances[0]["region"] if instances else "unknown"
        self.instances.labels(provider=provider, region=region, state="running").set(running)
        self.instances.labels(provider=provider, region=region, state="stopped").set(stopped)
        self.stopped.labels(provider=provider, region=region).set(stopped)
        self.scans.labels(provider=provider, status="success").inc()

    def update_security_metrics(self, bandit: dict, audit: dict) -> None:
        self.security.labels(tool="bandit",    severity="HIGH").set(bandit.get("high", 0))
        self.security.labels(tool="pip-audit", severity="CVE").set(audit.get("cve_count", 0))

    def start_server(self) -> None:
        start_http_server(self.port, registry=self.registry)
        print(f"✓  Metrics server: http://0.0.0.0:{self.port}/metrics")
"""),

        md("## Step 8: Alerting Module\n\n*Refer to: Lesson 5.5*"),

        code("""%%writefile ops-bot/src/ops_bot/alerting/alerts.py
\"\"\"Slack webhook alerting with deduplication.

Reference: https://api.slack.com/messaging/webhooks
\"\"\"
import os, time, json, hashlib, requests

class OpsAlerter:
    def __init__(self, slack_webhook: str | None = None, dedup_seconds: int = 300):
        self.webhook = slack_webhook or os.environ.get("SLACK_WEBHOOK_URL", "")
        self.dedup_s = dedup_seconds
        self._fired: dict[str, float] = {}

    def _is_duplicate(self, key: str) -> bool:
        return time.time() - self._fired.get(key, 0) < self.dedup_s

    def send_slack(self, title: str, message: str, severity: str = "info",
                   fields: dict | None = None, alert_key: str | None = None) -> bool:
        key = alert_key or hashlib.md5(f"{title}{severity}".encode()).hexdigest()[:12]
        if self._is_duplicate(key):
            return False  # suppressed
        self._fired[key] = time.time()

        colors = {"info": "#2196F3", "warning": "#FF9800",
                  "error": "#F44336", "critical": "#9C27B0"}
        icons  = {"info": "ℹ️",  "warning": "⚠️", "error": "🔴", "critical": "🚨"}
        blocks = [
            {"type": "header", "text": {"type": "plain_text",
             "text": f"{icons.get(severity,'📣')} {title}"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        ]
        if fields:
            blocks.append({"type": "section",
                "fields": [{"type": "mrkdwn", "text": f"*{k}:* {v}"}
                            for k, v in fields.items()]})
        payload = {"text": f"[{severity.upper()}] {title}",
                   "attachments": [{"color": colors.get(severity, "#808080"),
                                    "blocks": blocks}]}
        if not self.webhook:
            print(f"[ALERT-SIM] {severity.upper()}: {title} | {message}")
            return True
        try:
            r = requests.post(self.webhook, json=payload, timeout=10)
            return r.status_code == 200
        except Exception:
            return False

    def check_and_alert(self, instances: list[dict], threshold: int = 1,
                        scan_result: dict | None = None) -> None:
        stopped = [i for i in instances if i.get("state") not in ("running", "pending")]
        if len(stopped) >= threshold:
            self.send_slack(
                title=f"{len(stopped)} EC2 instance(s) are stopped",
                message=f"Stopped instances detected in region {instances[0].get('region','?')}.",
                severity="warning" if len(stopped) < 5 else "error",
                fields={i["instance_id"]: i["name"] for i in stopped[:5]},
                alert_key=f"stopped-instances-{len(stopped)}",
            )
        if scan_result and scan_result.get("high", 0) > 0:
            self.send_slack(
                title=f"{scan_result['high']} HIGH severity security finding(s)",
                message="Bandit detected HIGH severity issues. Review before deploying.",
                severity="error",
                alert_key="bandit-high-findings",
            )
"""),

        md("## Step 9: Build the CLI\n\n*Refer to: Lesson 1.4*"),

        code('''%%writefile ops-bot/src/ops_bot/cli.py
"""ops-bot CLI — Ops Automation Platform.

Usage:
    python -m ops_bot.cli inventory
    python -m ops_bot.cli scan --target src/
    python -m ops_bot.cli report --output report.json
    python -m ops_bot.cli serve --port 9090
"""
import click, json, sys, os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

@click.group()
@click.option("--verbose", "-v", is_flag=True)
@click.option("--env", "-e", default=None,
              type=click.Choice(["development", "staging", "production"]))
@click.pass_context
def cli(ctx, verbose, env):
    """Ops Automation Platform CLI."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["env"] = env or os.environ.get("ENVIRONMENT", "development")

    # Initialise logging
    from ops_bot.logger import configure_logging
    configure_logging()

@cli.command()
@click.option("--region", "-r", default=None)
@click.option("--output", "-o", default="table",
              type=click.Choice(["table", "json"]))
@click.pass_context
def inventory(ctx, region, output):
    """List AWS EC2 instance inventory."""
    from ops_bot.cloud.aws import AWSInventory
    from ops_bot.logger import get_logger
    log = get_logger("inventory")

    log.info("inventory_started", region=region or "default")
    try:
        inv = AWSInventory(region=region)
        instances = inv.list_ec2_instances()
    except Exception as e:
        console.print(f"[red]✗ Failed to fetch inventory: {e}[/red]")
        console.print("[dim]  Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, or use aws configure.[/dim]")
        instances = []  # graceful degradation

    if output == "json":
        click.echo(json.dumps(instances, indent=2, default=str))
        return

    table = Table(title=f"EC2 Inventory ({region or 'all regions'})")
    table.add_column("Instance ID", style="dim")
    table.add_column("Name")
    table.add_column("State")
    table.add_column("Type")
    table.add_column("Region")
    for i in instances:
        state_fmt = f"[green]{i['state']}[/green]" if i["state"] == "running" else f"[yellow]{i['state']}[/yellow]"
        table.add_row(i["instance_id"], i["name"], state_fmt, i["type"], i.get("region", ""))
    console.print(table)

    stopped = sum(1 for i in instances if i["state"] != "running")
    console.print(Panel(
        f"[bold]{len(instances)}[/bold] instances | "
        f"[green]{len(instances)-stopped} running[/green] | "
        f"[yellow]{stopped} stopped[/yellow]",
        title="Summary", border_style="cyan"
    ))
    log.info("inventory_completed", total=len(instances), stopped=stopped)

@cli.command()
@click.option("--target", "-t", default=".", help="Directory to scan")
@click.option("--dockerfile", default=None)
@click.pass_context
def scan(ctx, target, dockerfile):
    """Run DevSecOps security scans (Bandit + pip-audit)."""
    from ops_bot.security.scanner import OpsSecurityScanner
    from ops_bot.logger import get_logger
    log = get_logger("scan")
    env = ctx.obj.get("env", "development")
    scanner = OpsSecurityScanner()

    console.print(f"[bold]Running security scan[/bold] on [cyan]{target}[/cyan]")
    bandit = scanner.run_bandit(target)
    audit  = scanner.run_pip_audit()
    log.info("scan_complete", bandit_issues=bandit["total"], cves=audit["cve_count"])

    if bandit["total"] > 0:
        console.print(f"  [red]Bandit: {bandit['total']} issues ({bandit['high']} HIGH)[/red]")
    else:
        console.print("  [green]✓ Bandit: no issues[/green]")

    if audit["cve_count"] > 0:
        console.print(f"  [red]pip-audit: {audit['cve_count']} CVE(s)[/red]")
    else:
        console.print("  [green]✓ pip-audit: no CVEs[/green]")

    if scanner.has_blocking_issues(bandit, audit, env):
        console.print("[bold red]✗ Security gate FAILED[/bold red]")
        sys.exit(1)
    console.print("[bold green]✓ Security gate PASSED[/bold green]")

@cli.command()
@click.option("--format", "fmt", default="json", type=click.Choice(["json", "markdown"]))
@click.option("--output", default="report.json")
@click.pass_context
def report(ctx, fmt, output):
    """Run full ops report: inventory + scan + metrics + alerts."""
    import json
    from pathlib import Path
    from ops_bot.cloud.aws import AWSInventory
    from ops_bot.security.scanner import OpsSecurityScanner
    from ops_bot.monitoring.metrics import OpsMetrics
    from ops_bot.alerting.alerts import OpsAlerter
    from ops_bot.config import load_config
    from ops_bot.logger import get_logger

    cfg     = load_config()
    log     = get_logger("report", env=cfg.environment)
    metrics = OpsMetrics(port=cfg.prometheus_port)
    alerter = OpsAlerter(slack_webhook=cfg.slack_webhook_url)

    log.info("report_started")
    console.print("[bold]Ops Automation Platform — Full Report[/bold]")

    # Inventory
    console.print("\\n[cyan]1. Cloud Inventory[/cyan]")
    try:
        inv = AWSInventory(region=cfg.aws_region)
        instances = inv.list_ec2_instances()
        metrics.update_instance_metrics(instances)
        console.print(f"   {len(instances)} instances found")
    except Exception as e:
        log.error("inventory_failed", error=str(e))
        instances = []

    # Security scan
    console.print("\\n[cyan]2. Security Scan[/cyan]")
    scanner = OpsSecurityScanner()
    bandit  = scanner.run_bandit(".")
    audit   = scanner.run_pip_audit()
    metrics.update_security_metrics(bandit, audit)
    console.print(f"   Bandit: {bandit['high']} HIGH  | pip-audit: {audit['cve_count']} CVEs")

    # Alerts
    console.print("\\n[cyan]3. Alerts[/cyan]")
    alerter.check_and_alert(instances, threshold=cfg.thresholds.stopped_instances,
                            scan_result=bandit)

    # Save report
    report_data = {
        "environment": cfg.environment,
        "instances": instances,
        "security": {"bandit": bandit, "pip_audit": audit},
    }
    Path(output).write_text(json.dumps(report_data, indent=2, default=str))
    console.print(f"\\n[green]✓ Report saved: {output}[/green]")
    log.info("report_completed", output=output)

@cli.command()
@click.option("--port", default=9090, type=int)
@click.pass_context
def serve(ctx, port):
    """Start Prometheus metrics exporter."""
    import time
    from ops_bot.monitoring.metrics import OpsMetrics
    from ops_bot.cloud.aws import AWSInventory
    from ops_bot.security.scanner import OpsSecurityScanner
    from ops_bot.config import load_config

    cfg     = load_config()
    metrics = OpsMetrics(port=port)
    metrics.start_server()
    console.print(f"[bold]Collecting metrics every {cfg.scrape_interval_seconds}s...[/bold]")

    while True:
        try:
            inv = AWSInventory(region=cfg.aws_region)
            metrics.update_instance_metrics(inv.list_ec2_instances())
        except Exception:
            pass
        time.sleep(cfg.scrape_interval_seconds)

if __name__ == "__main__":
    cli()
'''),

        md("## Step 10: Tests"),

        code("""%%writefile ops-bot/tests/test_ops_bot.py
\"\"\"Unit tests for ops-bot.\"\"\"
import pytest, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_config_loads_defaults():
    from ops_bot.config import load_config
    cfg = load_config()
    assert cfg.environment in ("development", "staging", "production")
    assert cfg.prometheus_port > 0
    assert cfg.scrape_interval_seconds > 0
    print(f"✓ config loaded: {cfg.environment}")

def test_alerter_deduplication():
    from ops_bot.alerting.alerts import OpsAlerter
    alerter = OpsAlerter(slack_webhook=None, dedup_seconds=60)
    r1 = alerter.send_slack("Test", "message", alert_key="test-key-001")
    r2 = alerter.send_slack("Test", "message", alert_key="test-key-001")
    assert r1 is True
    assert r2 is False   # deduplicated
    print("✓ deduplication works")

def test_security_scanner_blocking():
    from ops_bot.security.scanner import OpsSecurityScanner
    scanner = OpsSecurityScanner()
    # 0 issues + 0 CVEs should never block
    ok = not scanner.has_blocking_issues(
        {"high": 0, "total": 0},
        {"cve_count": 0},
        environment="production",
    )
    assert ok
    # 1 HIGH in production should block
    blocked = scanner.has_blocking_issues(
        {"high": 1, "total": 1},
        {"cve_count": 0},
        environment="production",
    )
    assert blocked
    print("✓ security gate thresholds correct")

if __name__ == "__main__":
    test_config_loads_defaults()
    test_alerter_deduplication()
    test_security_scanner_blocking()
    print("\\nAll basic tests passed.")
"""),

        code("""# Run the tests
import subprocess, sys
r = subprocess.run(
    [sys.executable, "-m", "pytest", "ops-bot/tests/", "-v", "--tb=short"],
    capture_output=True, text=True,
    cwd="."
)
print(r.stdout)
if r.returncode == 0:
    print("\\n✅  All tests passed!")
else:
    print("\\n⚠   Some tests may be failing — implement the TODO stubs above.")"""),

        md("## Step 11: Dockerfile"),

        code("""%%writefile ops-bot/Dockerfile
# ops-bot — Security-hardened multi-stage Dockerfile
# Reference: https://docs.docker.com/develop/security-best-practices/

# ── Stage 1: build dependencies ─────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ── Stage 2: runtime ────────────────────────────────────────────────────
FROM python:3.11-slim

# Create a non-root user (CIS Docker Benchmark — no root in containers)
RUN groupadd -r opsbot && useradd -r -g opsbot -s /sbin/nologin opsbot

WORKDIR /app
COPY --from=builder /root/.local /home/opsbot/.local
COPY src/ ./src/

RUN chown -R opsbot:opsbot /app
USER opsbot

EXPOSE 9090

# Health check: poll the /metrics endpoint every 30s
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \\\\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9090/metrics')" || exit 1

ENV PYTHONPATH=/app/src
CMD ["python", "-m", "ops_bot.cli", "serve"]
"""),

        md("## Step 12: docker-compose.yml"),

        code("""%%writefile ops-bot/docker-compose.yml
version: '3.8'

services:
  ops-bot:
    build: .
    ports:
      - "9090:9090"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=INFO
      - AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-us-east-1}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-}
      - SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL:-}
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9091:9090"
    volumes:
      - ./configs/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=ops-admin
    volumes:
      - grafana-data:/var/lib/grafana
    restart: unless-stopped
    depends_on:
      - prometheus

volumes:
  grafana-data:
"""),

        code("""(Path("ops-bot/configs")).mkdir(exist_ok=True)
(Path("ops-bot/configs/prometheus.yml")).write_text(
    "global:\\n  scrape_interval: 30s\\n\\n"
    "scrape_configs:\\n"
    "  - job_name: ops-bot\\n"
    "    static_configs:\\n"
    "      - targets: [ops-bot:9090]\\n"
)
print("✓ prometheus.yml written")"""),

        md("""## Verification Checklist

Mark each item complete before tackling stretch goals:

- [ ] **Step 1:** Project structure with all dirs and `__init__.py` files
- [ ] **Step 2:** `requirements.txt` written and all deps installable
- [ ] **Step 3:** `config.py` — `AppConfig` loads from env vars
- [ ] **Step 4:** `logger.py` — `configure_logging()` and `get_logger()` work
- [ ] **Step 5:** `cloud/aws.py` — `AWSInventory` uses `get_paginator()`
- [ ] **Step 6:** `security/scanner.py` — bandit + pip-audit + blocking logic
- [ ] **Step 7:** `monitoring/metrics.py` — Prometheus metrics defined + HTTP server starts
- [ ] **Step 8:** `alerting/alerts.py` — Slack alerts with deduplication
- [ ] **Step 9:** `cli.py` — all 4 sub-commands work
- [ ] **Step 10:** 3+ unit tests pass with `pytest`
- [ ] **Step 11:** Dockerfile builds without errors
- [ ] **Step 12:** `docker-compose up` starts ops-bot + Prometheus + Grafana"""),

        md("""## Stretch Goals

### 1. Multi-Cloud Inventory (Phase 2)
Extend `inventory` to include Azure VMs and GCP instances using the adapter pattern from Lesson 2.5.

### 2. GitOps Integration (Phase 3)
Add `ops-bot deploy` that updates a Helm values file and opens a GitHub PR.

### 3. Full DevSecOps CI/CD Pipeline (Phase 4)
Add a GitHub Actions workflow that runs `ops-bot scan` on every PR and fails
on HIGH findings.

### 4. Distributed Tracing (Phase 5)
Instrument `ops-bot` commands with OpenTelemetry spans (Lesson 5.2) and add
Jaeger to `docker-compose.yml`.

### 5. Grafana Dashboard Auto-Provisioning
Use the Grafana API (Lesson 5.6) to deploy the ops dashboard on startup.

---

**Congratulations on completing the Python for CloudOps + DevOps + DevSecOps + Monitoring study plan!**"""),
    ]
    save(notebook(cells), BASE / "capstone" / "capstone-project.ipynb")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating notebooks grounded in official documentation...")
    print()

    print("Phase 1 — Python Automation Foundations")
    lesson_1_1()
    lesson_1_2()
    lesson_1_3()
    lesson_1_4()
    lesson_1_5()

    print("\nPhase 2 — Cloud Automation (CloudOps)")
    lesson_2_1()
    lesson_2_2()

    print("\nPhase 2 (remaining) + Phases 3–5 — structured stubs")
    generate_remaining()

    print("\nPhase 5 — Monitoring (Prometheus custom metrics — full lesson)")
    lesson_5_1()

    print("\nCapstone")
    capstone()

    print("\n✓  All notebooks generated.")
    print(f"   Location: {BASE}")
