# Luna - Installationsanleitung für Home Assistant

## Installation mit einem Befehl

Öffnen Sie die **Terminal & SSH App** in Home Assistant und führen Sie aus:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- de
```

Das Repository muss nicht vorher geklont werden. Der Installer lädt Luna herunter, erstellt ein Backup und installiert die Dateien unter `/config/luna`.

## Installierte Komponenten

- Luna-Pakete und alle sieben Sprachmodule
- Dokumentation
- bereinigte Export-/Referenzdateien
- Luna-Dashboard auf Basis des Luna-Test-Dashboards

Vorhandene `automations.yaml` und `scripts.yaml` werden nicht blind überschrieben. `luna_test_*` bleibt deaktiviertes Test-/Referenzmaterial.

## Paketregistrierung

Wenn die Luna-Pakete noch nicht registriert sind, zeigt der Installer den exakten Block für den vorhandenen Abschnitt `homeassistant:` -> `packages:`. Erstellen Sie keinen zweiten `homeassistant:`-Abschnitt.

## Dashboard

Der Installer legt das Dashboard hier ab:

```text
/config/luna/dashboard/luna-dashboard.yaml
```

Interne `.storage`-Dateien werden aus Sicherheitsgründen nicht verändert. Falls das Dashboard noch nicht registriert ist, zeigt der Installer den benötigten `lovelace:`-Block. Nach Registrierung, erfolgreicher Konfigurationsprüfung und Neustart erscheint **Luna** in der Seitenleiste.

## Kontrolle

1. Home-Assistant-Konfiguration prüfen.
2. Bei Fehlern nicht neu starten.
3. Nach erfolgreicher Prüfung neu starten.
4. Luna-Dashboard öffnen.
5. `input_select.luna_language_taal` prüfen und Sprache auswählen.

## Sicherheit

Physische Steuerung, Plannerausführung, Selbstwiederherstellung und lokale KI bleiben fail-closed, bis der Benutzer sie bewusst konfiguriert. Lokale KI ist optional.
