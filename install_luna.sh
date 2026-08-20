#!/bin/sh
set -eu

# Luna one-command multilingual installer for Home Assistant
# Direct use:
# curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl

REPO_ZIP="https://github.com/HenkTechLab/Luna/archive/refs/heads/main.zip"
HA_CONFIG="${HA_CONFIG:-/config}"
LANG_CODE="${1:-en}"
WORKDIR="${TMPDIR:-/tmp}/luna-install-$$"
BACKUP_DIR="$HA_CONFIG/luna_backup_$(date +%Y%m%d_%H%M%S)"
LUNA_DIR="$HA_CONFIG/luna"

case "$LANG_CODE" in
 nl) TITLE="Luna installatie"; DONE="Klaar";; de) TITLE="Luna Installation"; DONE="Fertig";; fr) TITLE="Installation Luna"; DONE="Terminé";; es) TITLE="Instalación Luna"; DONE="Terminado";; it) TITLE="Installazione Luna"; DONE="Completato";; pt) TITLE="Instalação Luna"; DONE="Concluído";; en|*) LANG_CODE="en"; TITLE="Luna installation"; DONE="Done";;
esac

cleanup(){ rm -rf "$WORKDIR"; }
trap cleanup EXIT INT TERM

[ -d "$HA_CONFIG" ] || { echo "ERROR: Home Assistant config directory not found: $HA_CONFIG"; exit 1; }
mkdir -p "$WORKDIR" "$BACKUP_DIR"

echo "=== $TITLE ==="
echo "[1/7] Download..."
if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$REPO_ZIP" -o "$WORKDIR/luna.zip"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$WORKDIR/luna.zip" "$REPO_ZIP"
else
  echo "ERROR: curl or wget is required."
  exit 1
fi

command -v unzip >/dev/null 2>&1 || { echo "ERROR: unzip is required."; exit 1; }
unzip -q "$WORKDIR/luna.zip" -d "$WORKDIR"
SRC="$WORKDIR/Luna-main"
[ -f "$SRC/packages/luna.yaml" ] || { echo "ERROR: Luna package missing."; exit 1; }

echo "[2/7] Backup..."
for f in configuration.yaml automations.yaml scripts.yaml; do [ ! -f "$HA_CONFIG/$f" ] || cp -p "$HA_CONFIG/$f" "$BACKUP_DIR/$f"; done
[ ! -d "$LUNA_DIR" ] || cp -R "$LUNA_DIR" "$BACKUP_DIR/luna"

echo "[3/7] Install files..."
rm -rf "$LUNA_DIR.new"; mkdir -p "$LUNA_DIR.new"
cp -R "$SRC/packages" "$LUNA_DIR.new/packages"
[ ! -d "$SRC/exports" ] || cp -R "$SRC/exports" "$LUNA_DIR.new/exports"
[ ! -d "$SRC/docs" ] || cp -R "$SRC/docs" "$LUNA_DIR.new/docs"
[ ! -d "$SRC/dashboard" ] || cp -R "$SRC/dashboard" "$LUNA_DIR.new/dashboard"
rm -rf "$LUNA_DIR"; mv "$LUNA_DIR.new" "$LUNA_DIR"

echo "[4/7] Check package registration..."
CONFIG="$HA_CONFIG/configuration.yaml"
NEED_MANUAL=1
[ -f "$CONFIG" ] && grep -q 'luna/packages/luna.yaml' "$CONFIG" && NEED_MANUAL=0

PACKAGE_BLOCK='    luna: !include luna/packages/luna.yaml
    luna_modules: !include luna/packages/luna_modules.yaml
    luna_advanced_modules: !include luna/packages/luna_advanced_modules.yaml
    luna_nederlands: !include luna/packages/languages/nederlands.yaml
    luna_english: !include luna/packages/languages/english.yaml
    luna_deutsch: !include luna/packages/languages/deutsch.yaml
    luna_francais: !include luna/packages/languages/francais.yaml
    luna_espanol: !include luna/packages/languages/espanol.yaml
    luna_italiano: !include luna/packages/languages/italiano.yaml
    luna_portugues: !include luna/packages/languages/portugues.yaml'

echo "[5/7] Dashboard..."
# Dashboard is installed as YAML because directly editing Home Assistant .storage is unsafe.
# Registration is printed for manual insertion if not already present.
DASHBOARD_BLOCK='lovelace:
  dashboards:
    luna-dashboard:
      mode: yaml
      title: Luna
      icon: mdi:robot
      show_in_sidebar: true
      filename: luna/dashboard/luna-dashboard.yaml'
DASHBOARD_REGISTERED=0
[ -f "$CONFIG" ] && grep -q 'filename: luna/dashboard/luna-dashboard.yaml' "$CONFIG" && DASHBOARD_REGISTERED=1

echo "[6/7] Safety..."
echo "exports/luna_test_* are reference/test material and are NOT automatically activated."
echo "Existing automations.yaml and scripts.yaml are NOT overwritten."

echo "[7/7] $DONE."
echo "Backup: $BACKUP_DIR"
if [ "$NEED_MANUAL" -eq 1 ]; then
  echo ""
  echo "PACKAGE REGISTRATION REQUIRED under the existing homeassistant: -> packages:"
  printf '%s\n' "$PACKAGE_BLOCK"
fi
if [ "$DASHBOARD_REGISTERED" -eq 0 ]; then
  echo ""
  echo "DASHBOARD REGISTRATION REQUIRED in configuration.yaml:"
  printf '%s\n' "$DASHBOARD_BLOCK"
fi

echo ""
echo "Validate Home Assistant configuration before restarting."
echo "Dashboard file: $LUNA_DIR/dashboard/luna-dashboard.yaml"
echo "Documentation: $LUNA_DIR/docs/$LANG_CODE"
