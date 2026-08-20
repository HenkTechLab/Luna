# Luna - Installationsanleitung für Home Assistant

## Ein Befehl

Öffnen Sie die **Terminal & SSH App** in Home Assistant.

Native Dashboard ohne zusätzliche Frontend-Abhängigkeiten:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- de native
```

Custom Dashboard mit Mushroom und card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- de custom
```

Für die Custom-Variante müssen **Mushroom** und **card-mod** über HACS verfügbar sein.

## Installer

Der Installer lädt Luna herunter, erstellt ein Backup und installiert Pakete, Sprachen, Dokumentation, Exporte und beide Dashboard-Dateien unter `/config/luna`. Vorhandene `automations.yaml` und `scripts.yaml` werden nicht überschrieben.

Falls noch Einträge in `configuration.yaml` fehlen, zeigt der Installer den exakten Block. Interne `.storage`-Dateien werden nicht verändert.

## Dashboards

- `luna-dashboard-native.yaml` - moderne Standardkarten von Home Assistant.
- `luna-dashboard-custom.yaml` - umfangreichere Oberfläche mit Mushroom und card-mod.

## Kontrolle

1. Home-Assistant-Konfiguration prüfen.
2. Bei einem Konfigurationsfehler nicht neu starten.
3. Nach erfolgreicher Prüfung neu starten.
4. Luna in der Seitenleiste öffnen.
5. `input_select.luna_language_taal` prüfen und die gewünschte Sprache wählen.

## Sicherheit

Physische Steuerung, Plannerausführung, Selbstwiederherstellung und lokale KI bleiben fail-closed, bis der Benutzer sie bewusst konfiguriert.
