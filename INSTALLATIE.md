# Luna installeren via HACS

HACS is de enige ondersteunde installatieroute. Er is geen Terminal & SSH App, curl-opdracht of los installatiescript nodig.

## Voorwaarden

- Een actuele Home Assistant-installatie.
- HACS is geïnstalleerd.
- De GitHub-repository `HenkTechLab/Luna` is openbaar; HACS ondersteunt geen privé-repositories.

Voor de custom dashboardvariant zijn daarnaast **Mushroom** en **card-mod** nodig. De native variant heeft geen frontend-afhankelijkheden.

## 1. Downloaden met HACS

1. Open **HACS**.
2. Open het menu en kies **Custom repositories**.
3. Vul `HenkTechLab/Luna` in en kies categorie **Integration**.
4. Open Luna, kies **Download** en herstart Home Assistant.
5. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen**.
6. Zoek **Luna**, voeg de integratie toe en kies **Native** of **Custom**.

Home Assistant maakt één Luna-configuratie aan. Een tweede Luna-configuratie wordt bewust geblokkeerd.

## 2. Packages eenmalig registreren

Voeg de volgende regels toe onder de bestaande `homeassistant:` → `packages:` sectie in `configuration.yaml`. Maak geen tweede `homeassistant:` sectie.

```yaml
homeassistant:
  packages:
    luna: !include custom_components/luna/resources/packages/luna.yaml
    luna_modules: !include custom_components/luna/resources/packages/luna_modules.yaml
    luna_advanced_modules: !include custom_components/luna/resources/packages/luna_advanced_modules.yaml
    luna_nederlands: !include custom_components/luna/resources/packages/languages/nederlands.yaml
    luna_english: !include custom_components/luna/resources/packages/languages/english.yaml
    luna_deutsch: !include custom_components/luna/resources/packages/languages/deutsch.yaml
    luna_francais: !include custom_components/luna/resources/packages/languages/francais.yaml
    luna_espanol: !include custom_components/luna/resources/packages/languages/espanol.yaml
    luna_italiano: !include custom_components/luna/resources/packages/languages/italiano.yaml
    luna_portugues: !include custom_components/luna/resources/packages/languages/portugues.yaml
```

Heeft je configuratie al packages, voeg dan alleen de tien `luna...` regels toe met dezelfde inspringing als de bestaande package-items.

## 3. Dashboard eenmalig registreren

Voeg één dashboard toe onder de bestaande `lovelace:` → `dashboards:` sectie. Maak geen tweede `lovelace:` sectie.

### Native

```yaml
lovelace:
  dashboards:
    luna-dashboard:
      mode: yaml
      title: Luna
      icon: mdi:moon-waning-crescent
      show_in_sidebar: true
      filename: custom_components/luna/resources/dashboard/luna-dashboard-native.yaml
```

### Custom

Installeer eerst Mushroom en card-mod via HACS en gebruik daarna:

```yaml
lovelace:
  dashboards:
    luna-dashboard:
      mode: yaml
      title: Luna
      icon: mdi:moon-waning-crescent
      show_in_sidebar: true
      filename: custom_components/luna/resources/dashboard/luna-dashboard-custom.yaml
```

## 4. Controleren en starten

1. Open **Ontwikkelaarstools → YAML** en voer de configuratiecontrole uit.
2. Los alle gemelde fouten op; herstart niet met een ongeldige configuratie.
3. Herstart Home Assistant.
4. Open **Luna** in de zijbalk.
5. Controleer dat `input_select.luna_language_taal` bestaat en kies de gewenste taal.
6. Controleer dat `binary_sensor.luna_veilig_fail_closed` aan staat.
7. Laat fysieke bediening, planneruitvoering, zelfherstel en lokale AI uit totdat eigen entiteiten bewust zijn gekoppeld en getest.

## Updates

1. Installeer de Luna-update in HACS.
2. Controleer de Home Assistant-configuratie.
3. Herstart Home Assistant.
4. Controleer beide Luna-statussensoren en het dashboard.

De include-paden blijven gelijk. HACS vervangt de integration-resources, zodat losse downloads of kopieeracties niet nodig zijn.

## Verwijderen

1. Verwijder eerst de Luna-integratie via **Instellingen → Apparaten & diensten**.
2. Verwijder de Luna package- en dashboardregels uit `configuration.yaml`.
3. Controleer de configuratie en herstart Home Assistant.
4. Verwijder Luna daarna via HACS.

Deze volgorde voorkomt include-fouten nadat HACS de Luna-bestanden heeft verwijderd.

