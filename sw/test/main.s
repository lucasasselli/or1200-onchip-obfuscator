    .section .text
    .align	4
    .global _start
    .org 0x100 
_start: 
    l.movhi r0, 0
    l.movhi r2, 0
    l.addi  r1,r0,1
loop:
    l.sfnei r2, 6
    l.bf loop
    l.add r2,r2,r1
    l.nop 0xc
