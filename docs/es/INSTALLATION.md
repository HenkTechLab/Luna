# Luna - guía de instalación para Home Assistant

## Instalación con un solo comando

Abra la **App Terminal & SSH** de Home Assistant y ejecute:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- es
```

No es necesario clonar previamente el repositorio. El instalador descarga Luna, crea una copia de seguridad e instala los archivos en `/config/luna`.

## Qué se instala

- paquetes Luna y los siete módulos de idioma
- documentación
- exportaciones/referencias saneadas
- dashboard Luna basado en el dashboard de Luna Test

`automations.yaml` y `scripts.yaml` existentes no se sobrescriben a ciegas. `luna_test_*` permanece como material de prueba/referencia desactivado.

## Registro de paquetes

Si los paquetes Luna todavía no están registrados, el instalador muestra el bloque exacto que debe añadirse bajo la sección existente `homeassistant:` -> `packages:`. No cree una segunda sección `homeassistant:`.

## Dashboard

El instalador coloca el dashboard en:

```text
/config/luna/dashboard/luna-dashboard.yaml
```

Por seguridad no se modifican los archivos internos `.storage`. Si el dashboard todavía no está registrado, el instalador muestra el bloque `lovelace:` necesario. Después del registro, validación y reinicio, **Luna** aparece en la barra lateral.

## Verificación

1. Valide la configuración de Home Assistant.
2. No reinicie si existe un error.
3. Reinicie después de una validación correcta.
4. Abra el dashboard Luna.
5. Compruebe `input_select.luna_language_taal` y seleccione el idioma.

## Seguridad

El control físico, la ejecución del planificador, la autorrecuperación y la IA local permanecen fail-closed hasta que el usuario los configure expresamente. La IA local es opcional.
