# Installare Luna con HACS

HACS è il metodo supportato per installare e aggiornare Luna. Il repository deve essere pubblico, perché HACS non supporta repository privati.

1. In HACS aggiungi `HenkTechLab/Luna` come repository personalizzato di tipo **Integration**.
2. Scarica Luna e riavvia Home Assistant.
3. Apri **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**, aggiungi **Luna** e scegli Native o Custom.
4. Registra i package e la dashboard scelta in `configuration.yaml` usando i blocchi della [guida principale](../../INSTALLATIE.md).
5. Convalida la configurazione di Home Assistant prima di riavviare.

Custom richiede Mushroom e card-mod tramite HACS. Gli aggiornamenti avvengono interamente con HACS, senza shell, curl o installer separato.

