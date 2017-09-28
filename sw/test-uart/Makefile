CFLAGS=-mboard=or1ksim

all: test-uart.elf test-uart.lst

test-uart.elf: test-uart.c
	or1k-elf-gcc -g -o test-uart.elf $(CFLAGS) test-uart.c

test-uart.lst: test-uart.elf
	or1k-elf-objdump -d test-uart.elf > test-uart.lst

clean:
	rm -rf build/ *.lst *.elf

