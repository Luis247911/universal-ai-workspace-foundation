"""Config/suite loader with optional-PyYAML handling and a JSON fallback.

YAML is nicer for humans but PyYAML is an optional extra. Loading a .yaml file without
PyYAML installed falls back to a sibling .json twin if present, otherwise raises a clear
ConfigError telling the user how to proceed. This keeps a bare `pip install` runnable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import ConfigError


def load_config(path) -> Any:
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"Config file not found: {p}")
    if p.suffix == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    if p.suffix in (".yaml", ".yml"):
        try:
            import yaml  # optional extra: pip install "uaw-harness[yaml]"
        except ImportError:
            twin = p.with_suffix(".json")
            if twin.exists():
                return json.loads(twin.read_text(encoding="utf-8"))
            raise ConfigError(
                f"PyYAML not installed and no JSON twin for {p.name}. "
                f"Install the extra (pip install 'uaw-harness[yaml]') or provide {twin.name}."
            ) from None
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    raise ConfigError(f"Unsupported config suffix '{p.suffix}': {p}")
