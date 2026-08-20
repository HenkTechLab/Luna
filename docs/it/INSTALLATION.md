# Luna - guida di installazione per Home Assistant

## Installazione con un solo comando

Aprire l'**App Terminal & SSH** di Home Assistant ed eseguire:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- it
```

Non è necessario clonare prima il repository. L'installer scarica Luna, crea un backup e installa i file in `/config/luna`.

## Cosa viene installato

- package Luna e tutti i sette moduli linguistici
- documentazione
- esportazioni/riferimenti ripuliti
- dashboard Luna basato sul dashboard Luna Test

I file `automations.yaml` e `scripts.yaml` esistenti non vengono sovrascritti alla cieca. `luna_test_*` rimane materiale di test/riferimento disattivato.

## Registrazione dei package

Se i package Luna non sono ancora registrati, l'installer mostra il blocco esatto da aggiungere nella sezione esistente `homeassistant:` -> `packages:`. Non creare una seconda sezione `homeassistant:`.

## Dashboard

L'installer colloca il dashboard in:

```text
/config/luna/dashboard/luna-dashboard.yaml
```

Per sicurezza i file interni `.storage` non vengono modificati. Se il dashboard non è ancora registrato, l'installer mostra il blocco `lovelace:` necessario. Dopo registrazione, verifica e riavvio, **Luna** appare nella barra laterale.

## Verifica

1. Validare la configurazione di Home Assistant.
2. Non riavviare in presenza di errori.
3. Riavviare dopo una validazione riuscita.
4. Aprire il dashboard Luna.
5. Verificare `input_select.luna_language_taal` e selezionare la lingua.

## Sicurezza

Controllo fisico, esecuzione del planner, autoripristino e AI locale rimangono fail-closed finché l'utente non li configura intenzionalmente. L'AI locale è opzionale.
