# HISTORY — from the first draft to today

Sources: `ptBR/NOTAS_PTBR.md` (per-version notes, kept in full), `git log`, and this working session.
Dates are commit dates; the PT-BR work before 2026-11-05 happened outside git (the repo starts with the upload of v4.0), and its early notes (before v2.15) were never itemised, so they are summarised from `NOTAS_PTBR.md`.

## 0. Base project (not ours)
- stoneboat65816's Vietnamese translation (2025-04 / 2025-07 uploads at the repo root): variable-width font, romaji ("furigana") mechanism, button-timing extras, serifu intro text. Our folders reuse its code and never modify it.

## 1. PT-BR, first stage: text only (draft → v2.x)
- **Draft:** 280 of 281 battle entries translated from the Japanese comments; fighter names; glossary (Rei Gan, Espada Espiritual, Mãos Sombrias, Mina do Dominador...). Nothing tested at that point.
- **serifu (intro text):** adapted, not translated literally (credits stoneboat, drops Vietnamese-specific text). Narrator texts (39 lines + 20 names) translated from Vietnamese.
- **ç glyph** drawn in the battle font (tile 41) and the dialogue font (glyph 38). `Yuyu_ptBR.bat` created to build next to the Vietnamese project.
- **Menu graphics** still in Vietnamese at this stage (square*, config, rank, preset, opening, ending, title).

## 2. PT-BR v2.15 → v2.45: menus, graphics, engine fixes
- v2.15-2.28: plates ("Livre", "Opções", rank "Classe"), fighter-select professions in a bigger/thin font, narrator colours, new VS graphic, key-config ring, name shadows, intro text colour, "Apresentado o PROJETO" screen.
- v2.17: battle text format `Nome 「fala」` (new 「 」 glyphs, widths in `tournament.asm`).
- v2.29-2.32: VS sprite sizes, defeat frames restored, Dimensão stripes traced to the special-DMA variables living in game RAM (moved to `$7F:FFD0`).
- v2.33: **romaji fix #1** — the 「 」 width was written over the romaji table; piece positions recomputed (45 lines).
- v2.34-2.41: Dimensão/credits corruption finally traced to data crossing the 64 KB bank limit; fixed with aligned static copies at `$F08000` / `$F09000`. Toguro 100% in the select screen, all profession lines redrawn.
- v2.42-2.45: team-order screens, "EQUIPE" credit, Ponta/Meio/Fim plate colours, Kurama's plant summon with romaji.

## 3. PT-BR v3.x: romaji everywhere
- v3.0 renumbering of 2.45. v3.1-3.11: 76 new ruby pieces (`Font/ruby_extra.bin`, codes `$76-$C1`), romaji over every move/line that has furigana in the Japanese original (Toguro, Kuwabara, Kamiya, Karasu, Yoko...).
- v3.12-3.15: VS graphic redone from the user's drawing and retouched by hand. v3.16: new brush-style "FIM". v3.17: Western name order (Yūsuke Urameshi) and macrons (Yūsuke, Tōya, Yōko).

## 4. PT-BR v4.0 → v5.7
- v4.0 (first version committed to git, 2026-11-05): title screen layout (copyright block and credit line down one tile row, "Relatório do Mundo Espiritual" raised), demo move list with Western names.
- v4.1a-j: battle checks against the original; narrator brackets 『 』 (codes `$F2/$F3`); `<name>` spacing rule (name + last letter); team header "TIME Toguro"; Ponta/Meio/Fim plates recoloured to indices 1,2,5,9; Cancelar without box.
- v5.0 consolidation; **v5.1 (2026-11-06): romaji repositioned (44 lines), IPS v5.1 published**, README with patch instructions and previews.
- v5.3-5.7: demo move list redone, ending cast/staff in Western order, Karasu "Trace Eye" piece fixes, opening credits (maioni / sniperdmaa), final credits "Projeto em pt-BR".

## 5. PT-BR v6.0 → v6.6 (2026-11-09)
- v6.0-6.4: every menu plate redrawn in the game's thin font (modes, arenas, Continuar/Desistir, sound screen, key-config bars, Tipo 1/2). v6.3 fixed an overflow of bank `$C8` (config_set too big) that corrupted palettes.
- v6.5: names back to white-on-grey (shared tiles between sound and select screens); tournament text speed.
- v6.6 (IPS v6.6, preview and README updated): Livre plate hand-drawn from the user's reference, arena boxes, TIME header for Toguro, loser's team header bug fixed in `load_team_name`, "Apresentando o" on the presentation screen.

## 6. English (enUS) 2026-11-10 → 11
- 2026-11-10: English draft of battle text, names, intro and narrator (v0.1, text only) → full build project copied into `enUS/` → v0.2 (English opening/title/ending graphics) → menu plates, arenas, fighter titles, END screen, tournament texts, key-config screen → IPS v0.3 renamed **v0.8** (matches build number) → preview and README.
- 2026-11-11: **v0.9** select-screen titles (Hiei "Jagan - Flying Shadow", Kamiya Doctor, Hagiri Sniper, Yoko Demon Fox, young Genkai Masked Fighter), Jin "Wind Master", Itsuki "Gatekeeper", names centred, Toguro labels.

## 7. Joint v0.9 (EN) / v7.0 (PT) — 2026-11-11 → 12
- ptBR v6.7 (select-screen titles) renamed **v7.0** on 2026-11-11.
- Fight HUD labels under the bars: first "Life/Spirit/Energy", then the orb research (red 愛 = vitality, teal 気 = balance, yellow 霊 = spirit energy) led to the user's choice **kanji + abbreviation** (HP / Bal BP / Energy MP; HP / Equi BP / Energia MP); orbs explained in READMEs and a new tutorial page; labels re-centred.
- Romaji: EN got furigana over 137 + 33 lines (ported from PT placement), PT +32 lines; today's simulation of the engine found overlapping pieces in 24 EN / 4 PT lines (fixed 23 + 3), including "Rei Gan".
- Move list text starts at x=40; Hiei "Evil Flame".
- Title: credit line `V0.9 EN-US 2026 MAIONI / SNIPERDMAA - STONEBOAT 2017-2025` (PT `V7.0 ...`), top text raised 6 px, EN SPECIAL EDITION gradient copied from PT, "Ghost Files" redrawn (the "s" looked like a "2").
- Battle text fixes from the user's screenshots (Ura-otoko lines, "Broke through!!", Kage spacing, PT spirit-attack wording).
- `docs/SPEC.md`, `docs/PLAN.md`, `docs/HISTORY.md` and `tools/` added.

## Version map
| Line | Versions | Last IPS |
|---|---|---|
| PT-BR | draft, 2.15-2.45, 3.0-3.17, 4.0-4.5, 5.0-5.7, 6.0-6.6, 6.7 → **7.0** | `ptBR/patch/Yuyu_PTBR_v7.0.ips` |
| EN-US | 0.1, 0.2, 0.3→0.8, **0.9** | `enUS/patch/Yuyu_enUS_v0.9.ips` |
