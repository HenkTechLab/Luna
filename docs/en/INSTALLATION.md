# Luna - Home Assistant installation guide

## One-command installation

Open the Home Assistant Terminal & SSH App and run:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- en
```

No repository clone is required. The installer downloads Luna, creates a backup and installs the files under `/config/luna`.

## What is installed

- Luna packages and all seven language modules
- documentation
- sanitized exports/reference material
- the Luna dashboard YAML based on the Luna Test dashboard

Existing `automations.yaml` and `scripts.yaml` are never blindly overwritten. `luna_test_*` remains disabled reference/test material.

## Package registration

If Luna packages are not registered yet, the installer prints the exact block that must be added under the existing `homeassistant:` -> `packages:` section. Never create a second `homeassistant:` section.

## Dashboard

The installer places the dashboard at:

```text
/config/luna/dashboard/luna-dashboard.yaml
```

For safety the installer does not edit Home Assistant's internal `.storage` files. If the dashboard is not registered yet, it prints the exact `lovelace:` registration block. After registration and a valid restart, **Luna** appears in the sidebar.

## Verification

1. Validate the Home Assistant configuration.
2. Do not restart if validation reports an error.
3. Restart after successful validation.
4. Open the Luna dashboard.
5. Verify `input_select.luna_language_taal` and select the required language.

## Safety

Physical control, planner execution, self-recovery and local AI remain fail-closed until deliberately configured. Local AI is optional.
