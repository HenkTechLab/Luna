# Luna - guide d'installation pour Home Assistant

## Une seule commande

Ouvrez l'**App Terminal & SSH** dans Home Assistant.

Dashboard natif sans dépendance frontend supplémentaire :

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- fr native
```

Dashboard custom avec Mushroom et card-mod :

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- fr custom
```

La variante custom nécessite **Mushroom** et **card-mod** via HACS.

## Installateur

L'installateur télécharge Luna, crée une sauvegarde et installe les packages, langues, documents, exports et les deux dashboards sous `/config/luna`. Les fichiers `automations.yaml` et `scripts.yaml` existants ne sont pas écrasés.

Si `configuration.yaml` nécessite encore un enregistrement, l'installateur affiche le bloc exact. Les fichiers internes `.storage` ne sont pas modifiés.

## Dashboards

- `luna-dashboard-native.yaml` - cartes Home Assistant standard et modernes.
- `luna-dashboard-custom.yaml` - interface enrichie avec Mushroom et card-mod.

## Vérification

1. Validez la configuration Home Assistant.
2. Ne redémarrez pas en présence d'une erreur de configuration.
3. Redémarrez après validation réussie.
4. Ouvrez Luna depuis la barre latérale.
5. Vérifiez `input_select.luna_language_taal` et sélectionnez la langue souhaitée.

## Sécurité

Le contrôle physique, l'exécution du planificateur, l'auto-récupération et l'IA locale restent fail-closed jusqu'à leur configuration volontaire par l'utilisateur.
