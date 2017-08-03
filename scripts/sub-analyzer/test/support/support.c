#include "support.h" 

void exit(int i)                                
{
    asm("l.add r3,r0,%0": : "r" (i));
    asm("l.nop %0": :"K" (NOP_EXIT));
    while (1);
}
void report(unsigned long value)
{
    asm("l.addi\tr3,%0,0": :"r" (value));
    asm("l.nop %0": :"K" (NOP_REPORT));
}

void report_sr()
{
    asm("l.nop %0": :"K" (NOP_REPORT_SR));
}
