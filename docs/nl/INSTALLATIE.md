# Luna - installatiehandleiding voor Home Assistant

## Eén commando

Open de **Terminal & SSH App** in Home Assistant.

Native dashboard, zonder extra frontend-afhankelijkheden:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl native
```

Custom dashboard met Mushroom en card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- nl custom
```

Voor de custom variant moeten **Mushroom** en **card-mod** via HACS beschikbaar zijn.

## Installer

De installer downloadt Luna, maakt een back-up, installeert packages, talen, documentatie, exports en beide dashboardbestanden onder `/config/luna`. Bestaande `automations.yaml` en `scripts.yaml` worden niet overschreven.

Als registratie in `configuration.yaml` nog nodig is, toont de installer het exacte ontbrekende blok. Interne `.storage` bestanden worden niet aangepast.

## Dashboards

- `luna-dashboard-native.yaml` - moderne standaard Home Assistant-kaarten.
- `luna-dashboard-custom.yaml` - uitgebreidere interface met Mushroom en card-mod.

## Controle

1. Controleer de Home Assistant-configuratie.
2. Herstart niet bij een configuratiefout.
3. Herstart na een geldige controle.
4. Open Luna in de zijbalk.
5. Controleer `input_select.luna_language_taal` en kies de gewenste taal.

## Veiligheid

Fysieke bediening, planneruitvoering, zelfherstel en lokale AI blijven fail-closed totdat de gebruiker deze bewust configureert.
