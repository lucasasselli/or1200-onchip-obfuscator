CFLAGS=-mboard=or1ksim

all: hello.elf hello.lst

hello.elf: hello.c
	or1k-elf-gcc -g -o hello.elf $(CFLAGS) hello.c

hello.lst: hello.elf
	or1k-elf-objdump -d hello.elf > hello.lst

clean:
	rm -rf build/ *.lst *.elf

