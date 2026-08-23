# Luna installeren met HACS

HACS is de ondersteunde installatie- en updateroute. De repository moet openbaar zijn, omdat HACS geen privé-repositories ondersteunt.

1. Voeg in HACS `HenkTechLab/Luna` toe als custom repository van het type **Integration**.
2. Download Luna en herstart Home Assistant.
3. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen**, voeg **Luna** toe en kies Native of Custom.
4. Registreer de packages en het gekozen dashboard in `configuration.yaml` met de exacte blokken uit de [volledige installatiehandleiding](../../INSTALLATIE.md).
5. Controleer de Home Assistant-configuratie en herstart alleen als die geldig is.

Custom vereist Mushroom en card-mod via HACS. Updates verlopen volledig via HACS; shell, curl en een apart installatiescript worden niet gebruikt.

