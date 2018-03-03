# vim:ft=or1kasm

    .section .text
    .align	4
    .global _start
    .org 0x100 

_start:
    l.movhi r0,0
    l.movhi r1,0
    l.movhi r2,0

    l.sfeq r1,r2
    l.sfeqi r1,8
    l.sfges r1,r2
    l.sfgesi r1,8
    l.sfgeu r1,r2
    l.sfgeui r1,8
    l.sfgts r1,r2
    l.sfgtsi r1,8
    l.sfgtu r1,r2
    l.sfgtui r1,8
    l.sfles r1,r2
    l.sflesi r1,8
    l.sfleu r1,r2
    l.sfleui r1,8
    l.sflts r1,r2
    l.sfltsi r1,8
    l.sfltu r1,r2
    l.sfltui r1,8
    l.sfne r1,r2

    l.nop 0xc # Exit
