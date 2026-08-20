# Luna - guía de instalación para Home Assistant

## Un solo comando

Abra la **App Terminal & SSH** en Home Assistant.

Dashboard nativo sin dependencias frontend adicionales:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- es native
```

Dashboard custom con Mushroom y card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- es custom
```

La variante custom requiere **Mushroom** y **card-mod** mediante HACS.

## Instalador

El instalador descarga Luna, crea una copia de seguridad e instala paquetes, idiomas, documentación, exportaciones y ambos dashboards en `/config/luna`. Los archivos `automations.yaml` y `scripts.yaml` existentes no se sobrescriben.

Si `configuration.yaml` aún necesita registro, el instalador muestra el bloque exacto. Los archivos internos `.storage` no se modifican.

## Dashboards

- `luna-dashboard-native.yaml` - tarjetas modernas estándar de Home Assistant.
- `luna-dashboard-custom.yaml` - interfaz más completa con Mushroom y card-mod.

## Verificación

1. Valide la configuración de Home Assistant.
2. No reinicie si existe un error de configuración.
3. Reinicie después de una validación correcta.
4. Abra Luna desde la barra lateral.
5. Compruebe `input_select.luna_language_taal` y seleccione el idioma.

## Seguridad

El control físico, la ejecución del planificador, la autorrecuperación y la IA local permanecen fail-closed hasta que el usuario los configure expresamente.
