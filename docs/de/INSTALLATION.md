# Luna - Installationsanleitung für Home Assistant

## Sichere Installation

Luna arbeitet standardmäßig nach dem Fail-Closed-Prinzip. Physische Steuerung, Plannerausführung, Selbstwiederherstellung und lokale KI-Inferenz bleiben deaktiviert, bis der Benutzer sie bewusst konfiguriert.

## Voraussetzungen

- Funktionierende Home-Assistant-Installation
- Zugriff auf `/config`
- Zugriff auf `configuration.yaml`
- Aktuelles Home-Assistant-Backup

## Installation

Repository auf das Home-Assistant-System kopieren oder ausführen:

```sh
sh install_luna.sh de
```

Der Installer kopiert Luna nach `/config/luna`, erstellt ein Backup relevanter vorhandener Dateien und überschreibt vorhandene `automations.yaml` oder `scripts.yaml` niemals blind.

Falls der Installer eine manuelle Konfiguration verlangt, müssen die Luna-Pakete unter dem vorhandenen Abschnitt `homeassistant:` -> `packages:` eingebunden werden. Keinen zweiten `homeassistant:`-Abschnitt erstellen.

## Automationen, Helfer, Skripte und Luna Test

`/config/luna/exports` enthält bereinigte Quell-/Referenzexporte für Automationen, Helfer und Skripte einschließlich `luna_test_*`. Diese Dateien werden bewusst **nicht automatisch aktiviert** und nicht blind in eine bestehende Home-Assistant-Konfiguration übernommen.

Die sichere installierbare Schicht befindet sich unter `/config/luna/packages`.

## Kontrolle

1. Home-Assistant-Konfiguration prüfen.
2. Bei einem Konfigurationsfehler nicht neu starten.
3. Nach erfolgreicher Prüfung Home Assistant neu starten.
4. Entwicklerwerkzeuge -> Zustände öffnen und nach `luna` suchen.
5. `input_select.luna_language_taal` prüfen.
6. Gewünschte Sprache auswählen.

## Lokale KI

Lokale KI ist optional. Luna zuerst ohne KI prüfen. Danach erst das lokale Backend konfigurieren und über `input_select.luna_ai_mode` den lokalen Modus auswählen.

## Wichtig

Zuerst Luna installieren und prüfen. Erst danach Geräte, Plannerausführung, Selbstwiederherstellung oder lokale KI konfigurieren.