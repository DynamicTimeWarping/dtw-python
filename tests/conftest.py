from __future__ import annotations

import os
import sys
from pathlib import Path


def _ensure_meson_editable_skip() -> None:
    build_path = Path(__file__).resolve().parent.parent / "build" / f"cp{sys.version_info.major}{sys.version_info.minor}"
    existing = os.environ.get("MESONPY_EDITABLE_SKIP", "")
    paths = [p for p in existing.split(os.pathsep) if p]
    path_str = str(build_path)
    if path_str not in paths:
        paths.append(path_str)
        os.environ["MESONPY_EDITABLE_SKIP"] = os.pathsep.join(paths)


_ensure_meson_editable_skip()
