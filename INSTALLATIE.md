# Luna - duidelijke installatiehandleiding voor Home Assistant

## Aanbevolen installatie: één commando

Open in Home Assistant de **Terminal & SSH App** en voer dit commando uit:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl
```

De gebruiker hoeft Luna niet eerst te downloaden of met Git te clonen. De installer downloadt de actuele Luna-release rechtstreeks vanaf GitHub.

## Wat de installer doet

1. Controleert of `/config` beschikbaar is.
2. Downloadt de Luna-repository.
3. Maakt een back-up van relevante bestaande configuratie.
4. Installeert de Luna-packages onder `/config/luna/packages`.
5. Kopieert documentatie en geschoonde exports.
6. Installeert het Luna-dashboardbestand onder `/config/luna/dashboard/luna-dashboard.yaml`.
7. Controleert of packages en dashboard al geregistreerd zijn.
8. Toont exact welke regels nog in `configuration.yaml` moeten worden toegevoegd.
9. Overschrijft bestaande `automations.yaml` en `scripts.yaml` niet.
10. Activeert `luna_test_*` niet automatisch.
11. Herstart Home Assistant niet automatisch.

## Waarom configuration.yaml niet blind automatisch wordt aangepast

De configuratie van iedere gebruiker kan anders zijn. Een shellscript dat zonder YAML-kennis automatisch regels in een bestaande `configuration.yaml` plaatst kan de configuratie beschadigen. Daarom toont de installer het exacte ontbrekende blok wanneer handmatige registratie nodig is.

## Luna-dashboard

Het dashboard is gebaseerd op het werkende dashboard uit de Luna Test-installatie en gebruikt moderne Home Assistant sections/tile-kaarten.

De installer plaatst het dashboard automatisch hier:

```text
/config/luna/dashboard/luna-dashboard.yaml
```

Als het dashboard nog niet geregistreerd is, toont de installer dit blok:

```yaml
lovelace:
  dashboards:
    luna-dashboard:
      mode: yaml
      title: Luna
      icon: mdi:robot
      show_in_sidebar: true
      filename: luna/dashboard/luna-dashboard.yaml
```

Bestaat `lovelace:` al, voeg dan alleen de Luna-dashboarddefinitie correct aan de bestaande structuur toe. Maak geen dubbele hoofdsecties.

De installer wijzigt bewust geen interne Home Assistant `.storage` bestanden.

## Luna-packages

Wanneer de packages nog niet geregistreerd zijn, toont de installer het benodigde blok voor de bestaande `homeassistant:` -> `packages:` sectie. Maak nooit een tweede `homeassistant:` sectie.

## Automations, helpers, scripts en Luna Test

De map `/config/luna/exports` bevat geschoonde bron-/referentie-exporten van Luna-automations, helpers en scripts, inclusief `luna_test_*` materiaal.

Deze exports worden bewust niet blind toegevoegd aan bestaande Home Assistant-configuraties. De veilige installeerbare Luna-laag staat onder `/config/luna/packages`.

## Na installatie

1. Lees de uitvoer van de installer.
2. Voeg alleen de aangegeven ontbrekende package- en dashboardregistratie toe.
3. Controleer de Home Assistant-configuratie.
4. Herstart niet als er een fout wordt gemeld.
5. Herstart Home Assistant na een geldige configuratiecontrole.
6. Open **Luna** in de zijbalk.
7. Controleer `input_select.luna_language_taal`.
8. Kies de gewenste taal.

## Andere talen

Gebruik hetzelfde installatiecommando met de gewenste taalcode:

```sh
# English
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- en

# Deutsch
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- de

# Français
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- fr

# Español
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- es

# Italiano
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- it

# Português
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- pt
```

## Veiligheid

Luna blijft standaard fail-closed. Fysieke bediening, planneruitvoering, zelfherstel en lokale AI worden pas gebruikt nadat de gebruiker deze bewust configureert en controleert.

**Belangrijkste regel: eerst installeren en controleren; daarna pas apparaten, planneruitvoering, zelfherstel of lokale AI activeren.**
