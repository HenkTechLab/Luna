# Luna - installatiehandleiding voor Home Assistant

## Installeren met één commando

Open de **Terminal & SSH App** in Home Assistant en kies een dashboardvariant.

### Optie 1 - Native

Alleen standaard Home Assistant-kaarten, zonder extra frontend-afhankelijkheden:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl native
```

### Optie 2 - Custom

Luxere interface met Mushroom en card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl custom
```

Voor de custom variant moeten **Mushroom** en **card-mod** via HACS beschikbaar zijn.

## Wat de installer doet

1. Controleert of `/config` beschikbaar is.
2. Downloadt Luna.
3. Maakt een back-up van relevante bestaande configuratie.
4. Installeert de Luna-packages onder `/config/luna/packages`.
5. Kopieert documentatie en geschoonde exports.
6. Installeert beide dashboardbestanden onder `/config/luna/dashboard/`.
7. Selecteert de gekozen dashboardvariant voor registratie.
8. Toont exact welke regels eventueel nog in `configuration.yaml` moeten worden toegevoegd.
9. Overschrijft bestaande `automations.yaml` en `scripts.yaml` niet.
10. Herstart Home Assistant niet automatisch.

## Packages registreren

Wanneer de Luna-packages nog niet geregistreerd zijn, toont de installer het exacte blok dat onder de bestaande `homeassistant:` -> `packages:` sectie moet worden toegevoegd. Maak nooit een tweede `homeassistant:` sectie.

## Dashboard

De twee dashboardbestanden zijn:

```text
/config/luna/dashboard/luna-dashboard-native.yaml
/config/luna/dashboard/luna-dashboard-custom.yaml
```

De native variant gebruikt moderne sections, headings, tiles, badges en section backgrounds.

De custom variant gebruikt Mushroom en card-mod voor extra styling, gradients, compacte statuskaarten en een meer uitgesproken command-center uiterlijk.

De installer wijzigt geen interne Home Assistant `.storage` bestanden. Als dashboardregistratie nog nodig is, toont hij het juiste `lovelace:` blok.

## Automatiseringen, helpers en scripts

De map `/config/luna/exports` bevat geschoonde bronlogica voor automatiseringen, helpers en scripts. Deze wordt niet blind samengevoegd met bestaande configuratiebestanden. De veilige installeerbare Luna-laag staat onder `/config/luna/packages`.

## Na installatie

1. Lees de uitvoer van de installer.
2. Voeg alleen ontbrekende package- en dashboardregistratie toe.
3. Controleer de Home Assistant-configuratie.
4. Herstart niet wanneer Home Assistant een configuratiefout meldt.
5. Herstart na een geldige configuratiecontrole.
6. Open **Luna** in de zijbalk.
7. Controleer `input_select.luna_language_taal`.
8. Kies de gewenste taal.

## Veiligheid

Luna blijft standaard fail-closed. Fysieke bediening, planneruitvoering, zelfherstel en lokale AI worden pas gebruikt nadat de gebruiker deze bewust configureert en controleert.

**Belangrijkste regel: eerst installeren en controleren; daarna pas apparaten, planneruitvoering, zelfherstel of lokale AI activeren.**
