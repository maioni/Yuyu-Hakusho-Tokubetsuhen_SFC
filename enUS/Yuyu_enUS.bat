@echo off
rem Builds the ENGLISH (draft) translation of Yuu Yuu Hakusho Tokubetsu-hen.
rem Put the headerless 2 MB Japanese ROM here as YuJ.smc. Needs atlas.exe and xkas.exe in this folder (or in PATH).

rem 1) Narrator texts (uses Narrator\Insert.exe)
cd Narrator
call Narrator.bat
cd ..

rem 2) ROM
copy /Y YuJ.smc Yuyu_enUS.smc
atlas -d log_enUS.txt Yuyu_enUS.smc battle_text_enUS.txt
atlas -d log_enUS.txt Yuyu_enUS.smc battle_name_enUS.txt
atlas -d log_enUS.txt Yuyu_enUS.smc serifu_enUS.txt
xkas.exe -o Yuyu_enUS.smc main.asm

echo.
echo Done: Yuyu_enUS.smc  (check log_enUS.txt for errors)
pause
