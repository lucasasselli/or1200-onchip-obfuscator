    .section .text
    .align	4
    .global _start
    .org 0x100 
_start: 
    l.movhi r0, 0
    l.addi r1, r0, 1
    l.movhi r2, 0
    l.movhi r3, 0
loop1:
    l.add r2, r2, r1
    l.add r3, r3, r1
    l.sfnei r2, 6
    l.bf loop1
    l.nop
loop2:
    l.add r3, r3, r1
    l.sfnei r3, 12
    l.bf loop2
    l.nop
    l.nop 0xc
