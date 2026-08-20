# Luna - installatiehandleiding voor Home Assistant

## Installeren met één commando

Open de **Terminal & SSH App** in Home Assistant en voer uit:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl
```

De gebruiker hoeft de GitHub-repository niet eerst te clonen. De installer downloadt Luna, maakt een back-up en installeert de bestanden onder `/config/luna`.

## Wat wordt geïnstalleerd

- Luna packages en alle zeven taalmodules
- documentatie
- geschoonde exports/referentiemateriaal
- het Luna-dashboard gebaseerd op het dashboard uit Luna Test

Bestaande `automations.yaml` en `scripts.yaml` worden nooit blind overschreven. `luna_test_*` blijft uitgeschakeld test-/referentiemateriaal.

## Packages registreren

Wanneer de Luna-packages nog niet in `configuration.yaml` geregistreerd zijn, toont de installer het exacte blok dat onder de bestaande `homeassistant:` -> `packages:` sectie moet worden toegevoegd. Maak nooit een tweede `homeassistant:` sectie.

## Luna-dashboard

De installer plaatst het dashboard automatisch als:

```text
/config/luna/dashboard/luna-dashboard.yaml
```

Om Home Assistant veilig te houden wijzigt de installer geen interne `.storage` bestanden. Als het dashboard nog niet geregistreerd is, toont de installer het exacte `lovelace:` blok dat in `configuration.yaml` nodig is. Na registratie, configuratiecontrole en herstart verschijnt **Luna** in de zijbalk.

## Controle

1. Controleer de Home Assistant-configuratie.
2. Herstart niet als er een configuratiefout is.
3. Herstart na een geldige controle.
4. Open het Luna-dashboard.
5. Controleer `input_select.luna_language_taal` en kies de gewenste taal.

## Veiligheid

Fysieke bediening, planneruitvoering, zelfherstel en lokale AI blijven fail-closed totdat de gebruiker deze bewust configureert. Lokale AI is optioneel.
