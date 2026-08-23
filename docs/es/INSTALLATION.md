# Instalar Luna con HACS

HACS es el método compatible para instalar y actualizar Luna. El repositorio debe ser público, ya que HACS no admite repositorios privados.

1. En HACS, añade `HenkTechLab/Luna` como repositorio personalizado de tipo **Integration**.
2. Descarga Luna y reinicia Home Assistant.
3. Abre **Ajustes → Dispositivos y servicios → Añadir integración**, añade **Luna** y elige Native o Custom.
4. Registra los paquetes y el panel elegido en `configuration.yaml` con los bloques de la [guía principal](../../INSTALLATIE.md).
5. Valida la configuración de Home Assistant antes de reiniciar.

Custom necesita Mushroom y card-mod mediante HACS. Todas las actualizaciones se realizan con HACS, sin shell, curl ni instalador independiente.

