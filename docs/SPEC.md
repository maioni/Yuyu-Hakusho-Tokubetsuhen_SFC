# SPEC — Yū Yū Hakusho Tokubetsu-hen (SFC): EN-US and PT-BR translations

Reference for how the project is built and the technical facts learned. Read this before changing anything.

## 1. Goal and scope
- Two translations of the SNES/SFC game, both based on stoneboat65816's Vietnamese project (repo root, never modified):
  - `enUS/` — English, version **1.0**, patch `enUS/patch/Yuyu_enUS_v1.0.ips`
  - `ptBR/` — Portuguese (Brazil), version **8.0**, patch `ptBR/patch/Yuyu_PTBR_v8.0.ips`
- Each folder is self-contained and builds with its own `.bat` (`Yuyu_enUS.bat` / `Yuyu_ptBR.bat`: Atlas inserts text, xkas applies code and graphics) on top of the headerless 2 MB Japanese ROM (`YuJ.smc`).
- The repo never contains the ROM. Credit line on the title: `V1.0 EN-US 2026 MAIONI / SNIPERDMAA - STONEBOAT 2017-2025` (PT: `V8.0 PT-BR ...`).
- User workflow: compile locally in `C:\Users\admin\Downloads\Yuyu-Hakusho-Tokubetsuhen_SFC`. The old `...-main` folder must not be touched.

## 2. ROM layout facts (LoROM, 2 MB base)
| Item | Location |
|---|---|
| Battle text (2-byte chars) | file offset `0x310000`; must end below `0x318000` (EN ends `0x313c0c`, PT `0x313eea`) |
| Serifu / tutorial text | file offset `0x320000`, single-byte table `serifu_PTBR.tbl` (UTF-8 BOM) |
| Title map / set | `title_map` at `0x290800` (2048 B), `title_set` at `0x291000` (15584 B) |
| Ruby (romaji) glyphs | `0x2010F0 + code*32` (4 tiles x 8 rows, 1bpp); width table `0x201000` |
| HUD label tiles / row | `0x382080` (17*32 B) / `0x3822C0` (64 B), via hooks in `code.asm` at `$F0:A000/A040` |
- Title tilemap is copied to WRAM `$7F:0000` and tiles to `$2000` (`redraw_title` in `code.asm`). Max 496 tiles in `title_set`.
- "PRESS START" is not in the title tilemap: it is blinked by DMA to VRAM `$6220` (`title.asm`); source still to be located.

## 3. Text formats
- Battle text: `battle_text_*.txt`, Atlas format with `#JMP/#WRITE` lines; `<name>` = fighter name; `<end>` ends a line. Lines starting with `//` are the original Japanese (ignored). No `'` exists in the battle font.
- Serifu text: tags `<line>`=F0, `<pause>`=F6, `<clear2>`=F5, `<end>`=FF. No `=` in the serifu font (use `:`). Characters `. ( ) : -` exist. A page may have up to 4 lines.
- Ruby (romaji) pieces: `<$XX><$20>` is ONE 16-bit word `0x20XX`. The engine copies 32 bytes (4 tiles) of glyph `XX` into a row buffer at the tile of the **previous drawn character's start x**, plus 1 tile. Placement rule (verified): `tile = (x_start_of_previous_char >> 3) + 1`. A later piece overwrites the last tiles of an earlier one, so a piece must start at `>= previous tile + ink tiles`. If it does not, letters are cut off (bug seen as "ReGan"). `tools/ruby/val2.py` checks this; `tools/ruby/fixr.py` fixes it by moving the piece one character to the right.
- Known leftover: the long "Mine of the Ruler" / "Mina do Dominador" line (5 pieces) still overlaps.

## 4. Fight HUD (labels under the bars)
- BG panel chars at VRAM `0xE000`, tilemap `0xF800`; free tile slots 207-223 (17 slots incl. blank, so max 16 unique 8-px columns of text). Label strip = tilemap row 30.
- Labels (kanji + abbreviation in the bar colours): red 体力 `HP`, blue 気 `Bal BP` (PT `Equi BP`), yellow 霊 `Energy MP` (PT `Energia MP`). Bar centre targets: x = 43, 128, 212; current centres EN (43,127,212) PT (43,131,212), limited by the 16-column budget.
- Meaning from the Japanese game: red orb 愛 = 体力 vitality (HP); teal orb 気 = 体勢 posture/balance (BP); yellow orb 霊 = 霊気 spirit energy (MP). The HP/BP/MP letters on the orbs and the R+direction recovery are stoneboat additions (`kaifuku` in `code.asm`: R+Left BP, R+Right spirit, R+Up HP).
- Build: `tools/hud/build_hud.py` (`make(strings, outdir, centers, gap)`), fonts in `hudlib.py`.

## 5. Title screen
- Credit line and logo text are rendered into `title_set/title_map`; tools in `tools/title/` (`apply.py` credit, `up.py` moves top text up, `grad.py` gives SPECIAL EDITION the same row gradient as EDIÇÃO ESPECIAL, `gf.py` redraws "Ghost Files").
- Palette indices of the banner text: 1 white, 12 cream, 11 gold, 15 dark gold, 13 brown; rows 104-112 gradient 1,1,12,12,11,11,15,13,13.

## 6. Tooling (all local, ephemeral paths under /tmp in the original session)
- `tools/ruby/atl.py` — mini Atlas (`insert(rom, txt, tbl)`).
- `tools/emu/mkips.py JP.smc new.smc out.ips` — IPS writer; always verify that applying the IPS to the JP ROM reproduces the new ROM.
- `tools/emu/emu.py` — snes9x libretro harness (screenshots, VRAM dump); `hud3.py`, `title4.py` boot to a fight / title screen.
- Patching a compiled ROM directly (without xkas): write the new bins at the offsets in section 2, then run `atl.insert` for text.

## 7. Terminology (decided)
- Orbs/HUD: 体力 Life Points = HP, 気 Balance Points = BP, 霊 Spiritual Energy Points = MP (documented in both READMEs and the tutorial page).
- Names: Japanese romanization (Yūsuke, Kurama...); special moves translated, with romaji above (ruby).

## Findings of 2026-11-13
- ROM size matters: a build whose size is not a power of two (e.g. the Vietnamese 3,309,568 B) shows garbage backgrounds in snes9x; padding with zeros to 4 MB fixes it (EN/PT at 3,678,976 B work).
- `enUS/Narrator/narratorNN.bin` / `nameNN.bin` are generated by `Narrator/Narrator.bat` (Insert.exe). `tools/narr/insert.py` is a Linux stand-in (verified byte-identical against the PT bins, except name bins that were hand-edited).
- Linux build without Atlas: copy the last real build, then `xkas -o rom main.asm` over it (xkas-plus from github.com/devinacker/xkas-plus). Needs `Font/furigana.bin` (from `Font.rar`) and `Opening/star.bin` (file is `Star.bin` in git; case matters on Linux).
- Sound screen: JP 'No.' + digit glyphs live at the end of `preset.bin` (VRAM $F200). Key-config header lines: `tools/cfg/hdrlines.py`.
- PT plate 'Combate Livre': `tools/plates/combate_livre.py` redraws `square01_set.bin`.
- Still open (not done): restore JP shaded A/B/X/Y icons on the KEY-CONFIG screen (needs separate palettes: JP uses more colours than the single 15-colour `config_col`), Rank plate frame, Type 1/2 plates (they are not in config_map; probably sprites), stray yellow/grey block between 'Weak' and 'high' on the EN key-config screen.
- Move-list icons (attract mode, `Opening/intro_bg1_*`): restored pixel-identical to JP: tiles VRAM $7AC0-$7BFF of `intro_bg1_set.bin` (offset $2C0), palettes 4-7 of `intro_bg1_col.bin`, map row 10 cols 2-3 = $1DB8,$1DB6. Reach the screen by waiting on the title (attract mode).
