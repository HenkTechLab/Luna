# Luna - duidelijke installatiehandleiding voor Home Assistant

Deze handleiding beschrijft stap voor stap hoe je Luna veilig installeert in Home Assistant.

> **Belangrijk:** Luna is standaard **fail-closed**. Fysieke bediening, planneruitvoering, zelfherstel en lokale AI-inference staan standaard uit. Configureer en test deze functies pas nadat de basisinstallatie correct werkt.

---

## 1. Wat is Luna?

Luna is een configureerbare Home Assistant-laag voor onder andere:

- status en systeemcontrole;
- geheugen- en leermodules;
- tijdlijn en routines;
- voorspellingen en planning;
- zelfcontrole en gezondheid;
- analytics en bewijscontrole;
- beslis- en onderhoudsstatus;
- optionele lokale AI;
- meertalige statussen.

Luna kan zonder lokale AI worden gebruikt. Een AI-backend is dus **niet verplicht** voor de basisinstallatie.

---

## 2. Vereisten

Voor installatie heb je nodig:

1. Een werkende Home Assistant-installatie.
2. Toegang tot de Home Assistant-configuratiemap (`/config`).
3. Mogelijkheid om bestanden en mappen naar `/config` te kopiëren.
4. Toegang tot `configuration.yaml`.
5. Een recente back-up van Home Assistant voordat je begint.

Maak altijd eerst een Home Assistant-back-up.

---

## 3. Luna downloaden

Download of clone de repository:

`HenkTechLab/Luna`

Je hebt voor de normale installatie minimaal de map `packages/` nodig.

De relevante structuur is:

```text
packages/
├── luna.yaml
├── luna_modules.yaml
├── luna_advanced_modules.yaml
└── languages/
    ├── nederlands.yaml
    ├── english.yaml
    ├── deutsch.yaml
    ├── francais.yaml
    ├── espanol.yaml
    ├── italiano.yaml
    └── portugues.yaml
```

De map `exports/` bevat geschoonde bronexporten en testmateriaal. Deze bestanden zijn **niet nodig voor de standaardinstallatie** en moeten niet automatisch als Home Assistant-pakket worden geladen.

---

## 4. Bestanden naar Home Assistant kopiëren

Kopieer de volledige map `packages` naar de Home Assistant-configuratiemap.

Daarna moet de structuur bijvoorbeeld zijn:

```text
/config/
├── configuration.yaml
└── packages/
    ├── luna.yaml
    ├── luna_modules.yaml
    ├── luna_advanced_modules.yaml
    └── languages/
        ├── nederlands.yaml
        ├── english.yaml
        ├── deutsch.yaml
        ├── francais.yaml
        ├── espanol.yaml
        ├── italiano.yaml
        └── portugues.yaml
```

Controleer de bestandsnamen zorgvuldig. Verander de namen niet tijdens de eerste installatie.

---

## 5. Luna toevoegen aan configuration.yaml

Open `/config/configuration.yaml`.

Voeg onder `homeassistant:` de volgende package-definities toe:

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

### Als `homeassistant:` al bestaat

Maak **geen tweede `homeassistant:`-sectie**.

Voorbeeld. Heb je al:

```yaml
homeassistant:
  name: Thuis
```

maak er dan bijvoorbeeld van:

```yaml
homeassistant:
  name: Thuis
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

Behoud alle bestaande Home Assistant-instellingen.

---

## 6. Configuratie controleren

Controleer vóór de herstart altijd de Home Assistant-configuratie.

Gebruik in Home Assistant de beschikbare configuratiecontrole voordat je herstart.

### Bij een fout

Herstart Home Assistant **niet** zolang de configuratiecontrole een fout meldt.

Controleer dan eerst:

- inspringing in `configuration.yaml`;
- dubbele `homeassistant:`-secties;
- of de map `packages` werkelijk onder `/config` staat;
- of alle genoemde bestanden bestaan;
- of bestandsnamen exact overeenkomen.

---

## 7. Home Assistant herstarten

Als de configuratiecontrole zonder fouten is afgerond, herstart Home Assistant.

Wacht totdat Home Assistant volledig beschikbaar is.

---

## 8. Controleren of Luna geladen is

Ga in Home Assistant naar:

**Ontwikkelaarstools -> Statussen**

Zoek op:

```text
luna
```

Controleer of Luna-helpers en statussen aanwezig zijn.

Controleer in het bijzonder of de taalkeuze bestaat:

```text
input_select.luna_language_taal
```

Als de Luna-entiteiten zichtbaar zijn, is de package-laag geladen.

---

## 9. Taal instellen

Luna bevat zeven taalmodules:

- Nederlands
- English
- Deutsch
- Français
- Español
- Italiano
- Português

Selecteer de gewenste taal via:

```text
input_select.luna_language_taal
```

De taalmodules verzorgen vertaalde Luna-statusvelden voor onder andere installatie, veiligheid, geheugen, tijdlijn, voorspelling, routine, planner, gezondheid, zelfcheck, leren, analytics, bewijs, beslissing, stem, onderhoud, configuratie en lokale AI-status.

---

## 10. Eerste veilige test

Na installatie moet je eerst alleen controleren of Luna correct geladen is.

Controleer:

1. Home Assistant start zonder configuratiefouten.
2. Luna-entiteiten zijn aanwezig.
3. De taalkeuze werkt.
4. Luna-statusvelden worden bijgewerkt.
5. Er worden geen ongewenste fysieke acties uitgevoerd.
6. Er worden geen meldingen naar onbekende targets gestuurd.
7. Lokale AI wordt niet onverwacht aangeroepen.

De standaardconfiguratie is bewust veilig opgezet: ontbrekende apparaten, services of AI-backends moeten niet tot fysieke acties leiden.

---

## 11. Veiligheidsfuncties

De volgende onderdelen staan standaard uit:

- fysieke bediening;
- zelfherstel;
- planneruitvoering;
- lokale AI-inference.

Laat deze functies uit tijdens de eerste installatie.

Activeer fysieke bediening of planneruitvoering pas wanneer:

1. de basisinstallatie stabiel werkt;
2. je de betreffende Luna-module begrijpt;
3. de placeholders zijn vervangen door jouw eigen Home Assistant-entiteiten;
4. iedere gebruikte entiteit afzonderlijk is gecontroleerd;
5. de functie eerst gecontroleerd en veilig getest is.

Gebruik nooit willekeurige entity-ID's om placeholders te vervangen.

---

## 12. Luna zonder AI gebruiken

Lokale AI is optioneel.

Zonder AI kan Luna nog steeds functioneren als veilige status-, leer-, planning- en controlelaag voor de onderdelen die geen inference vereisen.

Je hoeft voor de eerste installatie dus geen Ollama of andere AI-server te installeren.

---

## 13. Optionele lokale AI

Configureer lokale AI pas nadat Luna zonder AI correct werkt.

Een lokaal backend, bijvoorbeeld Ollama, kan via de daarvoor bedoelde Luna AI-configuratievelden worden ingesteld.

Daarna kan de Luna AI-modus op lokaal worden gezet via:

```text
input_select.luna_ai_mode
```

Selecteer pas `Lokaal` nadat de backend-URL en modelconfiguratie correct zijn ingevuld en getest.

De repository bevat geen persoonlijke AI-servergegevens, tokens of wachtwoorden.

---

## 14. Wat je NIET moet installeren

De map `exports/` is geen standaard Home Assistant-installatiepakket.

Bestanden zoals:

```text
exports/automations/luna_test_*.yaml
exports/helpers/luna_test_*.yaml
exports/scripts/luna_test.yaml
```

zijn geschoonde bronexporten/testmodules.

Laad deze **niet automatisch** naast de normale `packages/`-installatie, tenzij je precies weet waarvoor je ze gebruikt.

Voor een normale klantinstallatie gebruik je de bestanden onder:

```text
packages/
```

---

## 15. Problemen oplossen

### Luna-entiteiten ontbreken

Controleer:

- of `packages/` in `/config` staat;
- of de include-paden correct zijn;
- of Home Assistant na installatie opnieuw is gestart;
- of de configuratiecontrole fouten geeft.

### Home Assistant geeft YAML-fouten

Controleer eerst `configuration.yaml`.

Veel voorkomende oorzaken:

- verkeerde inspringing;
- twee keer `homeassistant:` gebruikt;
- verkeerd pad naar een package;
- bestand verkeerd genoemd of niet gekopieerd.

### Een taal werkt niet

Controleer of het betreffende taalbestand aanwezig is onder:

```text
/config/packages/languages/
```

Controleer daarna `input_select.luna_language_taal`.

### Fysieke functies doen niets

Dat kan tijdens de eerste installatie **correct gedrag** zijn.

Luna gebruikt veilige standaardinstellingen en placeholders. Fysieke functies horen pas te werken nadat de installatie bewust aan de eigen Home Assistant-installatie is gekoppeld en geactiveerd.

### AI werkt niet

Controleer eerst of lokale AI bewust is geconfigureerd. Zonder ingestelde backend en geactiveerde lokale AI-modus hoort Luna geen lokale inference uit te voeren.

---

## 16. Privacy

De gedeelde Luna-klantconfiguratie is geschoond.

De repository is ontworpen zonder persoonlijke gesprekken, persoonlijke geheugenrecords, gebruikers-ID's, echte namen, locaties, IP/MAC-adressen, wachtwoorden, tokens, telefoonnummers of persoonlijke meldkanalen in de klantconfiguratie.

Eigen privégegevens moeten lokaal door de gebruiker worden geconfigureerd en horen niet terug naar de publieke of gedeelde Luna-configuratie te worden gecommit.

---

## 17. Aanbevolen installatievolgorde

Gebruik voor een nieuwe installatie deze volgorde:

1. Maak een Home Assistant-back-up.
2. Download Luna.
3. Kopieer `packages/` naar `/config/packages/`.
4. Voeg de Luna package-includes toe aan de bestaande `homeassistant:`-sectie.
5. Controleer de Home Assistant-configuratie.
6. Los eventuele YAML-fouten op.
7. Herstart Home Assistant.
8. Zoek bij Ontwikkelaarstools -> Statussen naar `luna`.
9. Controleer `input_select.luna_language_taal`.
10. Kies de gewenste taal.
11. Test Luna eerst zonder fysieke bediening, planneruitvoering, zelfherstel en AI.
12. Configureer daarna pas optionele functies één voor één.

---

## 18. Installatie geslaagd

De basisinstallatie is geslaagd wanneer:

- Home Assistant zonder fouten start;
- Luna-entiteiten beschikbaar zijn;
- de Luna-taal geselecteerd kan worden;
- Luna-statusvelden functioneren;
- er geen ongewenste fysieke acties plaatsvinden;
- optionele functies uit blijven totdat je ze bewust configureert.

Vanaf dat punt kun je Luna gecontroleerd verder koppelen aan de eigen Home Assistant-installatie.

---

## Belangrijkste regel

**Eerst installeren en controleren. Daarna pas apparaten, planneruitvoering, zelfherstel of lokale AI activeren.**
