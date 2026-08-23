# Installer Luna avec HACS

HACS est la méthode d’installation et de mise à jour prise en charge. Le dépôt doit être public, car HACS ne prend pas en charge les dépôts privés.

1. Dans HACS, ajoutez `HenkTechLab/Luna` comme dépôt personnalisé de type **Integration**.
2. Téléchargez Luna puis redémarrez Home Assistant.
3. Ouvrez **Paramètres → Appareils et services → Ajouter une intégration**, ajoutez **Luna** et choisissez Native ou Custom.
4. Enregistrez les packages et le tableau de bord choisi dans `configuration.yaml` avec les blocs du [guide principal](../../INSTALLATIE.md).
5. Validez la configuration Home Assistant avant de redémarrer.

Custom nécessite Mushroom et card-mod via HACS. Les mises à jour passent entièrement par HACS, sans shell, curl ni installateur séparé.

