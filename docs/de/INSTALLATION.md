# Luna mit HACS installieren

HACS ist der unterstützte Installations- und Aktualisierungsweg. Das Repository muss öffentlich sein, da HACS keine privaten Repositories unterstützt.

1. Füge in HACS `HenkTechLab/Luna` als benutzerdefiniertes Repository vom Typ **Integration** hinzu.
2. Lade Luna herunter und starte Home Assistant neu.
3. Öffne **Einstellungen → Geräte & Dienste → Integration hinzufügen**, füge **Luna** hinzu und wähle Native oder Custom.
4. Registriere die Pakete und das gewählte Dashboard in `configuration.yaml` mit den Blöcken aus der [Hauptanleitung](../../INSTALLATIE.md).
5. Prüfe die Home-Assistant-Konfiguration und starte nur bei einer gültigen Konfiguration neu.

Custom benötigt Mushroom und card-mod über HACS. Updates erfolgen vollständig über HACS; Shell, curl und ein separates Installationsskript werden nicht verwendet.

