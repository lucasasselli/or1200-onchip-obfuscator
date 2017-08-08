  #define NOP_REPORT_SR 0xf

  .section .data

  .section .text
  .global test

test:
    // Generate carry flag
    l.andi r25,r3,1
    l.addi r25,r25,-1

    // Code payload
    l.xori r31,r3,8

    // Report result
    l.nop NOP_REPORT_SR

    // Return
    l.jr r9 
    l.nop   
