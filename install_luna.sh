#!/bin/sh
set -eu

# Luna multilingual installer for Home Assistant
# Usage: sh install_luna.sh [nl|en|de|fr|es|it|pt]

REPO_URL="https://github.com/HenkTechLab/Luna.git"
HA_CONFIG="${HA_CONFIG:-/config}"
LANG_CODE="${1:-en}"
WORKDIR="${TMPDIR:-/tmp}/luna-install-$$"
BACKUP_DIR="$HA_CONFIG/luna_backup_$(date +%Y%m%d_%H%M%S)"
LUNA_DIR="$HA_CONFIG/luna"

case "$LANG_CODE" in
  nl) TITLE="Luna installer voor Home Assistant"; TARGET="Doelmap"; DOWNLOAD="Luna downloaden"; BACKUP="Back-up maken"; INSTALL="Luna-bestanden installeren"; CHECK="configuration.yaml controleren"; EXPORTS="Automations, scripts en helpers controleren"; SUMMARY="Installatieoverzicht maken"; DONE="Klaar"; ERRDIR="Home Assistant-configuratiemap bestaat niet"; ERRGIT="git is niet beschikbaar"; MANUAL="Voeg de onderstaande regels handmatig toe onder homeassistant: -> packages:" ;;
  de) TITLE="Luna-Installer für Home Assistant"; TARGET="Zielordner"; DOWNLOAD="Luna herunterladen"; BACKUP="Backup erstellen"; INSTALL="Luna-Dateien installieren"; CHECK="configuration.yaml prüfen"; EXPORTS="Automationen, Skripte und Helfer prüfen"; SUMMARY="Installationsübersicht erstellen"; DONE="Fertig"; ERRDIR="Home-Assistant-Konfigurationsordner existiert nicht"; ERRGIT="git ist nicht verfügbar"; MANUAL="Fügen Sie die folgenden Zeilen manuell unter homeassistant: -> packages: ein:" ;;
  fr) TITLE="Installateur Luna pour Home Assistant"; TARGET="Dossier cible"; DOWNLOAD="Téléchargement de Luna"; BACKUP="Création de la sauvegarde"; INSTALL="Installation des fichiers Luna"; CHECK="Vérification de configuration.yaml"; EXPORTS="Vérification des automatisations, scripts et helpers"; SUMMARY="Création du résumé d'installation"; DONE="Terminé"; ERRDIR="Le dossier de configuration Home Assistant n'existe pas"; ERRGIT="git n'est pas disponible"; MANUAL="Ajoutez manuellement les lignes suivantes sous homeassistant: -> packages:" ;;
  es) TITLE="Instalador Luna para Home Assistant"; TARGET="Carpeta de destino"; DOWNLOAD="Descargando Luna"; BACKUP="Creando copia de seguridad"; INSTALL="Instalando archivos Luna"; CHECK="Comprobando configuration.yaml"; EXPORTS="Comprobando automatizaciones, scripts y helpers"; SUMMARY="Creando resumen de instalación"; DONE="Terminado"; ERRDIR="La carpeta de configuración de Home Assistant no existe"; ERRGIT="git no está disponible"; MANUAL="Añada manualmente las siguientes líneas bajo homeassistant: -> packages:" ;;
  it) TITLE="Installer Luna per Home Assistant"; TARGET="Cartella di destinazione"; DOWNLOAD="Download di Luna"; BACKUP="Creazione backup"; INSTALL="Installazione dei file Luna"; CHECK="Controllo di configuration.yaml"; EXPORTS="Controllo di automazioni, script e helper"; SUMMARY="Creazione riepilogo installazione"; DONE="Completato"; ERRDIR="La cartella di configurazione Home Assistant non esiste"; ERRGIT="git non è disponibile"; MANUAL="Aggiungere manualmente le seguenti righe sotto homeassistant: -> packages:" ;;
  pt) TITLE="Instalador Luna para Home Assistant"; TARGET="Pasta de destino"; DOWNLOAD="A transferir Luna"; BACKUP="A criar backup"; INSTALL="A instalar ficheiros Luna"; CHECK="A verificar configuration.yaml"; EXPORTS="A verificar automações, scripts e helpers"; SUMMARY="A criar resumo da instalação"; DONE="Concluído"; ERRDIR="A pasta de configuração do Home Assistant não existe"; ERRGIT="git não está disponível"; MANUAL="Adicione manualmente as seguintes linhas em homeassistant: -> packages:" ;;
  en|*) LANG_CODE="en"; TITLE="Luna installer for Home Assistant"; TARGET="Target directory"; DOWNLOAD="Downloading Luna"; BACKUP="Creating backup"; INSTALL="Installing Luna files"; CHECK="Checking configuration.yaml"; EXPORTS="Checking automations, scripts and helpers"; SUMMARY="Creating installation summary"; DONE="Done"; ERRDIR="Home Assistant configuration directory does not exist"; ERRGIT="git is not available"; MANUAL="Add the following lines manually under homeassistant: -> packages:" ;;
esac

cleanup() { rm -rf "$WORKDIR"; }
trap cleanup EXIT INT TERM

echo "=========================================="
echo " $TITLE"
echo "=========================================="
echo "$TARGET: $HA_CONFIG"

if [ ! -d "$HA_CONFIG" ]; then echo "ERROR: $ERRDIR: $HA_CONFIG"; exit 1; fi
if ! command -v git >/dev/null 2>&1; then echo "ERROR: $ERRGIT"; exit 1; fi

mkdir -p "$WORKDIR"
echo "[1/7] $DOWNLOAD..."
git clone --depth 1 "$REPO_URL" "$WORKDIR/repo"

for required in packages/luna.yaml packages/luna_modules.yaml packages/luna_advanced_modules.yaml; do
  [ -f "$WORKDIR/repo/$required" ] || { echo "ERROR: missing $required"; exit 1; }
done

echo "[2/7] $BACKUP..."
mkdir -p "$BACKUP_DIR"
for f in configuration.yaml automations.yaml scripts.yaml; do
  [ ! -f "$HA_CONFIG/$f" ] || cp -p "$HA_CONFIG/$f" "$BACKUP_DIR/$f"
done
[ ! -d "$LUNA_DIR" ] || cp -R "$LUNA_DIR" "$BACKUP_DIR/luna"

echo "[3/7] $INSTALL..."
rm -rf "$LUNA_DIR.new"
mkdir -p "$LUNA_DIR.new"
cp -R "$WORKDIR/repo/packages" "$LUNA_DIR.new/packages"
[ ! -d "$WORKDIR/repo/exports" ] || cp -R "$WORKDIR/repo/exports" "$LUNA_DIR.new/exports"
[ ! -d "$WORKDIR/repo/docs" ] || cp -R "$WORKDIR/repo/docs" "$LUNA_DIR.new/docs"
rm -rf "$LUNA_DIR"
mv "$LUNA_DIR.new" "$LUNA_DIR"

echo "[4/7] $CHECK..."
CONFIG="$HA_CONFIG/configuration.yaml"
NEED_MANUAL=1
if [ -f "$CONFIG" ] && grep -q 'luna/packages/luna.yaml' "$CONFIG"; then NEED_MANUAL=0; fi

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

echo "[5/7] $EXPORTS..."
echo "Luna exports and luna_test_* are copied as reference material and are NOT activated automatically."
echo "Existing automations.yaml and scripts.yaml are NOT overwritten."

echo "[6/7] $SUMMARY..."
cat > "$LUNA_DIR/INSTALLATION_STATUS.txt" <<EOF
Luna: $LUNA_DIR
Backup: $BACKUP_DIR
Packages: $LUNA_DIR/packages
Exports/reference: $LUNA_DIR/exports
Documentation: $LUNA_DIR/docs
Language: $LANG_CODE

Exports and luna_test_* are not automatically activated.
Existing automations.yaml and scripts.yaml were not overwritten.
Home Assistant was not automatically restarted.
EOF

echo "[7/7] $DONE."
if [ "$NEED_MANUAL" -eq 1 ]; then
  echo "$MANUAL"
  echo "------------------------------------------------------------"
  printf '%s\n' "$PACKAGE_BLOCK"
  echo "------------------------------------------------------------"
fi

echo "Documentation: $LUNA_DIR/docs/$LANG_CODE"
echo "Validate the Home Assistant configuration before restarting."
