# Luna - installatiehandleiding voor Home Assistant

## Veilige installatie

Luna is standaard fail-closed. Fysieke bediening, planneruitvoering, zelfherstel en lokale AI-inference blijven uit totdat de gebruiker deze bewust configureert.

## Vereisten

- Werkende Home Assistant-installatie
- Toegang tot `/config`
- Toegang tot `configuration.yaml`
- Recente Home Assistant-back-up

## Installatie

Kopieer de repository naar het Home Assistant-systeem of voer uit:

```sh
sh install_luna.sh nl
```

De installer kopieert Luna naar `/config/luna`, maakt een back-up van relevante bestaande bestanden en overschrijft bestaande `automations.yaml` of `scripts.yaml` nooit blind.

Wanneer de installer aangeeft dat handmatige configuratie nodig is, voeg je de Luna-regels toe onder de bestaande `homeassistant:` -> `packages:` sectie. Maak nooit een tweede `homeassistant:` sectie.

## Automations, helpers, scripts en Luna Test

`/config/luna/exports` bevat geschoonde bron-/referentie-exporten van automations, helpers en scripts, inclusief `luna_test_*`. Deze bestanden worden bewust **niet automatisch geactiveerd** en worden niet blind samengevoegd met een bestaande Home Assistant-installatie.

De veilige installeerbare laag staat onder `/config/luna/packages`.

## Controle

1. Controleer de Home Assistant-configuratie.
2. Herstart niet zolang er een configuratiefout bestaat.
3. Herstart Home Assistant na een geldige controle.
4. Ga naar Ontwikkelaarstools -> Statussen en zoek op `luna`.
5. Controleer `input_select.luna_language_taal`.
6. Selecteer de gewenste taal.

## Lokale AI

Lokale AI is optioneel. Controleer Luna eerst zonder AI. Configureer daarna pas de lokale backend en selecteer de lokale modus via `input_select.luna_ai_mode`.

## Belangrijk

Eerst Luna installeren en controleren. Daarna pas apparaten, planneruitvoering, zelfherstel of lokale AI configureren.