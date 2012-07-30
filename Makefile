all:
	gcc -Wall -O2 -funswitch-loops -ffast-math -fwhole-program -o md5game -lpthread md5game.c
