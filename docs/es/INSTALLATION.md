# Luna - guía de instalación para Home Assistant

## Instalación segura

Luna utiliza de forma predeterminada un diseño fail-closed. El control físico, la ejecución del planificador, la autorrecuperación y la inferencia de IA local permanecen desactivados hasta que el usuario los configure expresamente.

## Requisitos

- Instalación funcional de Home Assistant
- Acceso a `/config`
- Acceso a `configuration.yaml`
- Copia de seguridad reciente de Home Assistant

## Instalación

Copie el repositorio al sistema Home Assistant o ejecute:

```sh
sh install_luna.sh es
```

El instalador copia Luna a `/config/luna`, crea una copia de seguridad de los archivos existentes relevantes y nunca sobrescribe a ciegas `automations.yaml` o `scripts.yaml`.

Si el instalador indica que hace falta configuración manual, añada los paquetes de Luna bajo la sección existente `homeassistant:` -> `packages:`. No cree una segunda sección `homeassistant:`.

## Automatizaciones, helpers, scripts y Luna Test

`/config/luna/exports` contiene exportaciones de origen/referencia saneadas para automatizaciones, helpers y scripts, incluido material `luna_test_*`. Estos archivos **no se activan automáticamente** y no se fusionan a ciegas con una instalación existente de Home Assistant.

La capa segura instalable está en `/config/luna/packages`.

## Verificación

1. Valide la configuración de Home Assistant.
2. No reinicie mientras exista un error de configuración.
3. Reinicie Home Assistant después de una validación correcta.
4. Abra Herramientas para desarrolladores -> Estados y busque `luna`.
5. Compruebe `input_select.luna_language_taal`.
6. Seleccione el idioma deseado.

## IA local

La IA local es opcional. Compruebe primero Luna sin IA. Después configure el backend local y seleccione el modo local mediante `input_select.luna_ai_mode`.

## Importante

Primero instale y compruebe Luna. Solo después configure dispositivos, ejecución del planificador, autorrecuperación o IA local.