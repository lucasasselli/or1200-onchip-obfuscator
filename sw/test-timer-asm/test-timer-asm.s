# vim:ft=or1kasm
    .section .text
    .align	4
    .global _start
    .org 0x100 

_start:
    l.movhi r0,0
    l.xori r1,r0,0b0101000000000000 # TTMR address
    l.xori r3,r0,0b0101000000000001 # TTCR address
    l.xori r4,r0,0b0000000000010001 # SR address

    l.movhi r2,0b1010000000000000 # TTMR content (high)
    l.ori r2,r2, 255              # TTMR content (low)
    
    # Set SR
    l.mfspr r5,r4,0
    l.ori r5,r5,6
    l.mtspr r4,r5,0

    # Clear TTCR
    l.mtspr r3,r0,0
    # Start timer
    l.mtspr r1,r2,0

    # Count...
    l.movhi r5,0
stuck:
    l.j stuck
    l.addi r5,r5,1

    .org 0x500
timer_int:
    l.nop 0xc
    l.nop

