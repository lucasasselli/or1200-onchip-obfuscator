TARGET=or1k-elf

CC=$(TARGET)-gcc
OBJDUMP=$(TARGET)-objdump

SUPPORT_DIR=support

ASM_FILES = $(shell find $(SOURCEDIR) -name '*.S')
C_FILES = main.c
OBJ_FILES = $(ASM_FILES:.S=.o) $(C_FILES:.c=.o)

all: test

.S.o:
	$(CC) -O0 $? -c -o $@
	
.c.o:
	$(CC) -O2 $? -c -o $@

test: support.o $(OBJ_FILES) 
	$(CC) $? -o $@.elf
	$(OBJDUMP) -d $@.elf > $@.lst

support.o:
	$(CC) $(SUPPORT_DIR)/support.c -c -o support.o

clean:
	rm -f *.c *.o *.elf *.log *.bin *.lst *.S
