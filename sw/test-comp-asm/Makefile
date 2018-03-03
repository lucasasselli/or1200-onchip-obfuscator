CFLAGS=-mboard=de0_nano -DDE0_NANO

all: test-comp-asm.elf test-comp-asm.lst

test-comp-asm.elf: test-comp-asm.s
	or1k-elf-gcc -c -o test-comp-asm.elf $(CFLAGS) test-comp-asm.s

test-comp-asm.lst: test-comp-asm.elf
	or1k-elf-objdump -d test-comp-asm.elf > test-comp-asm.lst

clean:
	rm -rf build/ *.lst *.elf

