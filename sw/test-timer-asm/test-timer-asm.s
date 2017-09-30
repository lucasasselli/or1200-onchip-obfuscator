# vim:ft=or1kasm

/*
    NOTE:
    This test is designed to test the obfuscator behavior in the event of an exception, in this case a timer interrupt.
*/

    .section .text
    .align	4
    .global _start
    .org 0x100 

# Constants
    .set ADDR_T, 0b0101000000000000
    .set ADDR_SR, 0b0000000000010001

_start:
    l.movhi r0,0

# Set SR
    l.xori r1,r0,ADDR_SR
    l.mfspr r2,r1,0
    l.ori r2,r2,6
    l.mtspr r1,r2,0

# Clear TTCR
    l.xori r1,r0,ADDR_T # TTMR address
    l.mtspr r1,r0,1

# Start timer
    l.movhi r2,0b1010000000000000 # TTMR content (high)
    l.ori r2,r2, 255              # TTMR content (low)
    l.mtspr r1,r2,0

# Set seed
    l.movhi r3,0xcafe
    l.ori r3,r3,0xabba

    l.movhi r4,0

xor_shifth:
    l.srli r1,r3,3  # XS 1
    l.xor r3,r3,r1
    l.slli r1,r3,15 # XS 2
    l.xor r3,r3,r1
    l.srli r1,r3,12 # XS 3
    l.xor r3,r3,r1

# Report r3
    l.nop 2

# Iterate
    l.sfeqi r4,15
    l.bnf xor_shifth
    l.addi r4,r4,1

    l.nop 0xc # Exit

    .org 0x500
timer_int:
    # Clear interrupt flag
    l.xori r1,r0,ADDR_T
    l.mtspr r1,r0,0
    l.rfe
    l.nop

