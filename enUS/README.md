# Yū Yū Hakusho Tokubetsu-hen - English (enUS) - WORK IN PROGRESS
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
- patch/Yuyu_enUS_draft.ips = draft patch (build of 2026-11-10, first test), apply to headerless JP ROM.
