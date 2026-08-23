# Luna

Luna is een veilige, lokale en fail-closed Home Assistant-laag voor status, leren, planning en optionele lokale AI. De primaire installatie- en updateroute is **HACS**.

## Installatie via HACS

> Voor HACS moet deze GitHub-repository openbaar zijn. Een privé-repository kan niet als HACS custom repository worden gebruikt.

1. Installeer HACS en herstart Home Assistant.
2. Open HACS, kies **Custom repositories** en voeg `HenkTechLab/Luna` toe als type **Integration**.
3. Open Luna in HACS, kies **Download** en herstart Home Assistant.
4. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen**, zoek **Luna** en kies een dashboardvariant.
5. Registreer eenmalig de Luna-pakketten en het gekozen dashboard volgens [INSTALLATIE.md](INSTALLATIE.md).
6. Controleer de Home Assistant-configuratie en herstart pas als die geldig is.

HACS installeert en actualiseert alle uitvoerbare Luna-bestanden onder `custom_components/luna/`. De oude shell- en curl-installatieroute wordt niet meer gebruikt.

## Dashboardvarianten

- **Native:** `luna-dashboard-native.yaml`, uitsluitend standaard Home Assistant-kaarten.
- **Custom:** `luna-dashboard-custom.yaml`, met Mushroom en card-mod. Installeer beide aanvullingen afzonderlijk via HACS.

Beide varianten blijven onderdeel van dezelfde Luna-installatie. De gekozen variant bepaalt alleen welk dashboardbestand je in Home Assistant registreert.

## Taalmodules

Luna bevat Nederlands, English, Deutsch, Français, Español, Italiano en Português. Kies de taal na installatie met `input_select.luna_language_taal`.

## Veiligheid

De standaardwaarden zijn fail-closed:

- fysieke bediening staat uit;
- zelfherstel staat uit;
- planneruitvoering staat uit;
- lokale AI-inference staat uit;
- ontbrekende apparaten, diensten of AI veroorzaken geen actie.

Koppel eigen entiteiten en activeer optionele functies pas nadat de basisinstallatie is gecontroleerd.

## Updates

Werk Luna bij vanuit HACS en herstart Home Assistant. Omdat packages en dashboards binnen de integration-map staan, worden ze samen met de Python-integratie bijgewerkt. Controleer na een update altijd eerst de Home Assistant-configuratie.

## Sensoren en apparaten koppelen

Open na de installatie **Instellingen → Apparaten en diensten → Luna → Configureren**. Kies daar aanwezigheid, temperatuur, energie, vermogen, agenda en eventuele extra sensoren of apparaten. Luna maakt vaste eigen bronentiteiten aan en registreert veranderingen van gekozen sensoren lokaal in de tijdlijn.

Het selecteren van apparaten geeft Luna nog geen toestemming om ze te bedienen. Fysieke bediening blijft fail-closed en uit totdat de gebruiker deze afzonderlijk activeert.

## Bronbestanden

- `packages/` en `dashboard/` zijn de leesbare bronbestanden.
- `custom_components/luna/resources/` bevat de identieke, door HACS beheerde kopieën die Home Assistant gebruikt.
- `exports/` bevat aanvullende geschoonde bronlogica en wordt niet automatisch geactiveerd.

## Documentatie

Zie [INSTALLATIE.md](INSTALLATIE.md) voor de volledige Nederlandstalige installatie- en testprocedure. Andere talen staan onder [docs/](docs/README.md).

