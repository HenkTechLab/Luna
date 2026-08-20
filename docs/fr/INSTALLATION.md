# Luna - guide d'installation pour Home Assistant

## Installation sécurisée

Luna fonctionne par défaut en mode fail-closed. Le contrôle physique, l'exécution du planificateur, l'auto-récupération et l'inférence IA locale restent désactivés jusqu'à ce que l'utilisateur les configure volontairement.

## Prérequis

- Installation Home Assistant fonctionnelle
- Accès à `/config`
- Accès à `configuration.yaml`
- Sauvegarde récente de Home Assistant

## Installation

Copiez le dépôt sur le système Home Assistant ou exécutez :

```sh
sh install_luna.sh fr
```

L'installateur copie Luna vers `/config/luna`, sauvegarde les fichiers existants pertinents et n'écrase jamais aveuglément `automations.yaml` ou `scripts.yaml`.

Si l'installateur demande une configuration manuelle, ajoutez les packages Luna sous la section existante `homeassistant:` -> `packages:`. Ne créez pas une deuxième section `homeassistant:`.

## Automatisations, helpers, scripts et Luna Test

`/config/luna/exports` contient des exports source/référence nettoyés pour les automatisations, helpers et scripts, y compris `luna_test_*`. Ces fichiers ne sont volontairement **pas activés automatiquement** et ne sont pas fusionnés aveuglément avec une installation Home Assistant existante.

La couche d'installation sûre se trouve dans `/config/luna/packages`.

## Vérification

1. Validez la configuration Home Assistant.
2. Ne redémarrez pas tant qu'une erreur de configuration existe.
3. Redémarrez Home Assistant après validation réussie.
4. Ouvrez Outils de développement -> États et recherchez `luna`.
5. Vérifiez `input_select.luna_language_taal`.
6. Sélectionnez la langue souhaitée.

## IA locale

L'IA locale est facultative. Vérifiez d'abord Luna sans IA. Configurez ensuite le backend local et sélectionnez le mode local via `input_select.luna_ai_mode`.

## Important

Installez et vérifiez Luna d'abord. Configurez ensuite seulement les appareils, l'exécution du planificateur, l'auto-récupération ou l'IA locale.