# Install Luna with HACS

HACS is the supported installation and update method. The repository must be public because HACS does not support private repositories.

1. In HACS, add `HenkTechLab/Luna` as a custom repository of type **Integration**.
2. Download Luna and restart Home Assistant.
3. Go to **Settings → Devices & services → Add integration**, add **Luna**, and choose the Native or Custom dashboard.
4. Register the package files and the selected dashboard in `configuration.yaml` using the exact blocks in the root [installation guide](../../INSTALLATIE.md).
5. Validate the Home Assistant configuration and restart only when it is valid.

The Native dashboard uses built-in Home Assistant cards. The Custom dashboard requires Mushroom and card-mod, installed separately through HACS.

For updates, update Luna in HACS, validate the configuration, and restart Home Assistant. HACS manages the Python integration, packages, language modules, and both dashboard variants together. No shell, curl, or separate installer is used.

