#include "../../support/spr_defs.h"

  .section .data

  .section .text
  .global _test

_test:
        // Code payload
        l.xor r0, r0, r0
l.addi r0, r0, 8
l.xor r31, r0, r3

        // Report result
        l.nop NOP_REPORT_SR

        // Return
        l.jr r9 
        l.nop   
