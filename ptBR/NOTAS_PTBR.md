# Yū Yū Hakusho Tokubetsu-hen — tradução PT-BR (rascunho)

## Arquivos
- `battle_text_PTBR.txt` — 280 das 281 entradas de `battle_text.txt` traduzidas (a entrada #136 não tem texto no original e foi mantida). Os comentários em japonês e os ponteiros não foram alterados.
- `battle_name_PTBR.txt` — nomes dos lutadores.
- `Yuyu_PTBR.tbl` — igual ao `Yuyuvn.tbl`, mas com `4100=ç` no lugar de `4100=ả`.

## O que você precisa saber antes de usar
1. **Não testei nada.** Não tenho o `main.asm`, o `atlas`, o `xkas` nem a ROM montada aqui. O script só foi conferido por estrutura (281 blocos, ponteiros intactos).
2. **O glifo "ç" não existe na fonte.** O texto usa "ç" em 14 entradas (#5, 22, 61, 65, 123, 148, 151, 171, 185, 197, 203, 206, 232, 269). Mapeei para o byte `41` (antes "ả"), mas é preciso redesenhar esse tile na fonte (`Font.rar` / `font.asm`). Os outros acentos (á à â ã é ê í ó ô õ ú) já existem na fonte vietnamita.
3. **Códigos `<$xx><$20>` removidos.** Nas falas com nomes de golpes em kanji, a versão vietnamita usa esses códigos para posicionar tiles especiais. Nas linhas em PT-BR usei texto simples. Se algum nome de golpe aparecer cortado ou desalinhado, é aí que olhar.
4. **Espaçamento de `<name>` é suposição.** Mantive `<name>` colado na palavra seguinte, como no vietnamita (parece que o jogo coloca um espaço depois do nome). Confirme no emulador.
5. **Larguras de caixa desconhecidas.** Mantive as linhas em até ~40 caracteres, mas português costuma ser mais longo. Verifique as maiores: #15, 73, 126, 130, 157, 203.
6. **Falas com "Nome: texto"** usam espaço depois dos dois-pontos (o vietnamita não usava). Se faltar largura, remova o espaço.

## Glossário usado
| Japonês | PT-BR |
|---|---|
| 霊丸 | Rei Gan |
| 霊光弾 | Bala de Luz Espiritual |
| 霊剣 | Espada Espiritual |
| 次元刀 | Espada Dimensional |
| 薔薇棘鞭刃 | Chicote de Rosas |
| 邪王炎殺剣 / 黒龍波 / 煉獄焦 | Espada / Dragão Negro / Purgatório do Rei Maligno |
| 呪氷〜 | Gelo Maldito: … |
| 修羅旋風拳 | Punho do Furacão Asura |
| 影ノ手 | Mãos Sombrias |
| 支配者機雷 | Mina do Dominador |
| オジギソウ | Mimosa |
| 戸愚呂 兄/弟 | Toguro Velho / Toguro Novo |
| 死々若丸 | Shishiwakamaru (nome curto na lista: Shishi) |
| 妖狐 | Yoko |

Escolhas incertas (revise com o japonês): 首位打者剣, 風華円舞陣, 魔哭冥獄奏, 爆吐髑触葬, 空拳, e o duplo uso de "Toguro Novo" no segundo e no terceiro nome da lista de `battle_name`.

## Origem do texto
Traduzi a partir dos comentários em japonês (`//`) e usei o vietnamita só para saber onde entram `<name>`, `<name2>` e quem fala em cada linha.

---

## serifu_PTBR.txt (texto de abertura)
- O `serifu.txt` original **não é diálogo do jogo**: é o texto de aviso que a versão vietnamita mostra ao iniciar (controles, direitos autorais, recursos extras, código-fonte). Não dá para traduzir literalmente, porque boa parte é específica do projeto vietnamita (leituras Hán-Việt, "Việt hóa", tradução de 2017, manual em vietnamita). Por isso **adaptei**:
  - Mantive: controles (START, A, cores com B/X/Y/L/R e Select), aviso de que é tradução de fãs gratuita e sem autorização da Nintendo/Namco, os 6 recursos extras de timing de botões, o link do canal e o aviso sobre o código-fonte.
  - Troquei: a explicação Hán-Việt por uma nota sobre os nomes (romanização japonesa para personagens, golpes traduzidos), e acrescentei o crédito ao autor vietnamês (stoneboat).
  - Removi: o texto sobre o manual, a versão de 2017 e a afirmação de ser "a única tradução".
- **Revise antes de publicar:** as frases sobre ser gratuita e sem lucro/doações valem para o *seu* projeto? Não há crédito de tradutor PT-BR; acrescente uma página com seu nome. A página dos 6 recursos só é verdadeira se o PT-BR for montado sobre o `main.asm` vietnamita.
- Mesmas regras do original: `<line>`, `<pause>`, `<clear2>` e `<end>` preservados; linhas com no máximo 35 colunas (o original chegava a 38). Cada vírgula/ponto/exclamação seguido de espaço conta como 1 coluna, porque a tabela tem esses símbolos com o espaço embutido.
- `serifu_PTBR.tbl` = `serifu.tbl` com `38=ç` no lugar de `38=ả`. **O tile do "ç" também precisa ser desenhado na fonte do diálogo** (16 ocorrências).
- `raw-kaiwa.txt` é o dump japonês (em Shift-JIS/CP932, por isso não abre como UTF-8) das mesmas 281 entradas de batalha que eu já tinha traduzido, e bate com os comentários do `battle_text.txt`. Não precisei traduzir de novo.

---

## Como montar (Yuyu_ptBR.bat)
Coloque na mesma pasta do projeto vietnamita (com as pastas `Font/`, `Opening/`, `Narrator/` etc. extraídas dos `.rar`, `atlas.exe`, `xkas.exe` e todos os `.asm`):
`Yuyu_ptBR.bat`, `battle_text_PTBR.txt`, `battle_name_PTBR.txt`, `serifu_PTBR.txt`, `Yuyu_PTBR.tbl`, `serifu_PTBR.tbl`.
- A ROM japonesa (2.097.152 bytes, já sem header) precisa se chamar `YuJ.smc`.
- A ROM final sai como `Yuyu_ptBR.smc`; a vietnamita (`Yuyu.smc`) não é tocada. O log vai para `log_ptBR.txt`.
- **Glifo "ç" (resolvido):** `Font/font01.bin` (batalha, tile `41`) e `Font/font0.bin` (diálogo, glifo `38`) foram corrigidos: o antigo "ả" virou "ç" (o "c" com cedilha na linha que sobrava). Substitua os dois arquivos na pasta `Font/` do projeto e rode o `.bat` de novo. Só esses dois glifos mudaram; o resto é idêntico ao original.
- Faltam os gráficos com texto (`Opening/`, `Ending`, `Tournament`, `Narrator`, título), que continuam em vietnamita.

---

## Textos dos menus (pacote Narrator) — `Narrator_PTBR.zip`
- A narração dos menus e os nomes dos lutadores estão em `Narrator/narrator00..38` e `name00..19` (`.txt` + `.bin`). Traduzidos: 39 falas do locutor + 20 nomes. Os `.bin` já saem prontos (gerei com um codificador que reproduz byte a byte os `.bin` originais). **Basta copiar os `.bin` para a pasta `Narrator/` do projeto e rodar o `Yuyu_ptBR.bat`** (o xkas lê os `.bin`; o `Insert.exe` só é necessário se você editar os `.txt`).
- Os `.txt` do pacote só têm o vietnamita, sem o japonês. **Traduzi a partir do vietnamita**, então vale revisar com o japonês. Pontos de dúvida: `narrator04` ("máy phụ" → "controle secundário", significado incerto) e `narrator15` (o original vietnamita tinha uma piada local, "Cơm tấm phải có sườn heo!", que troquei por uma fala neutra de locutor).
- Larguras conferidas em pixels com a tabela `font0_width`; nenhuma linha é mais larga que o maior valor do original. O espaço no banco ROM é suficiente (os textos ficaram menores).
- `narrator_PTBR.tbl` = `narrator.tbl` com `38=ç`.

## Ainda em vietnamita (gráficos, não são texto)
Rótulos de menu gravados como tiles 4bpp, a redesenhar: `Narrator/square00..15_set.bin` (Thiết lập, Đấu võ tự do, Độ khó, Âm thanh, Nút bấm, Kiểu 1/2, Tổng lực chiến, Đối nhân chiến, Giải đấu, Đội nhóm, Vòm đen, Rừng, Tiếp tục, Bỏ cuộc…), `config_set.bin`, `rank_set.bin`, `preset*.bin`; avaliações do final (`Tournament/end1/end2/ending0..4_set`); telas da abertura (`Opening/`), final (`Ending/`) e título.

## v2.15
- Placa "Livre": faixa agora escura e opaca (como na referência), texto centralizado e texto centralizado; "Opções": ruído removido (pixels ciano no topo e resto sob o "ç").
- Seleção de lutadores (preset.bin + code.asm name_table2/3): profissões redesenhadas em fonte maior e centralizadas; Toguro agora "Toguro (velho)" / "Toguro (novo)" na seleção; Genkai Jovem refeito; "Personagem Secreto" -> "Secreto"; "Árvore" (Itsuki).
- ATENÇÃO: code.asm é substituído (só as tabelas name_table2/name_table3 mudaram). Copie sobre o do repositório.
- Pendentes: 級 sob S/A/B e faixa VS cortada.
- Texto do topo (narrador): cores agora cinza (sombra $318C, texto $6F7B) em vez de azul-marinho. tournament.asm é substituído (só essas linhas mudam).

## v2.16
- Texto do topo (narrador): cores idênticas ao original (texto $4EB4, sombra $2D6B).

## v2.17
- Texto de batalha: "Nome: fala" -> `Nome 「fala」` (glifos 「 」 novos no font01.bin, posições $F0/$F1; larguras em tournament.asm, org $C090F0).
- Pendente: linha de furigana em romaji com o nome original do golpe.
- 'escapou por pouco' -> 'foi atingido de raspão' (golpe e onda de choque).
- Golpes do Hiei: 'do Rei Maligno' -> 'das Chamas Mortais' (Espada/Dragão Negro/Purgatório/Chamas Mortais...); 'Rei Maligno' sozinho mantido.

## v2.18 (rascunho)
- square03_set.bin (4096) e square10_set.bin (3072) preenchidos com zeros até o tamanho que o loader copia: antes o jogo lia lixo da ROM depois do fim do ficheiro (ruído nas pontas das placas Som/Modo/Trilha/Voz).

## v2.19
- Seleção de lutadores/voz: nomes e profissões agora usam a paleta 3 do BG3 (interior branco, borda cinza); o vermelho do sufixo "(novo)/(velho)" foi removido. preset.bin (tiles dos nomes) com índices remapeados; code.asm: bits de paleta das name_table1/2/3.

## v2.20
- Texto da introdução ("Aperte START se quiser pular..."): Opening/serifu_col.bin, cor 2 de $3DEF (cinza) para $0000 (preto). Se o padrão vietnamita for outro, substituir este ficheiro pelo original.
- Tela "Apresentado o / PROJETO / YU YU HAKUSHO": ordem nova (Apresentado o, PROJETO, logo abaixo). Opening/pres_tiles.bin e pres_map.bin refeitos.

## v2.21
- Narrator/square13_set.bin: "Cancelar" numa linha só (fonte 3x5 do próprio jogo), sem quebra "Cance-/lar".

## v2.22
- Tela de nível do computador: placas S/A/B agora trazem "Classe" (em vez do 級 apagado), faixa azul como no original (Narrator/rank_set.bin).

## v2.23
- VS da tela de abertura da luta substituído pelo novo desenho do usuário (48x32, 6 sprites; Narrator/square15_set.bin + square15_col.bin).

## v2.24
- Tela de controles: anel ao redor do direcional restaurado (como no projeto vietnamita); config_set.bin ganhou 18 tiles e o DMA passou de $2200 para $2440 bytes (code.asm, draw_keyconfig).

## v2.25
- Faixa "Livre": fundo cinza (como a referência do usuário) e texto branco com contorno escuro (Narrator/square01_set.bin).

## v2.26
- Texto de BG3 (ex.: "Começa o duelo decisivo!") agora branco: $B2:C612 = $7FFF. Para voltar ao cinza do original, use $4EB4 em tournament.asm.

## v2.27
- Placas de nome do lado direito (COM): sombra passou de $4EB4 (cinza claro) para $2D6B (cinza escuro), igual à placa da esquerda ($B2:C62A).

## v2.28
- Nomes em fonte grossa nas placas de personagem (entradas 6–17: Rinku…Yōko, incl. Toguro velho/novo, Hagiri) não tinham sombra; adicionada sombra cinza (valor 2) embaixo/à direita em Narrator/preset.bin.

## v2.29
- VS maior: 64x48 px (12 sprites) em vez de 48x32. Frame da animação reescrito em $80:FC90 e ponteiros em $80:E724/E728 redirecionados; square15_set.bin refeito.

## v2.30
- Linha solta do Hiei (邪王) agora "Chamas Mortais" (antes "Rei Maligno").
- Nomes das placas de personagem (entradas 6–17) mais finos: sombra cinza só no último pixel de cada traço e abaixo das letras (preset.bin refeito a partir da v2.27).
- VS/derrota corrigidos: na v2.29 o VS grande sobrescrevia as tiles do efeito de derrota (linhas 2–3 do square15_set) e a paleta. Agora o VS usa só as linhas 0–1 (8 sprites, 48x48), as tiles de derrota voltam ao original e a paleta mantém os índices originais (1,2,4,5,10–13) + cores do VS em 3,6,7,8. Os 4 ponteiros de animação ($80:E724/E726/E728/E72A) apontam para o novo quadro em $80:FC90.
- Falas de narração (<name>/<name2>) agora no formato `Nome 「texto」`, como as falas. 16 textos foram encurtados para caber (largura máx. 224 px): ver diff de battle_text_PTBR.txt.
- Furigana em romaji: 60 linhas de golpes ganharam os códigos <$NN><$20> da tabela de romaji que já existe na ROM (os mesmos índices do projeto VN), posicionados pela largura dos caracteres. Linhas com mais de 224 px de largura (ex.: Hiei "Dragão Negro das Chamas Mortais!!") transbordam para a área do furigana e deixam lixo no canto esquerdo.

## v2.31
- Dimensão (seleção de arena) sem listras: as variáveis da DMA especial (trigger/vram/size/adr/bank) estavam em $0250–$0258, que é RAM do próprio jogo (marcas da seleção). Quando o jogo gravava $FFFF ali, a DMA disparava com lixo e escrevia 512 bytes (0xC9, barramento aberto) em VRAM $6E00 = última linha de tiles do Dimensão. Variáveis movidas para $7F:FFD0–$FFD8 e o gatilho agora usa o valor $5AA5.

## v2.32
- Derrota corrigida: o quadro B ($80:E745, os dois riscos vermelhos do X da derrota) usa as tiles $0C/$0E/$20 do square15_set, que o VS grande da 2.30/2.31 sobrescrevia, e os ponteiros do quadro B também tinham sido redirecionados. Agora só os ponteiros do quadro A ($E724/$E728) vão para o VS novo; B e as tiles de derrota ficam originais.
- VS 60x35 px com 6 sprites (tiles 00–0B/10–1B), posicionado em y -26..+9 (acima do chão do cenário). Paleta mescla as cores originais (índices 1,2,4,5,10–13) com as do VS (3,6,7,8).

## v2.33
- Romaji dos golpes (linha de cima): causa dupla. (1) A largura de 「 」 ($F0/$F1) era gravada em $C0:90F0, que e o inicio da tabela de romaji e destruia as 2 primeiras linhas do "R" de "Rei" (virava "re"). Agora shift_font devolve 4 px para codigos >= $F0 e a tabela de romaji fica intacta (removido o `org $C090F0`). (2) O posicionamento dos pedacos de romaji foi recalculado com a largura correta de 「 」 (4 px): antes cada pedaco caia 1 tile antes do previsto e apagava a ultima letra do pedaco anterior (EnSa|tsu -> "EnStsu", Ren|G|oku -> "Renoku", Jao -> "Ja").
- 45 linhas com romaji reposicionadas (Yusuke, Kuwabara, Kurama, Hiei, Genkai, Rinku, Toya, Jin, Shishiwakamaru, Bui, Hagiri, Itsuki, Sensui, Yoko). Texto portugues inalterado, exceto 3 pontuacoes finais para caber em 224 px: Hiei "Dragao Negro das Chamas Mortais" (sem "!!"), Sensui "Chama Violeta" (sem "!") e Itsuki "conto com voce" (sem "!").

## v2.34
- Dimensão (miniatura da arena, sprites 12-15 do OAM, tiles $70-$7B do set square12 = VRAM $3700-$37FF) ainda saía com listras amarelas: nos dumps da VRAM os últimos 512 bytes do set (4096 B enviados por DMA em $3000) ficam com 0xC9, enquanto os 3584 primeiros estao corretos. Mesmo com a DMA especial corrigida na 2.31 isso continuou, entao a causa nao e a variavel colidindo.
- Contorno: load_frame12 agora tambem agenda um reenvio dos 512 bytes finais (square12_set+$E00 -> VRAM $3700) pelo gancho de DMA do final da NMI (dma_special), com 1 frame de atraso (gatilho $5AA4 -> $5AA5). A DMA principal continua igual.
- Tela VS: removido um residuo solto (≈33 px, sobra da conversao do VS) no canto inferior esquerdo da celula do sprite 7 (tiles $06/$16 do square15_set), que aparecia como um pontinho vermelho/branco ao lado esquerdo do "VS".

## v2.35
- Rinku, Devil Wheel: "Grande Roda" -> "Roda Demoníaca" (coerente com "Ioiô Demoníaco"); romaji reposicionado.

## v2.36
- Narrações com nome estouravam a caixa de 224 px (texto cortado no fim e lixo no romaji). Nomes de batalha (battle_name_PTBR.txt) encurtados: "Toguro Mais Velho"/"Toguro Mais Novo" -> "Toguro" e "Genkai Jovem" -> "Genkai" (o retrato indica qual é). Todas as narrações agora cabem em 224 px.
- Dois ajustes de pontuação para caber: "A erva Shimaneki brota dentro do corpo" (sem "!") e Toguro "Não vai achar meu coração né?" (sem vírgula).

## v2.37
- Dump da Dimensão com a 2.36: os 512 bytes finais do square12 (VRAM $3700) ficam com 0xC2 (barramento aberto) -> o reenvio direto da ROM lia de endereco invalido. Agora load_frame12 copia esses 512 bytes (square12_set+$E00) pela CPU para WRAM $7F:FC00 (mesmo tipo de leitura da copia principal, que funciona) e a DMA do fim da NMI envia de la, 1 frame depois.

## v2.38
- Causa real da caixa Dimensao (e do texto "como Urameshi Yusuke" dos creditos): `square12_set` (4096 B) e `gekishu01_set` (3072 B) atravessam o limite de 64K do banco (LoROM). Os bytes depois de $xx:FFFF continuam em $xx+1:8000, mas a leitura (CPU ou DMA) seguia para $xx+1:0000, que nao e ROM (barramento aberto / espelho errado). Por isso so os ultimos 512 B (Dimensao) e ~544 B (creditos) saiam errados. A v2.34-2.37 nao resolvia, pois liam do mesmo endereco.
- Novo `rom_copy` (copia ROM->WRAM em duas partes, continuando em $8000 do banco seguinte) usado por `load_frame12`; e `fix_dma_src` nos creditos (gekishu00/20 e todos os gekishuNN): se a fonte da DMA cruza 64K, copia para $7F:5000 e aponta a DMA para la. Sem custo quando nao cruza.
- Tela FIM: tiles 4-7 de `owari_set.bin` ainda tinham a metade de baixo do "HET" vietnamita (serifas e pontinho sob o FIM). Zerados.

## v2.39
- Selecao de lutadores: o Toguro 100% (entrada 20 de name_table2/3) usava os mesmos tiles do Toguro (novo) e mostrava "Toguro (novo)"; o original mostra "100%". Agora a 1a linha e "Toguro 100%" (tiles novos $2FB,$2FC,$2FE,$2FF,$300,$30D, que estavam vazios e sem referencia nas tabelas; o resto reaproveita os tiles de "Toguro"). Segunda linha continua "Irmao Mais Novo".

## v2.40
- Corrigido erro do xkas na 2.38/2.39: `LDX {rc_dst}` (LDX nao tem modo long); agora LDA + TAX.

## v2.41
- Dimensão / créditos: removidos rom_copy/fix_dma_src (v2.38-2.40, sem efeito na prática). `square12_set` (4096 B) e `gekishu01_set` (3072 B) agora têm cópia estática alinhada em `org $F08000` (square12_fix) e `org $F09000` (gekishu01_fix), no começo do banco $F0 (arquivo 0x380000, livre), sem cruzar 64K. load_frame12 copia de square12_fix com o mesmo laço do load_frame13 (LDA label,x longo); gekishu01 faz a DMA direto de gekishu01_fix.
- Seleção de personagem: TODAS as linhas de profissão e os sufixos "(velho)", "(novo)", "Jovem" foram redesenhados na fonte fina (1px + sombra cinza). Os tiles liberados do preset.bin foram reutilizados (219 tiles novos). name_table2/3 regeneradas (table3 = table2 deslocada 2 colunas). "Toguro 100%" mantido.

## v2.42
- Placas Ponta/Meio/Fim (preset2.bin) [corrigido na v2.44]: os índices deslocados -1 da v2.14 estão certos para a paleta dessa tela (a v2.42 voltou aos originais e deixou a moldura vermelha). Na v2.44 só a faixa cinza (índice 4) virou azul (índice 5, cor 33,123,189), como no original.
- Tela "A ordem de luta foi definida!": name_table4 (cabeçalhos "TIME <nome>") usava a paleta 0 do BG3 com os tiles de nome já remapeados para a paleta 3 (interior branco, borda cinza) -> fonte estranha. Agora os tiles de nome usam a paleta 3 (os tiles "TIME" 782-787 continuam na paleta 0). Se ainda ficar estranho, preciso do dump CGRAM dessa tela.

## v2.43
- Final: tela "STAFF" traduzida para "EQUIPE" (Ending/gekishu20_set.bin, 2bpp 16 tiles de largura; o texto original estava nas colunas 11-21 das linhas 1-3; o novo ocupa colunas 9-22, fonte serifada em negrito, tiles de valor 1).

## v2.44
- Placas Ponta/Meio/Fim: revertida a v2.42 (moldura vermelha); mantidos os índices da v2.14 e a faixa cinza do topo trocada pelo azul do original.

## v2.45
- Kurama 'invocou uma planta devoradora' (ponteiro #63): agora com 「 」 e romaji em cima (Shokuyō shokubutsu shōkan), como o original. Largura 223 px.

## v3.0
- Versao renumerada: conteudo da 2.45 passa a ser a 3.0. Proximas entregas: 3.1, 3.2...

## v3.1
- Romaji (linha de cima) adicionado nas falas que no original têm furigana: narração 上空 (Jō kū), "deu um soco poderoso" (Kiai / hai), "acendeu o espírito de luta" (Tō shi / mo), "aumentou o poder do soco" (Ryo ku), Yusuke "Não visitei o além à toa" (yo / mi).
- Kurama (planta devoradora) refeita: os códigos antigos ($25,$4D,$44,$24,$A1) apontavam para peças de outros golpes ou vazias. Agora usa peças novas Sho/kuyō/sho/kubu/tsu/shō/kan (Shokuyō shokubutsu shōkan).
- 15 peças novas de romaji gravadas em $C09FB0 (códigos $76-$84), Font/ruby_extra.bin, desenhadas com as letras da própria tabela.

## v3.2
- Nomes de golpes/habilidades sem fala (ex.: Punho Vazio, Disparo de Dedo, Rugido de Fúria, Corpo de Aço Explosivo) agora centralizados na caixa como no original (espaços à esquerda calculados pela largura; romaji reposicionado). Não centralizados por passarem de 224 px: "Substância do Prazer Cerebral", "Planta do Makai de folhas flutuantes", "Pólen da Erva Medicinal Demoníaca".

## v3.3
- Romaji em cima nos golpes do Toguro que faltavam: Corpo de Aço Explosivo (Baku niku kō tai) e Rugido de Fúria (Dogō, 2 linhas). Peças novas $85-$87 (Font/ruby_extra.bin agora com 18 peças). Punho Vazio (Kū ken) e Disparo de Dedo (Shi dan) já tinham.

## v3.4
- Romaji novo: Kuwabara "Espada Campeã de Rebatidas" (Shui da sha ken), "Espada, vem" (ken), "aumentou a defesa" (Bō gyo ryo ku), Toguro "coração" (Shin zō, 2 linhas), "Forma Defensiva" (Gotai). Peças $88-$90 (Font/ruby_extra.bin, 27 peças). Espada Espiritual (Rei ken) já estava certo.

## v3.5
- Romaji novo nas falas do Toguro: "Vamos decidir isto" (Shō bu), "Só um disfarce" (Gi tai), "absorveu/liberou energia demoníaca" (yō ki kyū shū / yō ki hō sha). Peças $91-$97 (Font/ruby_extra.bin, 34 peças).

## v3.6
- Romaji novo (furigana do original): ondas de choque (Shō geki ha), "Isso me desagrada" (ki), energia de luta/espiritual/demoníaca (Rei ki, yō ki, tō ki, mi, kyū shū, zen shin, chi kara, kōri), "ataque espiritual selado" (Rei geki). Peças $98-$9C (Font/ruby_extra.bin, 39 peças; "c" desenhado a partir do "o").

## v3.7
- Romaji novo: técnicas seladas (Waza fū), "Consegue ver meus movimentos" (mi), Rinku "Passeio com o cachorrinho" (inu san po), Bui "Mostre sua força" (hon ki), vitalidade/vida (tai ryo ku kai fuku), poder espiritual/demoníaco (Rei/yō ryo ku taka), esquivar/rebateu (Kō geki), "Morra" de Hiei/Toya/Toguro (shi), Karasu (Vá: yu; Granada de Mão: Pine apple; Bomba Subterrânea: Mu ddy Bo mb; Bomba Perseguidora: Trace Eye), "Não é páreo" do Shishiwakamaru (aite), Manto da Morte (Shide hago romo).
- Peças $99-$B0 (Font/ruby_extra.bin, 59 peças; "P" e "f" desenhados).

## v3.8
- Romaji novo: Kamiya (dissecar: kai bō; "Não vai sobrar ninguém": noko ke; "Veja bem": mi), Shinobu (yasu), Golpe de Mão (Shu tō), Mão Milagrosa (ki seki te), Arma de Ki Sólido (ki kō jū), Aura de Luz Sagrada (sei kō ki). Peças $B1-$B8 (Font/ruby_extra.bin, 67 peças).

## v3.9
- Tiro de Pedra (岩石): romaji Gan seki em cima, centralizado. Mãos Sombrias do Itsuki já tinham (Kage no te).

## v3.10
- Romaji novo: "invocou a mimosa do Makai" (Ma kai shō kan), Yoko "invocou uma planta sugadora" (kyū sho kubu tsu shō kan), Yoko "Hora do castigo" (ji kan), Semente da Erva Shimaneki (sō). Peça nova $B9 (ji); Font/ruby_extra.bin com 68 peças. "Planta do Makai de folhas flutuantes" segue sem romaji (texto largo demais).

## v3.11
- Romaji novo: Yoko "Eu vou te matar" (koro), Pólen da Erva Medicinal Demoníaca (yaku yō sō ka fun), Pólen da Flor Onírica (ka fun). Peças $BA-$BC; Font/ruby_extra.bin com 71 peças.

## v3.12
- VS refeito a partir do desenho novo do usuário: 48x32 completo (antes o desenho visível tinha só ~36x28 e parecia cortado nas laterais). 6 sprites 3x2 (tiles 00-0B/10-1B de square15_set), frame em $80:FC90 com x -24/-8/+8 e y -26/-10; quadro B e efeito de derrota inalterados.

## v3.13
- VS com os pixels retocados pelo usuário (8 pixels alterados sobre a 3.12).

## v3.14
- VS: contorno escuro (índice 1) fechado nas pontas que encostavam na borda dos sprites (34 pixels), principalmente a ponta direita da barra do S e o topo/base, que no jogo pareciam cortadas.

## v3.15
- VS: anel branco contínuo ao redor de toda a letra (pixels vizinhos ao contorno escuro viram branco) e rosa interno trocado por vermelho.

## v3.16
- Tela FIM: o FIM é 1 grupo de 4 sprites 16x16 (tiles 0,2,4,6) em x=208,y=176 (área de 32x32 px). Novo FIM branco em estilo pincel (inclinado, pontas irregulares) desenhado nos tiles 0-7 e 16-23 de `Ending/owari_set.bin` (índice 1 da paleta 6 = branco). Limite: 32 px de largura, por isso o FIM é pequeno; um maior exigiria mexer na rotina que monta o OAM.

## v3.17
- Ordem do nome: "Urameshi Yūsuke" -> "Yūsuke Urameshi" na seleção de lutadores (preset.bin, palavras trocadas pixel a pixel nos mesmos 12 tiles) e nos créditos (Ending/gekishu01_set.bin, linha "como Yūsuke Urameshi", recentralizada).
- Macrons padronizados: Yūsuke, Tōya, Yōko em battle_text_PTBR.txt (25 linhas, só texto PT), battle_name_PTBR.txt, Narrator/name00/06/17.txt e serifu_PTBR.txt. Créditos: "Youko" -> "Yōko" (gekishu04_set.bin).
- Créditos conferidos (sem alterar): ainda estão na ordem japonesa "Kuwabara Kazuma", "Minamino Shūichi", "Kamiya Minoru", "Hagiri Kaname", "Sensui Shinobu"; Toguro "Velho/Novo" nos créditos vs "(velho)/(novo)" na seleção. Nomes de dubladores e equipe ficam na ordem japonesa.

## v4.0
- Tela de título: bloco de direitos autorais + linha "pt-BR baseado em Stoneboat" descidos 1 linha de tiles (8 px), como no original. "PRESSIONE START" mantido no tamanho original (a versão menor foi revertida a pedido).
- Não feito (4.1): logotipo no estilo do original, chamas dos YU menores, "Relatório do Mundo Espiritual" menor, relevo em "EDIÇÃO ESPECIAL". Fundo mantido.
- "Relatório do Mundo Espiritual" subido 1 linha de tiles (8 px) para sair do alcance das chamas dos YU.
- Lista de golpes da apresentação (Opening/demo00_set.bin): "Urameshi Yūsuke" -> "Yūsuke Urameshi" (palavras trocadas e recentradas; cabeçalho [1]..[5] intacto). Demais demos (demo01-19) não alteradas.

## v4.1 (batalha: conferência com o original)
- #4 "Opa! <name> cambaleou!!": faltava espaço depois do nome (saía "Kuramacambaleou").
- #265 (Sensui, 紫炎弾): faltava o "!" final; "Chama Violeta!" passava de 224 px (230), então virou "Chama Roxa!" (~208 px).
- Romaji novo (furigana do original): "poder do golpe enfraqueceu" (i ryo ku), "toda a postura" (Kan zen / Tai sei), Minoru "vencer" (Ka), Kazuya "esperto" (chō shi). Peças $BD-$C1 (i, Ka, chō, Kan, Tai); Font/ruby_extra.bin agora com 76 peças.
- Narração com `<name> 「...」`: no original é o narrador (sem nome, 『』); mantida como estava.
- v4.1b: narrador da luta. As falas 『…』 do original (sem nome, dita pelo narrador) agora usam os glifos novos 『 』 (códigos $F2/$F3 em Font/font01.bin, largura 4 como 「 」; tbl: F200=『 F300=』) em vez de `Nome 「…」`. Ex.: 『Sensui foi atingido de raspão~~!!』. Onde cabe (pior caso: nome de 51 px, limite 224 px) vai o rótulo "Narrador 『…』" (13 linhas: #2,3,4,9,11,14,16,17,21,23,31,42,255); nas demais só 『…』.
- v4.1c: glifos 『 』 refeitos (5 px, colchetes aninhados) com largura 6 (code.asm shift_font); rótulo "Narrador" em 12 linhas; #15 "enche o corpo!!!", #63 sem "!" final, #68 "Erva Shimaneki grudou em <name>!" por causa da largura.
- Encurtadas por causa dos colchetes (passavam de 224 px): #73 "brota no corpo", #130 "se espalha!!", #157 "envolveu o local!!".
- v4.1d: o código <name>/<name2> já deixa uma folga no fim do nome (a rotina soma de novo a largura da última letra), por isso `『<name> foi…』` saía com espaço duplo. Agora `『<name>foi…』` (inclui #4 "Opa! <name>cambaleou!!", que na v4.1 eu tinha "corrigido" por engano). Largura do nome no cálculo = nome + última letra (Kuwabara = 57 px). Rótulo "Narrador" agora em 10 linhas.
- v4.1e: glifos 『 』 redesenhados a partir do original (colchetes duplos de 1 px, 6x12, largura 7 em shift_font). Romaji das falas 『…』 recolocado (as posições antigas foram calculadas com o layout `<name> 「`; com 『 o "Sho"/"kuyō" do Kurama se sobrepunham): peças reposicionadas sem sobreposição, com 1 tile de folga quando cabe. #68 sem "!" final e #130 "se espalha!" por largura.
- v4.1f: cabeçalho "TIME Toguro" (name_table4: toguro ani / otouto / otouto 100%): os tiles 2D70-2D75 / 2D80-2D85 guardam o sufixo "(velho)/(novo)" em fonte minúscula, que na faixa do cabeçalho vira "lixo". Agora o cabeçalho usa só as 5 colunas de "Toguro" (resto $0000); a tela de seleção continua usando as 8 colunas com o sufixo.
- Placas Ponta/Meio/Fim (sprites, paleta OBJ 14): na tela "Começa a próxima luta!" a paleta 14 tem azul=idx5, vermelho=idx6-8 e turquesa=idx9 (CGRAM do usuário). Os tiles atuais usam 6/7/8 na moldura (vermelho nessa tela); falta o CGRAM/OAM da tela de escolha ("Aperte A, X ou Y") para achar índices que funcionem nas duas.

## v4.1g – placas Ponta/Meio/Fim
Dump da paleta OBJ 14 nas duas telas de ordem: índices 6-8 mudam (azuis numa, vermelhos na outra). Só 1, 2, 5 e 9 são iguais. preset2.bin refeito só com esses índices (miolo teal=9, borda azul=5, contorno escuro=1).
Tambem idx 3 -> 2 (3 e rosa/cinza conforme a tela; paleta confirmada por dump da tela 'Comeca a proxima luta').
v4.1h: placas = tiles 32-43 (topo) + 48-59 (base); recolor so com idx 1,2,5,9; contorno superior do texto Meio/Fim recriado; tiles 0-31/64-87 restaurados.
v4.1i: texto 'Fim' redesenhado (F menor).
v4.1j: Cancelar sem caixa preta: square13_set.bin usa o corpo original do JP (tiles 76-79/92-95 do JP) e o texto Cancelar branco com sombra escura, sem fundo. Backup anterior: square13 da v4.1i.
v4.3: Cancelar com contorno escuro completo (sombra so embaixo ficou ilegivel).
v4.4: Toguro 'Meu coração está aqui...' (era 'é aqui').
v4.5: ruby 'Shinzō' das 2 falas do Toguro movido para cima de 'coração' (estava sobre outra palavra).

## v5.0
Consolida 4.1g–4.5: placas Ponta/Meio/Fim (indices 1,2,5,9; Fim redesenhado), Cancelar sem caixa (contorno completo), Toguro 'coracao esta aqui' + romaji sobre 'coracao'. Pendente (5.1): separar palavras do romaji.

## v5.1
Romaji reposicionado (44 linhas, sem <name>): modelo calibrado com 3 prints (peca = tile inicial do caractere anterior + 3); palavras novas do romaji separadas por >=6 px (gap 6/5/4/3 conforme coube). Linhas com <name> e 998/1010/1016 nao alteradas.

## v5.3 (inclui as mudanças da lista de golpes)
- Lista de golpes da apresentação (Opening/demo*_set.bin), refeita com as próprias letras da fonte da lista: cabeçalhos "Kazuma Kuwabara", "Minoru Kamiya", "Kaname Hagiri", "Shinobu Sensui" (nome antes do sobrenome, como Yūsuke Urameshi); Hiei: "Espada das Chamas", "Dragão das Chamas", "Purgatório das Chamas"; Rinku: "Roda Demoníaca"; Hagiri: "Tiro de Moeda/Dado/Pedra"; Toguro (novo e 100%): "Disparo de Dedo".
- Não coube na lista (limite de ~146 px na fonte): Espada Campeã de Rebatidas, Semente Mortal da Erva Shimaneki, Flauta Demoníaca/Gelo Maldito: Muro de Cristal, Muralha de Vento Explosivo, Machado ... Demoníaco, Mãos Sombrias..., Chute Cortante: Onda Rubra, nomes da Yōko. Ficaram como estavam.
- Batalha (Kuwabara): "Espada, vem!!" mantida (a pedido).

## v5.4
- Ending (Ending/gekishu*_set.bin): nomes do elenco de vozes e da equipe japonesa na ordem ocidental (Nome Sobrenome): Nozomu Sasaki, Shigeru Chiba, Megumi Ogata... e os créditos (Shūichi Sakurabuki, Yoshihiro Togashi, Toyo Isokawa...). "como Kuwabara Kazuma/Kamiya Minoru/Hagiri Kaname/Sensui Shinobu" agora "como Kazuma Kuwabara/Minoru Kamiya/Kaname Hagiri/Shinobu Sensui"; "(Minamino Shūichi)" -> "(Shūichi Minamino)". "Crystal Imai" mantido.
- Lista de golpes do Hagiri: 4º golpe "Shuriken" -> "Dardo" (o original japonês é ダーツ, igual à batalha).
- Karasu: romaji "Trace Eye" (Bomba Perseguidora) corrigido. A peça "Trace" tinha 36 px e era cortada em 32 (o "e" sumia) e a peça "Eye" caía em cima dela; "Trace" foi redesenhada em 32 px e as duas peças reposicionadas nas falas "Bomba Perseguidora!" (Karasu) e "Bomba Perseguidora 「Gigigigi!!」". Peça "Shide" (33 px) também ajustada para 32.

## v5.5
- Lista de golpes da Yōko: "Espada da Árvore Viva" -> "Espada do Espírito"; "Golpe do Demônio Arbóreo" -> "Golpe de Espinhos"; "Folhas Demoníacas" -> "Planta do Makai" (versões curtas dos nomes da batalha, que não cabem inteiros na lista). "Sensitiva Demoníaca" mantida.

## v5.6
- Abertura, telas "Elenco de vozes" (Opening/1..10.bin, 1bpp 256x96): nomes dos dubladores na ordem ocidental (Nozomu Sasaki, Shigeru Chiba, Megumi Ogata, Shigeru Nakahara, Nobuyuki Hiyama, Hisako Kyōda, Megumi Hayashibara, Reiko Kondō, Katsumi Suzuki, Toshiyuki Morikawa, Kappei Yamaguchi, Ryō Horikawa, Norio Wakamoto, Tesshō Genda, Tarō Arakawa, Eiji Sekiguchi, Kōji Tsujitani, Rokurō Naya) e personagens "como Yūsuke Urameshi / Kazuma Kuwabara / Minoru Kamiya / Kaname Hagiri / Shinobu Sensui". Palavras apenas trocadas de lugar (sem redesenhar), centralização preservada.
- Abertura, créditos da tradução (Opening/11.bin): "Uma tradução de maioni / sniperdmaa" + "baseado em" ao lado do logo STONE BOAT (URLs mantidas).
- Abertura, "PROJETO" (Opening/12.bin): "(Relatório do Mundo Espiritual)" (antes "...Mundo dos Espíritos").

## v5.7
- Karasu: no "Bomba Perseguidora!" o romaji "Trace Eye" saía sem espaço (peças coladas); peça "Trace" movida um tile para a esquerda (`Karasu <$AA><$20>「Bomba <$AB><$20>Perseguidora!」`), agora com 1 tile de intervalo como na outra fala.
- Créditos finais (Ending/gekishu23_set.bin): "Programação + versão em vietnamita", "Projeto original: StoneBoat" e nova linha "Projeto em pt-BR: maioni / sniperdmaa".
- Conferidos os nomes das telas de elenco/equipe do ending e do elenco da abertura: todos em ordem ocidental (Nome Sobrenome).

## v6.0 (parcial) – placas de menu fiéis ao original
- Narrator/square00–04,06–09_set.bin redesenhados com fonte fina estilo JP: Dificuldade/Som/Botões, Combate Solo/Equipe/Torneio/Campeonato, Livre/Opções.
- Modos: sem caixa escura; a imagem sob o texto foi reconstruída (PT+JP) e o texto fica direto por cima (transparente).
- Pendente: arenas (sq11), Continuar/Desistir (sq14), caixas Ponta/Meio/Fim, tela de som, listas da config de botões.
- v6.0: arenas (Floresta/Domo em square11, Colina/Dimensão em square12, paletas 0–3 de square11_col) com fonte fina e fundo transparente.
- v6.0: Continuar/Desistir (square14) com fonte fina.
- v6.0: placas Ponta/Meio/Fim (preset2.bin) refeitas como o original: bisel ciano, gradiente azul (paleta da ROM JP $19480C), fonte fina.
- v6.0: Continuar/Desistir (square14) conforme o ajuste manual do usuario (listras lilás, texto 1px abaixo).
- v6.0: arenas conforme ajuste manual do usuario (square11/12).
- v6.0: Dificuldade/Som/Botões conforme ajuste manual do usuario (fundo transparente, imagem continua atrás do texto).
- v6.0: modos (Solo/Equipe/Torneio/Campeonato) conforme ajuste manual do usuario.
- v6.0: modos com limpeza dos pixels de cor ao redor do texto (despeckle), moldura inferior original.
- v6.0: modos com os retoques manuais finais do usuario (print 768x672).
- v6.0: tela de botões: barras azuis ornamentais ao lado dos títulos (Soco/Defesa) copiadas do VN, cores do texto da Defesa (Tipo 1) como no JP (A vermelho, Y verde). config_set.bin +36 tiles (326), DMA do draw_keyconfig $2440 -> $28C0 (code.asm). Mapa do BG em VRAM $1C00 => limite 448 tiles.
- v6.0: Tipo 1/Tipo 2 (square05) com caixa menor e fonte fina como no JP; corrigida paleta (vermelho estranho no Soco) das celulas do mapa config.
- v6.0: tela de som: placas Modo/Estéreo/Mono/Trilha/Voz (square10) com fonte fina e moldura como no JP. Numeração (No.00) não alterada.
- v6.0: tela de som: placas voltam às posições do original JP (tournament.asm: grupos OAM Modo/Estéreo/Mono em $89D730 = valores JP; Trilha/Voz em $89D5C5/$89D5CE +16 px). ATENÇÃO: 'No.00' e nome (BG) ainda nas posições antigas (x=80/144); no JP estão em x=106/195.
- v6.1: bordas brancas completas nas placas da tela de som (Modo/Estéreo/Mono/Trilha/Voz).
- v6.1: tela de som: 'No.' e digitos redesenhados com a fonte do topo (Narrator/preset.bin), 'No.' na col 13, digitos na col 16, nome na col 25 (recua se tiver 8+ tiles); placas com borda completa. Testado em emulador (snes9x) com a ROM 5.7 + patches binarios equivalentes.
- v6.1: nomes do teste de voz refeitos na fonte do topo em Narrator/preset.bin (Yōko, Genkai Jovem, Toguro Velho, Toguro Novo, que apareciam na fonte antiga).
- v6.2: nome do personagem alinhado a esquerda, sempre na col 20 (o rotina de recuo foi removida).
- v6.3 (IMPORTANTE): o config_set.bin da v6.0-6.2 tinha 10432 bytes e estourava o banco $C8 (sobravam so 28 bytes), corrompendo as paletas que vem depois (square06..09/11_col) e o rank_set. Efeito: caixas de Modos vazias/azuis, placa da classe B quebrada no Nivel, cores erradas. Agora o config_set tem so os tiles usados (273 tiles = 8736 bytes) e o mapa foi renumerado; o DMA em draw_keyconfig usa #$2220. Sobram 572 bytes no banco.
- v6.3: Tipo 1/Tipo 2 sem sobras de cor (square05: tiles 5 e 22 limpos); "Esquiva"/"Aparar" com a primeira letra na cor certa (config_set); brilho amarelo das 3 caixas do menu de configuracoes igual ao original (square02/03/04); nomes na tela de som na mesma fonte fina de "No.00" (paleta 0, name_table1 e preset.bin).
- v6.4: placa 'Desistir' (square14) voltou a ter a moldura com o indice 10 (a que brilha em amarelo quando selecionada), igual a 'Continuar'.

## v6.5
- Nomes (Narrator/preset.bin): voltaram a tinta branca com borda cinza (indices 1/2 da paleta 3). Os tiles dos nomes (0xD8-0x1AD) sao COMPARTILHADOS entre a tela de som e as telas de selecao de lutador/equipe/ordem; a v6.2-6.4 os tinha em tinta "idx 2" (branca so na paleta 0), o que deixava os nomes cinza nas telas de selecao. Agora a tela de som tambem usa a paleta 3 para os nomes e para "No. 00" (code.asm: name_table1, `number` e #$2CC0). "Kurama" tem 6 pares de tiles na selecao: o 6o par agora e limpo (sobrava um ponto).
- tournament.asm: removido o ajuste "+16 px" de Trilha/Voz em $89D5C5/$89D5CE. Esses quadros de sprite sao os mesmos das etiquetas 1P/COM/2P (duelo, chaveamento): a etiqueta COM ficava 16 px a direita, cortada pela borda da tela. Na tela de som nao fazia diferenca visual (testado).
- Tela de botoes: "Esquiva"/"Aparar" sem pixels da cor trocada (tiles 251 e 264 do config_set); marca amarela no canto da faixa "Defesa" (tile 95 do config_set caia numa area da VRAM sobrescrita depois pelo jogo; movido para o tile 273). config_set = 274 tiles (8768 bytes); DMA do draw_keyconfig = #$2240.
- Falas do torneio (Narrator/narrator15-36): velocidade do texto 1 (antes 2/3) para o texto terminar de aparecer antes de a tela seguinte entrar; narrator27 encurtada ("e avança de fase!").

## v6.6
- Livre: faixa do texto agora continua a imagem da personagem (torso/fundo) em vez de cinza liso (square01_set.bin, 33 tiles únicos por célula).
- Pendentes: Toguro em fonte fina, brilho amarelo dos Modes (poucos pixels), posição do texto TIME, furigana, "Inacreditável!" repetido.
- 6.6 (cont.): caixas de arena Colina/Dimensão: linha superior da barra (tiles 24-31 e 84-91 de square12_set) refeita igual à de Floresta/Domo (brilho amarelo contínuo). Cabeçalho "TIME Toguro": o 5º tile (0x16e/0x16f e 0x17e/0x17f) continha o início de "(" -> viravam um "1"; criados tiles limpos 0x104/0x105 e 0x295/0x296 (name_table4). Rótulo "TIME" (tiles 0x30f/0x311/0x313) subido 1 linha para ficar na mesma linha de base do nome.
- 6.6 (cont.): "Toguro" (velho/novo/100%) nas telas de seleção agora na fonte fina (mesmos tiles do cabeçalho), sem o desenho decorativo antigo; tiles novos 0x104/105, 0x295/296 (5ª coluna limpa) e 0x297/298 (traço do "(" de velho); tick solto removido do "100%" (tile 0x2fc).
- 6.6 (cont.): Livre refeito conforme a referência do usuário: faixa cinza-claro lisa nas laterais e a imagem da personagem (torso) só na parte central, atrás do texto.
- 6.6 (cont.): cabeçalho 'TIME Toguro' agora distingue '(velho)', '(novo)' e '100%' (sufixos copiados da tela de seleção para name_table4, cols 10-14).
- 6.6 (cont.): placas Ponta/Meio/Fim na tela 'Começa a próxima luta' ficavam vermelhas (a paleta OBJ 14 dessa tela, em $285C00, tem vermelho nos idx 6-8). Agora idx 3,6,7,8 recebem os mesmos azuis da tela de ordem (tournament.asm, org $D0DC06/$D0DC0C). Se X/O/linha vermelha também mudarem de cor, avisar.
- 6.6 (cont.): Livre desenhado à mão: luva vermelha à esquerda, torso rosa listrado, cinto escuro e barriga atrás do texto, laterais cinza-claro lisas (ref. do usuário).
- 6.6 (cont.): revertido o patch de paleta ($285C00 = paleta do VS, o VS ficou azul). Em vez disso, as placas Ponta/Meio/Fim (preset2 tiles 16-31) só usam idx 5/9/2 (azuis iguais nas duas paletas).
- 6.6 (cont.): brilho amarelo dos Modes igualado nas 4 caixas (square06-09_set: linhas 45 e 59 da barra e borda direita da caixa Solo em idx 15). "Yūsuke Urameshi" (seleção de equipe e cabeçalho TIME) redesenhado na fonte fina (tiles 0x2a4-0x2b9). Narrator34: "Já chegamos à última luta das semifinais!" (evita "Inacreditável!" repetido); narrator32: "!!" -> "!". O gráfico OPTION/KEY-CONF é arte original em inglês do jogo, mantido.

## v6.6 (cont. final)
- square15: troca de paleta (VS vermelho; caixas Ponta/Meio/Fim azuis) — tiles 0-31 remapeados 6→14,7→12,8→15.
- preset2 revertido para a versão 6.5 (corrige tags 1P/2P/COM).
- "Tipo 1/Tipo 2" redesenhado em negrito (square05).
- Cabeçalhos "Time", Yōko e Genkai Jovem refeitos em fonte fina (preset.bin + name_table4).
- PENDENTE: na tela "A vitória ficou com a equipe…" o cabeçalho do time perdedor fica em branco; na ROM japonesa os dois lados mostram "<nome> チーム". Causa ainda não isolada.
- CORRIGIDO: cabeçalho vazio do time perdedor na vitória por equipes: $0258/$025A vinham com byte alto $FF; load_team_name agora mascara (AND #$00FF) e copia com MVN (rotina menor, cabe no lugar original). Testado no emulador.
- Abertura: "Apresentado o" -> "Apresentando o" (Opening/pres_tiles.bin / pres_map.bin; tiles agora 2bpp 16x16, chars novos a partir do tile 416; stream LZ decodificado/recodificado, validado no emulador).
- Gerador da ROM de teste agora aplica square00_set e square11_set (Floresta/Domo e Opcoes com a fonte pequena igual a Colina/Dimensao).

## v7.0 (ajustes finais)
- Rótulos do HUD de luta (kanji + sigla, nas cores das barras): 体力 HP (Pontos de Vida), 気 BP (Pontos de Equilíbrio), 霊 MP (Pontos de Energia Espiritual). Os orbs são os mesmos três: vermelho 愛 recupera 体力, azul-esverdeado 気 recupera 体勢 (equilíbrio) e amarelo 霊 recupera 霊気 (energia espiritual).
- Lista de golpes da abertura: o texto dos golpes começava no pixel 38/39, vazando para a coluna de tiles que não recebe a cor vermelha do golpe selecionado (pixels brancos à esquerda). Todas as linhas (demo00-19) agora começam no pixel 40.
- Romaji (furigana) nas 32 falas/golpes que ainda não tinham (peças tiradas do original japonês, posicionadas pela largura dos caracteres).
