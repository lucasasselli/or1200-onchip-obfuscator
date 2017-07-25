#include "../../support/spr_defs.h"

  .section .data

  .section .text
  .global _test_gold

_test_gold:
        // Code payload
        l.xori r31,r3,8

        // Report result
        // l.or r3,r0,r31
        // l.nop NOP_REPORT

        // Return
        l.ori r11,r31,0
        l.jr r9 
        l.nop   
