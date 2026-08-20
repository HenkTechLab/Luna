# Luna - guide d'installation pour Home Assistant

## Installation en une commande

Ouvrez l'**App Terminal & SSH** de Home Assistant et exécutez :

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- fr
```

Il n'est pas nécessaire de cloner le dépôt. L'installateur télécharge Luna, crée une sauvegarde et installe les fichiers dans `/config/luna`.

## Éléments installés

- packages Luna et les sept modules linguistiques
- documentation
- exports/références nettoyés
- tableau de bord Luna basé sur le tableau de bord Luna Test

Les fichiers `automations.yaml` et `scripts.yaml` existants ne sont jamais écrasés aveuglément. `luna_test_*` reste du matériel de test/référence désactivé.

## Enregistrement des packages

Si les packages Luna ne sont pas encore enregistrés, l'installateur affiche le bloc exact à ajouter dans la section existante `homeassistant:` -> `packages:`. Ne créez jamais une deuxième section `homeassistant:`.

## Tableau de bord

L'installateur place le tableau de bord ici :

```text
/config/luna/dashboard/luna-dashboard.yaml
```

Pour des raisons de sécurité, les fichiers internes `.storage` ne sont pas modifiés. Si le tableau de bord n'est pas enregistré, l'installateur affiche le bloc `lovelace:` nécessaire. Après enregistrement, validation et redémarrage, **Luna** apparaît dans la barre latérale.

## Vérification

1. Validez la configuration Home Assistant.
2. Ne redémarrez pas en cas d'erreur.
3. Redémarrez après validation réussie.
4. Ouvrez le tableau de bord Luna.
5. Vérifiez `input_select.luna_language_taal` et sélectionnez la langue.

## Sécurité

Le contrôle physique, l'exécution du planificateur, l'auto-récupération et l'IA locale restent fail-closed jusqu'à leur configuration volontaire par l'utilisateur. L'IA locale est facultative.
