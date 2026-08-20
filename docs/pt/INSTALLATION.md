# Luna - guia de instalação para Home Assistant

## Instalação segura

Luna utiliza por padrão um comportamento fail-closed. Controlo físico, execução do planeador, autorrecuperação e inferência de IA local permanecem desativados até que o utilizador os configure deliberadamente.

## Requisitos

- Instalação Home Assistant funcional
- Acesso a `/config`
- Acesso a `configuration.yaml`
- Backup recente do Home Assistant

## Instalação

Copie o repositório para o sistema Home Assistant ou execute:

```sh
sh install_luna.sh pt
```

O instalador copia Luna para `/config/luna`, cria um backup dos ficheiros existentes relevantes e nunca substitui cegamente `automations.yaml` ou `scripts.yaml`.

Se o instalador indicar que é necessária configuração manual, adicione os packages Luna à secção existente `homeassistant:` -> `packages:`. Não crie uma segunda secção `homeassistant:`.

## Automações, helpers, scripts e Luna Test

`/config/luna/exports` contém exportações de origem/referência higienizadas para automações, helpers e scripts, incluindo material `luna_test_*`. Estes ficheiros **não são ativados automaticamente** e não são combinados cegamente com uma instalação Home Assistant existente.

A camada segura instalável encontra-se em `/config/luna/packages`.

## Verificação

1. Valide a configuração do Home Assistant.
2. Não reinicie enquanto existir um erro de configuração.
3. Reinicie o Home Assistant após uma validação bem-sucedida.
4. Abra Ferramentas de programador -> Estados e procure `luna`.
5. Verifique `input_select.luna_language_taal`.
6. Selecione o idioma pretendido.

## IA local

A IA local é opcional. Verifique primeiro Luna sem IA. Depois configure o backend local e selecione o modo local através de `input_select.luna_ai_mode`.

## Importante

Primeiro instale e verifique Luna. Só depois configure dispositivos, execução do planeador, autorrecuperação ou IA local.