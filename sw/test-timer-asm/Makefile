CFLAGS=-mboard=de0_nano -DDE0_NANO

all: test-timer-asm.elf test-timer-asm.lst

test-timer-asm.elf: test-timer-asm.s
	or1k-elf-gcc -c -o test-timer-asm.elf $(CFLAGS) test-timer-asm.s

test-timer-asm.lst: test-timer-asm.elf
	or1k-elf-objdump -d test-timer-asm.elf > test-timer-asm.lst

clean:
	rm -rf build/ *.lst *.elf

