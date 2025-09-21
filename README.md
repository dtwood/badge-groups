# badge-groups

## Installation
This app is a Python package, which can either be installed from pre-built packages, or run in a local checkout of the
repository.

### Installing pre-built packages
The pre-built artifacts on GitHub can be installed by running the following command:
``` sh
pip3 install https://github.com/dtwood/badge-groups/releases/download/v0.1.0/badge_groups-0.1.0-py3-none-any.whl
```

You can then run against a list of badge preferences (saved as `demo-data.csv`) by running the command `badge-groups`.

### Running in a local checkout
The simplest way to run against a local checkout of the source is using the `uv` tool (https://docs.astral.sh/uv/).
Check out the git repository, then run `uv run badge-groups` to automatically set up a Python virtual environment
inside your checkout, install all dependencies and build and run the Python script. You can also run dev tools against
the checkout, for example with `uv run pytest` to run the unit tests, `uv run ruff format` to automatically format
your changes, or `uv run ruff lint` to run the linter.