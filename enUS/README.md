# Yū Yū Hakusho Tokubetsu-hen - English (enUS) - v0.1 (initial, WIP)
Fan/faithful style: romanized names (Yūsuke, Rei Gan, Jagan...), literal move names. Derived from the PT-BR project.

Status (texts only, draft, NOT compiled/tested):
- [x] battle_text_enUS.txt (281 strings; ruby codes `<$xx><$20>` removed, must be re-inserted/width-checked)
- [x] battle_name_enUS.txt (romaji, same as PT-BR)
- [x] serifu_enUS.txt (intro, 97 lines)
- [x] Narrator/ narrator00-38 + name00-19 (all text done)
- [ ] Opening / Ending / Tournament texts
- [ ] Graphics (title, menus, fonts) - pending decision
- [ ] Build + emulator test

Notes:
- title.asm = ptBR/title.asm without the NAMCO/PRESENTED patch (those two screens stay in original Japanese). Replace ptBR's title.asm with this one in the build folder.
- patch/Yuyu_enUS_v0.1.ips = initial version v0.1 (texts only; Namco/Presented screens original JP; graphics still PT-BR), apply to headerless JP ROM.

Update (graphics, 2026-11-10):
- Opening: voice cast slides 1-10, translator credits (11), "NAMCO presents" (12), controller credits, "In memory of byuu", title screen (Ghost Files / SPECIAL EDITION / PRESS START), and the 20 move-list demo screens (demo00-19) are now English.
- Ending: all staff/cast credit images (gekishu00-42) in English; "STAFF" already was.
- NOT yet: END screen sprites (owari_set.bin, still PT "FIM"), menu plates in Narrator/ (square*, config, preset...), Tournament/ ranking images.
