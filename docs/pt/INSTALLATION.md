# Luna - guia de instalação para Home Assistant

## Um único comando

Abra a **App Terminal & SSH** no Home Assistant.

Dashboard nativo sem dependências frontend adicionais:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- pt native
```

Dashboard custom com Mushroom e card-mod:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- pt custom
```

A variante custom requer **Mushroom** e **card-mod** através do HACS.

## Instalador

O instalador transfere Luna, cria um backup e instala packages, idiomas, documentação, exportações e ambos os dashboards em `/config/luna`. Os ficheiros `automations.yaml` e `scripts.yaml` existentes não são substituídos.

Se `configuration.yaml` ainda precisar de registo, o instalador mostra o bloco exato. Os ficheiros internos `.storage` não são modificados.

## Dashboards

- `luna-dashboard-native.yaml` - cartões modernos padrão do Home Assistant.
- `luna-dashboard-custom.yaml` - interface mais rica com Mushroom e card-mod.

## Verificação

1. Valide a configuração do Home Assistant.
2. Não reinicie se existir um erro de configuração.
3. Reinicie após validação bem-sucedida.
4. Abra Luna na barra lateral.
5. Verifique `input_select.luna_language_taal` e selecione o idioma.

## Segurança

Controlo físico, execução do planeador, autorrecuperação e IA local permanecem fail-closed até serem configurados deliberadamente pelo utilizador.
