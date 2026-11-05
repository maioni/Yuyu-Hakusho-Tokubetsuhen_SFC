# Tradução PT-BR (Yū Yū Hakusho Tokubetsu-hen, SFC)

Pasta autônoma com a tradução para português do Brasil, baseada no projeto vietnamita de stoneboat65816.
Nada fora de `ptBR/` foi alterado, então o projeto vietnamita continua intacto na raiz.

## Como montar
1. ROM japonesa sem header (2 MB), renomeada para `YuJ.smc`, dentro desta pasta.
2. Ferramentas: `atlas` e `xkas.exe` (as mesmas do projeto original).
3. Execute `Yuyu_ptBR.bat`. Resultado: `Yuyu_ptBR.smc`.

## Conteúdo
- `battle_text_PTBR.txt`, `battle_name_PTBR.txt`, `serifu_PTBR.txt` + `*.tbl`: textos em PT-BR.
- `code.asm`, `title.asm`, `tournament.asm`, `title_patch.asm`: código adaptado (romaji acima dos golpes, VS, FIM, etc.).
- `Font/`, `Narrator/`, `Opening/`, `Ending/`, `Tournament/`: gráficos já traduzidos (tiles 2bpp/4bpp).
- Demais `.asm`: iguais aos do projeto original, copiados para a pasta ser autossuficiente.
- `NOTAS_PTBR.md`: histórico de versões e decisões.

Créditos PT-BR: sniperdmaa / maioni. Projeto original: StoneBoat.
