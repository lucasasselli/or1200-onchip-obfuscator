    .section .text
    .align	4
    .global _start
    .org 0x100 
_start: 
    l.movhi r0, 0
    l.movhi r1, 0
    l.movhi r2, 0
    l.xori r1, r1, 15
    l.xori r2, r2, 10
    l.nop
    l.nop
    l.nop
    l.add r3, r2, r1
    l.nop
    l.nop 0xc
