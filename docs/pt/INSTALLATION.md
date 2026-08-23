# Instalar Luna com HACS

HACS é o método suportado para instalar e atualizar Luna. O repositório deve ser público, pois o HACS não oferece suporte a repositórios privados.

1. No HACS, adicione `HenkTechLab/Luna` como repositório personalizado do tipo **Integration**.
2. Baixe Luna e reinicie o Home Assistant.
3. Abra **Definições → Dispositivos e serviços → Adicionar integração**, adicione **Luna** e escolha Native ou Custom.
4. Registe os packages e o painel escolhido em `configuration.yaml` com os blocos do [guia principal](../../INSTALLATIE.md).
5. Valide a configuração do Home Assistant antes de reiniciar.

Custom requer Mushroom e card-mod através do HACS. As atualizações são feitas integralmente pelo HACS, sem shell, curl ou instalador separado.

