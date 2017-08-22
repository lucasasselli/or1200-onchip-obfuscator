    .section .text
    .align	4
    .global _start
    .org 0x100 
_start: 
    l.movhi r0, 0
    l.movhi r1, 0
    l.movhi r2, 0
    l.movhi r3, 0
    l.movhi r4, 0
    l.movhi r5, 0
loop_0:
    l.sfnei r1, 6
    l.bf loop_0
    l.addi r1,r1,1
    l.nop 0xfffffff0
    l.nop 0xfffffff1
    l.nop 0xfffffff2
    l.j target_0
    l.nop 0xfffffff0
    l.nop 0xfffffff1
    l.nop 0xfffffff2
target_0:
    l.nop 0xc
