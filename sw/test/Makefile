CFLAGS=-mboard=de0_nano -DDE0_NANO

all: main.elf main.lst

all: main.elf main.lst

main.elf: main.s
	or1k-elf-gcc -c -o main.elf $(CFLAGS) main.s

main.lst: main.elf
	or1k-elf-objdump -d main.elf > main.lst

clean:
	rm -rf build/ *.lst *.elf

