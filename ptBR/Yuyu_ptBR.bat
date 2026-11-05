@echo off
rem Monta a traducao PT-BR de Yuu Yuu Hakusho Tokubetsu-hen.
rem Use a ROM japonesa SEM header (2 MB), renomeada para YuJ.smc.

copy /Y YuJ.smc Yuyu_ptBR.smc


atlas -d log_ptBR.txt Yuyu_ptBR.smc battle_text_PTBR.txt
atlas -d log_ptBR.txt Yuyu_ptBR.smc battle_name_PTBR.txt
atlas -d log_ptBR.txt Yuyu_ptBR.smc serifu_PTBR.txt
xkas.exe -o Yuyu_ptBR.smc main.asm

pause
