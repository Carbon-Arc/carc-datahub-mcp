#!/usr/bin/env python3
"""Auto-install launcher for mcp-server-datahub.

On first run:
1. Installs uv via pip (fast package manager)
2. Uses uv sync to install dependencies from uv.lock
3. Creates a marker file to skip setup on subsequent runs

Subsequent runs use the cached .venv for instant startup.
"""
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
VENV_DIR = SCRIPT_DIR / ".venv"
MARKER = VENV_DIR / ".installed"


def setup_environment():
    """Install uv and sync dependencies on first run."""
    if MARKER.exists():
        return

    print("First run: setting up environment...", file=sys.stderr)

    # Install uv using pip (into user site-packages to avoid permission issues)
    print("Installing uv package manager...", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "--quiet", "uv"],
        check=True,
    )

    # Use uv sync to create venv and install deps from uv.lock (fast!)
    # Constrain Python version to avoid 3.14+ which lacks pre-built wheels for many packages
    print("Installing dependencies with uv...", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "uv", "sync", "--python", ">=3.10,<3.14", "--directory", str(SCRIPT_DIR)],
        check=True,
    )

    # Mark as installed
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.touch()
    print("Setup complete!", file=sys.stderr)


def main():
    setup_environment()

    # Run the MCP server using the venv python
    python = VENV_DIR / ("Scripts" if sys.platform == "win32" else "bin") / "python"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SCRIPT_DIR / "src")

    # Use execve to replace process (Unix) or subprocess (Windows)
    args = [str(python), "-m", "mcp_server_datahub"] + sys.argv[1:]
    if sys.platform == "win32":
        sys.exit(subprocess.call(args, env=env))
    else:
        os.execve(str(python), args, env)


if __name__ == "__main__":
    main()
