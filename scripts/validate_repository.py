"""Validate the HACS-facing Luna repository layout."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "luna"

RESOURCE_PAIRS = {
    ROOT / "dashboard" / "luna-dashboard-native.yaml": INTEGRATION
    / "resources"
    / "dashboard"
    / "luna-dashboard-native.yaml",
    ROOT / "dashboard" / "luna-dashboard-custom.yaml": INTEGRATION
    / "resources"
    / "dashboard"
    / "luna-dashboard-custom.yaml",
    ROOT / "packages" / "luna.yaml": INTEGRATION
    / "resources"
    / "packages"
    / "luna.yaml",
    ROOT / "packages" / "luna_modules.yaml": INTEGRATION
    / "resources"
    / "packages"
    / "luna_modules.yaml",
    ROOT / "packages" / "luna_advanced_modules.yaml": INTEGRATION
    / "resources"
    / "packages"
    / "luna_advanced_modules.yaml",
}

for language_file in (ROOT / "packages" / "languages").glob("*.yaml"):
    RESOURCE_PAIRS[language_file] = (
        INTEGRATION / "resources" / "packages" / "languages" / language_file.name
    )


def validate() -> None:
    """Run repository consistency checks."""
    required = [
        ROOT / "README.md",
        ROOT / "INSTALLATIE.md",
        ROOT / "hacs.json",
        INTEGRATION / "manifest.json",
        INTEGRATION / "__init__.py",
        INTEGRATION / "config_flow.py",
        INTEGRATION / "strings.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise ValueError(f"Missing required files: {', '.join(missing)}")

    if (ROOT / "install_luna.sh").exists():
        raise ValueError("The retired shell installer must not be present")

    for json_file in [ROOT / "hacs.json", *INTEGRATION.rglob("*.json")]:
        with json_file.open(encoding="utf-8") as handle:
            json.load(handle)

    manifest = json.loads((INTEGRATION / "manifest.json").read_text(encoding="utf-8"))
    required_manifest_keys = {
        "domain",
        "name",
        "codeowners",
        "config_flow",
        "documentation",
        "integration_type",
        "issue_tracker",
        "version",
    }
    missing_manifest = required_manifest_keys - manifest.keys()
    if missing_manifest:
        raise ValueError(f"Manifest keys missing: {sorted(missing_manifest)}")
    if manifest["domain"] != "luna" or manifest["config_flow"] is not True:
        raise ValueError("The Luna manifest domain/config_flow is invalid")

    for python_file in INTEGRATION.rglob("*.py"):
        ast.parse(python_file.read_text(encoding="utf-8"), filename=str(python_file))

    for source, managed in RESOURCE_PAIRS.items():
        if not managed.is_file():
            raise ValueError(f"Managed resource is missing: {managed.relative_to(ROOT)}")
        if source.read_bytes() != managed.read_bytes():
            raise ValueError(
                f"Managed resource differs from source: {managed.relative_to(ROOT)}"
            )

    documentation = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [ROOT / "README.md", ROOT / "INSTALLATIE.md", *ROOT.glob("docs/**/*.md")]
    ).lower()
    forbidden = ["install_luna.sh", "raw.githubusercontent.com/henktechlab/luna"]
    found = [term for term in forbidden if term in documentation]
    if found:
        raise ValueError(f"Retired installer references found: {', '.join(found)}")


if __name__ == "__main__":
    validate()
    print("Luna repository validation passed")

