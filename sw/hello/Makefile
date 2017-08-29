CFLAGS=-mboard=or1ksim-uart

all: main.elf main.lst

main.elf: main.c
	or1k-elf-gcc -g -o main.elf $(CFLAGS) main.c

main.lst: main.elf
	or1k-elf-objdump -d main.elf > main.lst

clean:
	rm -rf build/ *.lst *.elf

