all:
	gcc -Wall -O2 -ffast-math -fwhole-program -o md5game -lpthread md5game.c
