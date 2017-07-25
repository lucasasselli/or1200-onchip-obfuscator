	.file	"hello.c"
	.section	.rodata
.LC0:
	.string	"Hello World!"
	.section .text
	.align	4
.proc	main
	.global main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	l.sw    	-8(r1),r2	 # SI store
	.cfi_offset 2, -8
	l.addi  	r2,r1,0 # addsi3
	.cfi_def_cfa_register 2
	l.sw    	-4(r1),r9	 # SI store
	l.addi	r1,r1,-16	# allocate frame
	.cfi_offset 9, -4
	l.sw    	-12(r2),r3	 # SI store
	l.sw    	-16(r2),r4	 # SI store
	l.movhi  	r3,hi(.LC0) # movsi_high
	l.ori   	r3,r3,lo(.LC0) # movsi_lo_sum
	l.jal   	puts # call_value_internal
	l.nop			# nop delay slot
	l.addi  	r3,r0,0	 # move immediate I
	l.ori   	r11,r3,0	 # move reg to reg
	l.ori	r1,r2,0	# deallocate frame
	l.lwz   	r2,-8(r1)	 # SI load
	l.lwz   	r9,-4(r1)	 # SI load
	l.jr    	r9	# return_internal
	l.nop			# nop delay slot
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.ident	"GCC: (GNU) 6.0.0 20160228 (experimental)"
