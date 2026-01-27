## Developing

### Setup

Requires [`uv`](https://docs.astral.sh/uv/) - see the [project README](README.md) for installation instructions.

```bash
make setup

# <authentication is the same as in production>
```

### Run using the MCP inspector

```bash
npx -y @modelcontextprotocol/inspector@latest

# In the UI, select "STDIO" and put in
# command: <full-path-to-uv>
# args: --directory path/to/mcp-server-datahub run mcp-server-datahub
```

### Run using an MCP client

Use this configuration in your MCP client e.g. Claude Desktop, Cursor, etc.

```js
{
  "mcpServers": {
    "datahub": {
      "command": "<full-path-to-uv>",  // e.g. /Users/hsheth/.local/bin/uv
      "args": [
        "--directory",
        "path/to/mcp-server-datahub",  // update this with an absolute path
        "run",
        "mcp-server-datahub"
      ],
      "env": {  // required if ~/.datahubenv does not exist
        "DATAHUB_GMS_URL": "<your-datahub-url>",
        "DATAHUB_GMS_TOKEN": "<your-datahub-token>"
      }
    }
  }
}
```

### Run linting

```bash
# Check linting
make lint-check

# Fix linting
make lint
```

### Run tests

The test suite is currently very simplistic, and requires a live DataHub instance.

```bash
make test
```

## Building the MCPB Bundle

The `.mcpb` file is a zip archive that can be installed in Claude Desktop as an extension.

### Prerequisites

- Ensure `uv.lock` exists and is up to date (`uv lock` if needed)
- Update the version in `manifest.json` if releasing a new version

### Build Steps

```bash
# 1. Get the version from manifest.json
VERSION=$(python3 -c "import json; print(json.load(open('manifest.json'))['version'])")

# 2. Create the bundle (zip with .mcpb extension)
zip -r "carc-datahub-mcp-v${VERSION}.mcpb" . -x@.mcpbignore

# 3. Verify the bundle contains uv.lock (required for fast startup)
unzip -l "carc-datahub-mcp-v${VERSION}.mcpb" | grep uv.lock
```

### Important Notes

- **Always include `uv.lock`** in the bundle. Without it, `uv run` must resolve all dependencies on first launch, causing a timeout/disconnect in Claude Desktop.
- The `.mcpbignore` file controls what's excluded from the bundle (similar to `.gitignore`)
- Test the bundle by installing it in Claude Desktop before distributing

### Installing in Claude Desktop

Double-click the `.mcpb` file or drag it into Claude Desktop to install.

## Publishing

We use setuptools-scm to manage the version number.

CI will automatically publish a new release to PyPI when a GitHub release is created.
