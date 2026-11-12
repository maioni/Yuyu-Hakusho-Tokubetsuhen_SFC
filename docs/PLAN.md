# PLAN / HISTORY — Yū Yū Hakusho Tokubetsu-hen translations

Working log. Update it at the end of every work session. Full chronology: see `docs/HISTORY.md`.

## Done (newest last)
- v0.9 EN / v7.0 PT: title credit line (maioni / sniperdmaa, based on stoneboat), battle-text fixes from the user's screenshots.
- Orb research from Japanese screenshots, GameFAQs and the original battle text; HUD label scheme chosen by the user (kanji + abbreviation).
- HUD labels under the bars built and centred as far as the 16-column budget allows; README / NOTAS documented the orbs; tutorial page about the orbs added (EN and PT).
- Title: credit text, top text moved up 6 px (behind-the-flame problem), EN SPECIAL EDITION gradient matched to PT, "Ghost Files" redrawn.
- Romaji: "Rei Gan" overlap fixed; simulation of the piece-placement engine run over all lines (24 EN / 4 PT lines with lost ink; 23 + 3 fixed).
- `docs/` and `tools/` added so decisions and scripts are no longer only in a chat session.

## Open items
1. **Tutorial 4th line glitch** (all dialogue boxes): the 4th text line shows a horizontal line through the letters. The original also has 4-line pages (25 pages with 3 `<line>`); the box clears 0x1000 bytes (4 lines x 64 tiles). Suspect: the dialog tilemap (`serifu_map.bin`) rows or the tile offset of line 4. Next step: compare rendered VRAM of line 4 against the map.
2. **PRESS START / PRESSIONE START** should look the same in both versions (size, font, position). Find where the text is stored first (blinking DMA to VRAM `$6220`, see SPEC).
3. Title element positions differ between EN and PT (logo, banner, press start); user noticed, wants them aligned.
4. "Mine of the Ruler" / "Mina do Dominador" ruby overlap.
5. Visual check in game of the 26 romaji lines changed (Rose Whip, Yo-Yo, bombs, Bui, Kamiya, Hagiri, Sensui).
6. Black screen after the Sensui demo / ending FIM screen (to investigate).
7. Yellow orb letter never confirmed in game (MP kept as in stoneboat's version).
8. User actions: delete remote branch `ptbr-translation`; decide what to do with the old `...-main` folder (never delete without explicit confirmation).

## Working rules
- Update only the project folder without `-main`; never touch the old one.
- After any ROM change: regenerate both IPS, verify IPS-on-JP equals the build, copy changed files to the PC folder, commit and push.
- Commit trailers: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` and `Claude-Session: ...`.
- Verify visually (emulator screenshot) before telling the user something is fixed; say plainly what was not verified.
