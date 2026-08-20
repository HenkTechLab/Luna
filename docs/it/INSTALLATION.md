# Luna - guida di installazione per Home Assistant

## Un solo comando

Aprire l'**App Terminal & SSH** in Home Assistant.

Dashboard nativo senza dipendenze frontend aggiuntive:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- it native
```

Dashboard custom con Mushroom e card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- it custom
```

La variante custom richiede **Mushroom** e **card-mod** tramite HACS.

## Installer

L'installer scarica Luna, crea un backup e installa package, lingue, documentazione, esportazioni ed entrambi i dashboard in `/config/luna`. I file `automations.yaml` e `scripts.yaml` esistenti non vengono sovrascritti.

Se `configuration.yaml` richiede ancora la registrazione, l'installer mostra il blocco esatto. I file interni `.storage` non vengono modificati.

## Dashboard

- `luna-dashboard-native.yaml` - moderne schede standard di Home Assistant.
- `luna-dashboard-custom.yaml` - interfaccia più ricca con Mushroom e card-mod.

## Verifica

1. Validare la configurazione di Home Assistant.
2. Non riavviare se esiste un errore di configurazione.
3. Riavviare dopo una validazione riuscita.
4. Aprire Luna dalla barra laterale.
5. Verificare `input_select.luna_language_taal` e selezionare la lingua.

## Sicurezza

Controllo fisico, esecuzione del planner, autoripristino e AI locale rimangono fail-closed finché l'utente non li configura intenzionalmente.
