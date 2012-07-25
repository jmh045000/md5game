all:
	gcc -Wall -O3 -fno-tree-dce -o md5game -lpthread md5game.c
