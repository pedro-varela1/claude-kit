# 001 · Windows support
_2026-10-09_

Nesta máquina (Windows 11, sem admin nem Developer Mode), symlinks falham com WinError 1314 e
junctions funcionam. Os hooks do Claude Code rodam no Git Bash, ou no PowerShell quando não há Git
Bash. O `latexmk` do MiKTeX precisa de Perl: funciona no Git Bash e falha no PowerShell. As fontes
da casa não estavam instaladas e o PDF caía no fallback Latin Modern.

## Como estruturar a versão Windows do kit?
- **Kit multiplataforma** (recommended) **← chosen**: um único `install.py`/`settings.json` que
  detecta o Windows; a branch `windows` pode ser mergeada em `main`.
- **Variante só na branch**: a branch diverge de `main`, e cada mudança do kit seria feita duas
  vezes.

## Que tipo de link o instalador deve criar no Windows?
- **Directory junctions** (recommended) **← chosen**: sem admin nem Developer Mode, e todos os
  links do kit são diretórios.
- **Symlinks + Developer Mode**: adiciona um pré-requisito de sistema sem ganho para diretórios.
- **Cópia dos arquivos**: quebra o modelo "linked, not copied".

## O guard de details/ e as regras ask do LaTeX devem cobrir o tool PowerShell?
- **Cobrir Bash e PowerShell** (recommended) **← chosen**: matcher `Bash|PowerShell`, padrões de
  escrita do PowerShell, caminhos com `\` e regras `PowerShell(latexmk *)` etc.
- **Só o Bash, como hoje**: um comando PowerShell escreveria em details/ sem aprovação.

## Para o details.pdf nesta máquina: como resolver o TeX e as fontes?
- **MiKTeX + pacotes de fonte** (recommended) **← chosen**: instalar `sourceserif`, `sourcesans`
  e `stix2-otf` no MiKTeX; o README aceita TeX Live ou MiKTeX.
- **Instalar TeX Live**: vários GB, duplicado com o MiKTeX, mesmo PDF.
- **Deixar o fallback**: PDF fora do estilo da casa.
