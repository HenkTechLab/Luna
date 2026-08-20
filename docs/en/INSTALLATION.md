# Luna - Home Assistant installation guide

## Safe installation

Luna is fail-closed by default. Physical control, planner execution, self-recovery and local AI inference remain disabled until the user deliberately configures them.

## Requirements

- Working Home Assistant installation
- Access to `/config`
- Access to `configuration.yaml`
- A recent Home Assistant backup

## Installation

Copy the repository to the Home Assistant system or run:

```sh
sh install_luna.sh en
```

The installer copies Luna to `/config/luna`, creates a backup of relevant existing files and never blindly overwrites existing `automations.yaml` or `scripts.yaml`.

Add these entries under the existing `homeassistant:` -> `packages:` section when the installer reports that manual configuration is required:

```yaml
    luna: !include luna/packages/luna.yaml
    luna_modules: !include luna/packages/luna_modules.yaml
    luna_advanced_modules: !include luna/packages/luna_advanced_modules.yaml
    luna_nederlands: !include luna/packages/languages/nederlands.yaml
    luna_english: !include luna/packages/languages/english.yaml
    luna_deutsch: !include luna/packages/languages/deutsch.yaml
    luna_francais: !include luna/packages/languages/francais.yaml
    luna_espanol: !include luna/packages/languages/espanol.yaml
    luna_italiano: !include luna/packages/languages/italiano.yaml
    luna_portugues: !include luna/packages/languages/portugues.yaml
```

Do not create a second `homeassistant:` section.

## Automations, helpers, scripts and Luna Test

`/config/luna/exports` contains sanitized source/reference exports for automations, helpers and scripts, including `luna_test_*` material. These files are deliberately **not activated automatically**. They must not be blindly merged into an existing Home Assistant installation.

The supported safe installation layer is `/config/luna/packages`.

## Verification

1. Validate the Home Assistant configuration.
2. Do not restart while validation reports an error.
3. Restart Home Assistant after successful validation.
4. Open Developer Tools -> States and search for `luna`.
5. Verify `input_select.luna_language_taal`.
6. Select the required language.

## Local AI

Local AI is optional. First verify Luna without AI. Configure the local backend only afterwards and select the local mode through `input_select.luna_ai_mode`.

## Important

Install and verify Luna first. Only then configure devices, planner execution, self-recovery or local AI.