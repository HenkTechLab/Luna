# Luna

Veilige, configureerbare Home Assistant-laag voor status, leren, planning en optionele lokale AI. Luna start zonder fysieke bediening, zelfherstel, planneruitvoering en AI-inference.

## Installatie

Kopieer de repository naar je Home Assistant-configuratie en voeg de pakketten expliciet toe:

```yaml
homeassistant:
  packages:
    luna: !include packages/luna.yaml
    luna_modules: !include packages/luna_modules.yaml
    luna_advanced_modules: !include packages/luna_advanced_modules.yaml
    luna_nederlands: !include packages/languages/nederlands.yaml
    luna_english: !include packages/languages/english.yaml
    luna_deutsch: !include packages/languages/deutsch.yaml
    luna_francais: !include packages/languages/francais.yaml
    luna_espanol: !include packages/languages/espanol.yaml
    luna_italiano: !include packages/languages/italiano.yaml
    luna_portugues: !include packages/languages/portugues.yaml
```

Herlaad daarna Home Assistant-pakketten of herstart Home Assistant. Controleer in Ontwikkelaarstools → Statussen of de Luna-helpers beschikbaar zijn.

## Taalmodules

Er zijn zeven losse taalmodules: Nederlands, English, Deutsch, Français, Español, Italiano en Português. Kies de taal met `input_select.luna_language_taal`. Status-, fout-, planner-, geheugen-, test-, AI- en zelfcontrolemeldingen worden per module vertaald.

## Veiligheidsinstellingen

De standaardwaarden zijn fail-closed:

- fysieke bediening: uit;
- zelfherstel: uit;
- planneruitvoering: uit;
- lokale AI-inference: uit;
- ontbrekende apparaten, diensten of AI: geen actie.

Activeer fysieke of plannerfuncties pas nadat je eigen entiteiten als placeholders hebt ingevuld en afzonderlijk hebt getest. Meldtargets zijn niet inbegrepen.

## AI zonder en met lokale AI

Zonder AI werkt Luna als veilige status-, leer- en controlelaag. Voor lokale AI kun je een lokaal backend (bijvoorbeeld Ollama) configureren via de AI-backendvelden en daarna `input_select.luna_ai_mode` op `Lokaal` zetten. De backend-URL en modelnaam blijven placeholders; er wordt niets naar een externe dienst gestuurd zonder eigen configuratie.

## Export en testmodules

De map `exports/` bevat de geschoonde bronlogica uit de Luna-configuratie:

- 91 automatiseringen gelezen en geëxporteerd;
- 381 helperdefinities gelezen; 363 geschoonde helpers geëxporteerd;
- 8 scripts gelezen en geëxporteerd;
- 18 persoons-/apparaatgebonden helperrecords uitgesloten.

Bestanden onder `exports/automations/luna_test_*.yaml`, `exports/helpers/luna_test_*.yaml` en `exports/scripts/luna_test.yaml` zijn gemarkeerde testmodules. Ze zijn bronexporten in JSON-vormige YAML-lijsten en worden niet automatisch geladen als klantpakket. De installeerbare klantpakketten staan onder `packages/`.

## Privacy

Er zijn geen gesprekken, persoonlijke geheugenrecords, gebruikers-ID's, echte namen, locaties, IP/MAC-adressen, wachtwoorden, tokens, telefoons of meldkanalen opgenomen. Geheugenvelden zijn leeg en tellerinitialen zijn nul. Fysieke, telefoon-, netwerk- en systeembindingen zijn vervangen door placeholders.

## Controle

Controleer vóór gebruik:

1. YAML-lijsten kunnen als YAML worden geparsed.
2. Placeholder-entiteiten bestaan nog niet en veroorzaken daardoor fail-closed gedrag.
3. Je configureert pas eigen entiteiten nadat de veilige basiscontrole geslaagd is.
4. De repository bevat alleen de naam Luna.
