# Luna - Home Assistant installation guide

## One command

Open the **Terminal & SSH App** in Home Assistant.

Native dashboard with no extra frontend dependencies:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- en native
```

Custom dashboard with Mushroom and card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- en custom
```

The custom variant requires **Mushroom** and **card-mod** through HACS.

## Installer

The installer downloads Luna, creates a backup, installs packages, languages, documentation, exports and both dashboard files under `/config/luna`. Existing `automations.yaml` and `scripts.yaml` are not overwritten.

If `configuration.yaml` still needs registration, the installer prints the exact missing block. Internal `.storage` files are not modified.

## Dashboards

- `luna-dashboard-native.yaml` - modern standard Home Assistant cards.
- `luna-dashboard-custom.yaml` - richer interface using Mushroom and card-mod.

## Verification

1. Validate the Home Assistant configuration.
2. Do not restart when a configuration error exists.
3. Restart after successful validation.
4. Open Luna from the sidebar.
5. Verify `input_select.luna_language_taal` and select the required language.

## Safety

Physical control, planner execution, self-recovery and local AI remain fail-closed until the user deliberately configures them.
