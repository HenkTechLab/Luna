# Luna - guida di installazione per Home Assistant

## Installazione sicura

Luna utilizza per impostazione predefinita un comportamento fail-closed. Controllo fisico, esecuzione del planner, autoripristino e inferenza AI locale rimangono disattivati finché l'utente non li configura intenzionalmente.

## Requisiti

- Installazione Home Assistant funzionante
- Accesso a `/config`
- Accesso a `configuration.yaml`
- Backup recente di Home Assistant

## Installazione

Copiare il repository sul sistema Home Assistant oppure eseguire:

```sh
sh install_luna.sh it
```

L'installer copia Luna in `/config/luna`, crea un backup dei file esistenti rilevanti e non sovrascrive mai alla cieca `automations.yaml` o `scripts.yaml`.

Se l'installer richiede una configurazione manuale, aggiungere i package Luna nella sezione esistente `homeassistant:` -> `packages:`. Non creare una seconda sezione `homeassistant:`.

## Automazioni, helper, script e Luna Test

`/config/luna/exports` contiene esportazioni sorgente/riferimento ripulite per automazioni, helper e script, incluso materiale `luna_test_*`. Questi file **non vengono attivati automaticamente** e non vengono uniti alla cieca a un'installazione Home Assistant esistente.

Il livello installabile sicuro si trova in `/config/luna/packages`.

## Verifica

1. Validare la configurazione di Home Assistant.
2. Non riavviare finché è presente un errore di configurazione.
3. Riavviare Home Assistant dopo una validazione riuscita.
4. Aprire Strumenti per sviluppatori -> Stati e cercare `luna`.
5. Verificare `input_select.luna_language_taal`.
6. Selezionare la lingua desiderata.

## AI locale

L'AI locale è opzionale. Verificare prima Luna senza AI. Solo successivamente configurare il backend locale e selezionare la modalità locale tramite `input_select.luna_ai_mode`.

## Importante

Installare e verificare prima Luna. Solo dopo configurare dispositivi, esecuzione del planner, autoripristino o AI locale.