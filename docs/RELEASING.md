# Como publicar uma versão

Este repositório não compila o app (o código é privado). Você gera os arquivos no projeto do app e publica aqui. O workflow `Release metadata` faz o resto sozinho.

## Convenção de nomes

- Tag: `v1.2.3` (versão semântica; versões de teste: `v1.2.3-beta.1`, marque como pré-lançamento).
- Arquivos: `NewbieMaps-1.2.3-win-x64.zip` e `NewbieMaps-1.2.3-win-x64.msi`.
- Só `.zip` e `.msi` entram nos metadados. Qualquer outro anexo é ignorado.

## Passo a passo

1. Gere o zip (e o MSI, quando existir) no projeto do app e teste num PC limpo.
2. Crie a release com os arquivos (no PowerShell, na pasta dos arquivos):

   ```powershell
   gh release create v1.2.3 .\NewbieMaps-1.2.3-win-x64.zip .\NewbieMaps-1.2.3-win-x64.msi `
     --repo EduCarvalhoO/newbiemaps --title "NewbieMaps 1.2.3" --notes-file .\notes.md
   ```

   Se só tiver o zip, passe só o zip. Para uma versão de teste, acrescente `--prerelease`.
3. A publicação dispara o workflow `Release metadata` (aba Actions), que:
   - baixa o `.zip` e o `.msi` da release;
   - calcula o SHA-256 e anexa `SHA256SUMS.txt` à release;
   - atualiza `latest.json` na `main` (só para a última versão estável, nunca para pré-lançamento).
4. Confira: a release tem o `SHA256SUMS.txt`, e `latest.json` mostra a versão nova.

## Se algo der errado

- **Workflow falhou:** abra a execução em Actions. Causas comuns: tag que não é versão (`main`, `1.2`), nenhum `.zip` ou `.msi` anexado, nome de arquivo com caractere estranho.
- **Gerar de novo:** Actions, `Release metadata`, `Run workflow`, informe a tag.
- **Publiquei o arquivo errado:** edite a release e volte para rascunho (ou apague só o anexo errado), anexe o certo e rode o workflow de novo. Não reutilize o mesmo número de versão para um arquivo diferente se alguém já baixou; publique a próxima.

## Como o site usa isso

O site lê `https://raw.githubusercontent.com/EduCarvalhoO/newbiemaps/main/latest.json` no navegador e mostra versão, tamanho, SHA-256 e os links de download. Enquanto `version` for `null`, os botões ficam em "Em breve".

## Mais tarde

Compilar e publicar automaticamente a partir do repositório do app (GitHub Actions) exige um token com acesso a este repositório guardado como segredo. Não é necessário agora.
