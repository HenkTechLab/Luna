#!/bin/sh
set -eu

# Luna installer for Home Assistant
# Installs the safe package layer. Export/test material is copied separately
# and is never merged blindly into an existing Home Assistant configuration.

REPO_URL="https://github.com/HenkTechLab/Luna.git"
HA_CONFIG="${HA_CONFIG:-/config}"
WORKDIR="${TMPDIR:-/tmp}/luna-install-$$"
BACKUP_DIR="$HA_CONFIG/luna_backup_$(date +%Y%m%d_%H%M%S)"
LUNA_DIR="$HA_CONFIG/luna"

cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT INT TERM

echo "=========================================="
echo " Luna installer voor Home Assistant"
echo "=========================================="
echo
echo "Doelmap: $HA_CONFIG"

if [ ! -d "$HA_CONFIG" ]; then
  echo "FOUT: Home Assistant-configuratiemap bestaat niet: $HA_CONFIG"
  echo "Gebruik bijvoorbeeld: HA_CONFIG=/config sh install_luna.sh"
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "FOUT: git is niet beschikbaar."
  echo "Download de Luna-repository handmatig of voer dit script uit in een omgeving met git."
  exit 1
fi

mkdir -p "$WORKDIR"
echo "[1/7] Luna downloaden..."
git clone --depth 1 "$REPO_URL" "$WORKDIR/repo"

for required in packages/luna.yaml packages/luna_modules.yaml packages/luna_advanced_modules.yaml; do
  if [ ! -f "$WORKDIR/repo/$required" ]; then
    echo "FOUT: verplicht Luna-bestand ontbreekt: $required"
    exit 1
  fi
done

echo "[2/7] Back-up maken..."
mkdir -p "$BACKUP_DIR"
for f in configuration.yaml automations.yaml scripts.yaml; do
  if [ -f "$HA_CONFIG/$f" ]; then
    cp -p "$HA_CONFIG/$f" "$BACKUP_DIR/$f"
  fi
done
if [ -d "$LUNA_DIR" ]; then
  cp -R "$LUNA_DIR" "$BACKUP_DIR/luna"
fi

echo "Back-up: $BACKUP_DIR"

echo "[3/7] Luna-bestanden installeren..."
rm -rf "$LUNA_DIR.new"
mkdir -p "$LUNA_DIR.new"
cp -R "$WORKDIR/repo/packages" "$LUNA_DIR.new/packages"

# exports bevat geschoonde bronlogica, inclusief luna_test-bestanden.
# Bewaar dit als referentie/importmateriaal, maar laad het NIET automatisch.
if [ -d "$WORKDIR/repo/exports" ]; then
  cp -R "$WORKDIR/repo/exports" "$LUNA_DIR.new/exports"
fi

rm -rf "$LUNA_DIR"
mv "$LUNA_DIR.new" "$LUNA_DIR"

echo "[4/7] configuration.yaml controleren..."
CONFIG="$HA_CONFIG/configuration.yaml"
if [ ! -f "$CONFIG" ]; then
  echo "WAARSCHUWING: configuration.yaml niet gevonden."
  NEED_MANUAL=1
else
  NEED_MANUAL=0
fi

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

if [ "$NEED_MANUAL" -eq 0 ]; then
  if grep -q 'luna/packages/luna.yaml' "$CONFIG"; then
    echo "Luna package-includes zijn al aanwezig; configuration.yaml blijft ongewijzigd."
  else
    echo "LET OP: bestaande configuration.yaml wordt niet automatisch herschreven."
    echo "Dit voorkomt beschadiging van bestaande YAML-structuur."
    NEED_MANUAL=1
  fi
fi

echo "[5/7] Automations, scripts en helpers controleren..."
echo "De map $LUNA_DIR/exports bevat automations, scripts en helpers uit de geschoonde bronexport."
echo "Deze worden bewust NIET blind toegevoegd aan automations.yaml/scripts.yaml."
echo "Ook luna_test_* exportbestanden worden NIET automatisch geactiveerd."
echo "De veilige, installeerbare Luna-laag staat onder $LUNA_DIR/packages."

echo "[6/7] Installatieoverzicht maken..."
cat > "$LUNA_DIR/INSTALLATIE_STATUS.txt" <<EOF
Luna bestanden gekopieerd naar:
$LUNA_DIR

Back-up:
$BACKUP_DIR

Veilige packages:
$LUNA_DIR/packages

Geschoonde export/reference inclusief automations, helpers, scripts en luna_test_*:
$LUNA_DIR/exports

BELANGRIJK:
- exports worden niet automatisch geactiveerd;
- luna_test_* wordt niet automatisch geactiveerd;
- bestaande automations.yaml en scripts.yaml zijn niet overschreven;
- Home Assistant is niet automatisch herstart.
EOF

echo "[7/7] Klaar."
echo
if [ "$NEED_MANUAL" -eq 1 ]; then
  echo "Voeg onderstaande regels handmatig toe onder homeassistant: -> packages:"
  echo "------------------------------------------------------------"
  printf '%s\n' "$PACKAGE_BLOCK"
  echo "------------------------------------------------------------"
fi

echo
echo "Daarna:"
echo "1. Controleer de Home Assistant-configuratie."
echo "2. Herstart alleen als de configuratie geldig is."
echo "3. Zoek bij Ontwikkelaarstools -> Statussen naar 'luna'."
echo "4. Activeer exports/luna_test_* niet zonder afzonderlijke controle."
echo
echo "Installatie voltooid zonder bestaande automations/scripts te overschrijven."
