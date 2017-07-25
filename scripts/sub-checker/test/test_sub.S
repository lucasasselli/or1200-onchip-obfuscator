#include "../../support/spr_defs.h"

  .section .data

  .section .text
  .global _test_sub

_test_sub:
        // Code payload
        l.xor r0, r0, r0
l.addi r0, r0, 8
l.xor r31, r0, r3

        // Report result
        // l.or r3,r0,r31
        // l.nop NOP_REPORT

        // Return
        l.ori r11,r31,0
        l.jr r9 
        l.nop   
