org $80D0A3
	JML redraw_title
org $80D125
	JML rewrite_title_col
	
org $80D5CE
	incbin "Opening/star.bin"

	
//####PRESS START###########
org $80D3B4
	LDX #$0100		//opening title press start size
	STX $4305
org $80D3D3
	LDX #$6220	//vram
org $80D3C2
	LDX #(blank)
	STX $4302
	LDA.b #(blank)>>16
	STA $4304
	LDX #$0100
	STX $4305
org $80D403
	LDX #(blank)
	STX $4302
	LDA.b #(blank)>>16
	STA $4304
	LDX #$0100
	STX $4305
	LDX #$6220	//vram
	STX $D0

org $80D550
	LDA #$0056
	STA $40
	LDA #$0050
	STA $42		//star1: entre o 1o e o 2o YU

org $80D561
	LDA #$00A2
	STA $40
	LDA #$0059
	STA $42  //star2: entre o 2o YU e HAKU/SHO

//FOGO (sprite animado, aparece junto com as estrelas) dentro dos dois U
org $80D579
	dw $0036	//fogo 1: X (original $002C)
org $80D57C
	dw $004D	//fogo 1: Y (original $005F)
org $80D585
	dw $0088	//fogo 2: X (original $0040)
org $80D588
	dw $004D	//fogo 2: Y (original $005A)

//SEQUENCIA: 1) so o fogo animado; 2) depois as estrelas + fogo FIXO.
//Fase do fogo+estrelas ($D383): remove a chamada das estrelas (fica so o fogo animado).
org $80D383
	db $EA,$EA,$EA
//A rotina $D5B7 (chamada junto com as estrelas) desenhava o "glint" (14 sprites tile $FE,
//que no set novo viram listras). Agora desenha o fogo fixo (um quadro parado) dentro dos U.
org $80D5B7
	JSL static_fire
	RTS
org $80D626
	db $F0,$D0,$4C,$00

//BLANK: garante bytes zero reais em $E58000 (antes so existia o label, sem dados).
//Sem isso a ROM termina antes e o emulador le lixo. $1000 zeros: a limpeza do texto (narrator) copia $C00 bytes de "blank" para a VRAM.
org $E58000
fillbyte $00
fill $1000

org $E59000
static_fire:
	LDA #$3A00
	STA $44
	LDA #$0036
	STA $40
	LDA #$004D
	STA $42
	LDX #$D63E
	JSL $809789
	LDA #$0088
	STA $40
	LDA #$004D
	STA $42
	LDX #$D63E
	JSL $809789
	RTL

//NAMCO / PRESENTED screens: original Japanese streams kept (no patch here).
