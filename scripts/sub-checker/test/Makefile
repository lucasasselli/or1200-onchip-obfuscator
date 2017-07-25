
ASM_FILES = $(shell find $(SOURCEDIR) -name '*.S')
C_FILES = main.c
OBJ_FILES = $(ASM_FILES:.S=.o) $(C_FILES:.c=.o)
SUPPORT_DIR = ../../support/

common = $(SUPPORT_DIR)libsupport.a

all: test-nocache test-icdc test-ic test-dc

.S.o:
	or32-uclinux-gcc -O0 $? -c -o $@
	
.c.o:
	or32-uclinux-gcc -O2 $? -c -o $@

test-nocache: $(OBJ_FILES) $(SUPPORT_DIR)reset-nocache.o $(common)
	or32-uclinux-ld -T $(SUPPORT_DIR)orp.ld $? -o $@.or32
	or32-uclinux-objcopy -O binary $@.or32 $@.bin
	or32-uclinux-objdump -d $@.or32 > $@.lst

test-icdc: $(OBJ_FILES) $(SUPPORT_DIR)reset-icdc.o $(common)
	or32-uclinux-ld -T $(SUPPORT_DIR)orp.ld $? -o $@.or32
	or32-uclinux-objcopy -O binary $@.or32 $@.bin
	or32-uclinux-objdump -d $@.or32 > $@.lst

test-ic: $(OBJ_FILES) $(SUPPORT_DIR)reset-ic.o $(common)
	or32-uclinux-ld -T $(SUPPORT_DIR)orp.ld $? -o $@.or32
	or32-uclinux-objcopy -O binary $@.or32 $@.bin
	or32-uclinux-objdump -d $@.or32 > $@.lst

test-dc: $(OBJ_FILES) $(SUPPORT_DIR)reset-dc.o $(common)
	or32-uclinux-ld -T $(SUPPORT_DIR)orp.ld $? -o $@.or32
	or32-uclinux-objcopy -O binary $@.or32 $@.bin
	or32-uclinux-objdump -d $@.or32 > $@.lst

clean:
	rm -f *.o *.or32 *.log *.bin *.lst *.S
