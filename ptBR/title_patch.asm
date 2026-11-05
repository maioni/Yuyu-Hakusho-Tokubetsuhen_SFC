// title.asm: manter os blocos org $80D550 e org $80D561 EXATAMENTE como estao.
// ESTRELAS: ficam no lugar onde estava o efeito de fogo (inferior-esquerda de cada "YU").
org $80D550
	LDA #$002C
	STA $40
	LDA #$005F
	STA $42		//star1 pos
org $80D561
	LDA #$007C
	STA $40
	LDA #$005F
	STA $42		//star2 pos
// FOGO (efeito amarelo animado): vai para os espacos entre os YU (no lugar da chama azul).
org $80D579
	dw $0054	//fogo 1: X (era $002C)
org $80D585
	dw $00A4	//fogo 2: X (era $0040)
