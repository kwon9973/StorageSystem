CC = gcc

all: main.o
	${CC} main.o -o hello

main.i: main.c
	${CC} -E main.c > main.i

main.s: main.i
	${CC} -S main.i

main.o: main.s
	${CC} -c main.s

clean:
	rm -rf main.o main.i main.s hello

execute:
	./hello
