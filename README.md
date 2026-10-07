# RenameOS Desktop

Aplicação desktop para renomear e mover arquivos em lote com uma interface gráfica. Evolução do [script RenameOS](https://github.com/olegariobru/renameOs).

## Demonstração

![Interface de renomeação de arquivos](https://github.com/user-attachments/assets/34a79152-76da-4861-b423-7931de21f5f4)

![Interface de movimentação de arquivos](https://github.com/user-attachments/assets/81726b2e-4e06-4411-893c-ba9620bab39f)

## Funcionalidades

### Renomeação

- Seleção de múltiplos arquivos.
- Remoção de itens da seleção.
- Preenchimento com os nomes atuais.
- Contagem de arquivos e novos nomes.
- Validação de quantidade e detecção de destinos existentes.
- Preservação da extensão quando o novo nome não contém ponto.

### Movimentação

- Seleção de pastas de origem e destino.
- Seleção por lista TXT, nomes separados por vírgula ou quantidade.
- Prioridade de seleção: TXT, nomes digitados e quantidade.
- Exibição da quantidade de itens movidos.

## Tecnologias

Python 3, Tkinter, `os` e `shutil`. A execução do código-fonte não exige bibliotecas externas, mas requer uma instalação Python com Tkinter.

## Como executar

```bash
git clone https://github.com/olegariobru/renameOSnew.git
cd renameOSnew
python -m tkinter
python updateRenameOS.py
```

O primeiro comando Python verifica se o Tkinter está disponível e abre sua janela de demonstração.

## Como utilizar

Na aba **Renomear**, selecione os arquivos e informe um novo nome por linha, respeitando a ordem da lista. Confira a quantidade e confirme a operação.

Na aba **Mover Arquivos**, selecione origem e destino e informe um dos critérios. Em um TXT, utilize um nome completo por linha, incluindo a extensão.

Faça a verificação inicial com cópias: renomeações e movimentações alteram os arquivos diretamente.

## Organização

- `updateRenameOS.py`: interface e operações.
- `updateRenameOS.spec`: configuração de empacotamento.
- `build/` e `dist/`: artefatos de uma compilação anterior com PyInstaller.

## Limitações e próximos passos

- Não há testes automatizados nem rollback das operações.
- A seleção por quantidade usa a ordem retornada pelo sistema de arquivos.
- Separar interface e lógica de operações.
- Adicionar simulação, relatórios e tratamento mais completo de conflitos.
- Distribuir executáveis por releases e evitar versionar novos arquivos de build.

## Como contribuir

Abra uma issue com o problema ou a melhoria proposta. Para enviar código, crie um fork e uma branch, mantenha a alteração focada e abra um pull request explicando o resultado e como verificou o funcionamento.

## Licença

Este repositório ainda não contém um arquivo `LICENSE`. A licença de uso e redistribuição precisa ser formalizada pelo autor.

## Autor

[Bruno Olegário](https://github.com/olegariobru) · [LinkedIn](https://www.linkedin.com/in/bolgarimacedo/)
