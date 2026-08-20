# Luna

Veilige, configureerbare Home Assistant-laag voor status, leren, planning en optionele lokale AI. Luna start zonder fysieke bediening, zelfherstel, planneruitvoering en AI-inference.

## Snelle installatie

Open de Home Assistant Terminal & SSH App en kies een dashboardvariant.

Volledig standaard Home Assistant:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl native
```

Luxere variant met Mushroom en card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl custom
```

De custom variant vereist dat **Mushroom** en **card-mod** via HACS beschikbaar zijn.

## Taalmodules

Luna bevat zeven taalmodules: Nederlands, English, Deutsch, Français, Español, Italiano en Português. Kies de taal met `input_select.luna_language_taal`. Status-, fout-, planner-, geheugen-, AI- en zelfcontrolemeldingen worden per module vertaald.

## Veiligheidsinstellingen

De standaardwaarden zijn fail-closed:

- fysieke bediening: uit;
- zelfherstel: uit;
- planneruitvoering: uit;
- lokale AI-inference: uit;
- ontbrekende apparaten, diensten of AI: geen actie.

Activeer fysieke of plannerfuncties pas nadat de eigen entiteiten als placeholders zijn ingevuld en afzonderlijk zijn gecontroleerd. Meldtargets zijn niet inbegrepen.

## AI zonder en met lokale AI

Zonder AI werkt Luna als veilige status-, leer- en controlelaag. Voor lokale AI kan een lokaal backend, bijvoorbeeld Ollama, worden geconfigureerd via de AI-backendvelden. Zet daarna `input_select.luna_ai_mode` op `Lokaal`. De backend-URL en modelnaam blijven placeholders totdat de gebruiker deze zelf configureert.

## Exports

De map `exports/` bevat geschoonde bronlogica voor automatiseringen, helpers en scripts. De veilige installeerbare gebruikerslaag staat onder `packages/`.

## Dashboards

Er zijn twee keuzes:

- `dashboard/luna-dashboard-native.yaml` — uitsluitend standaard Home Assistant-kaarten;
- `dashboard/luna-dashboard-custom.yaml` — premium interface met Mushroom en card-mod.

De installer registreert de gekozen variant en overschrijft bestaande `automations.yaml` en `scripts.yaml` niet.

## Privacy

Er zijn geen gesprekken, persoonlijke geheugenrecords, gebruikers-ID's, echte namen, locaties, IP/MAC-adressen, wachtwoorden, tokens, telefoons of persoonlijke meldkanalen opgenomen. Geheugenvelden zijn leeg en tellerinitialen zijn nul. Fysieke, telefoon-, netwerk- en systeembindingen zijn vervangen door placeholders.

## Controle

Controleer vóór gebruik:

1. De Home Assistant-configuratie is geldig.
2. Placeholder-entiteiten veroorzaken fail-closed gedrag zolang ze niet zijn gekoppeld.
3. Eigen entiteiten worden pas geconfigureerd nadat de veilige basiscontrole is geslaagd.
4. Optionele functies worden één voor één geactiveerd.
