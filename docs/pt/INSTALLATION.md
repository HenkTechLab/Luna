# Luna - guia de instalação para Home Assistant

## Instalação com um único comando

Abra a **App Terminal & SSH** do Home Assistant e execute:

```sh
curl -fsSL https://raw.githubusercontent.com/HenkTechLab/Luna/main/install_luna.sh | sh -s -- pt
```

Não é necessário clonar previamente o repositório. O instalador transfere Luna, cria um backup e instala os ficheiros em `/config/luna`.

## O que é instalado

- packages Luna e os sete módulos de idioma
- documentação
- exportações/referências higienizadas
- dashboard Luna baseado no dashboard Luna Test

Os ficheiros `automations.yaml` e `scripts.yaml` existentes não são substituídos cegamente. `luna_test_*` permanece material de teste/referência desativado.

## Registo dos packages

Se os packages Luna ainda não estiverem registados, o instalador mostra o bloco exato a adicionar à secção existente `homeassistant:` -> `packages:`. Não crie uma segunda secção `homeassistant:`.

## Dashboard

O instalador coloca o dashboard em:

```text
/config/luna/dashboard/luna-dashboard.yaml
```

Por segurança, os ficheiros internos `.storage` não são modificados. Se o dashboard ainda não estiver registado, o instalador mostra o bloco `lovelace:` necessário. Após registo, validação e reinício, **Luna** aparece na barra lateral.

## Verificação

1. Valide a configuração do Home Assistant.
2. Não reinicie se existir um erro.
3. Reinicie após validação bem-sucedida.
4. Abra o dashboard Luna.
5. Verifique `input_select.luna_language_taal` e selecione o idioma.

## Segurança

Controlo físico, execução do planeador, autorrecuperação e IA local permanecem fail-closed até serem configurados deliberadamente pelo utilizador. A IA local é opcional.
