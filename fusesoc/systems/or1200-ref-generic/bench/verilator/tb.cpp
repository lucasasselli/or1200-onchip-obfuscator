/*
 * or1200-generic system Verilator testbench
 *
 * Author: Olof Kindgren <olof.kindgren@gmail.com>
 * Author: Franck Jullien <franck.jullien@gmail.com>
 *
 * This program is free software; you can redistribute  it and/or modify it
 * under  the terms of  the GNU General  Public License as published by the
 * Free Software Foundation;  either version 2 of the  License, or (at your
 * option) any later version.
 *
 */

#include <stdint.h>
#include <signal.h>
#include <argp.h>
#include <verilator_tb_utils.h>

#include "Vorpsoc_top__Syms.h"

#include "decoder.h"

static bool done;

#define NOP_NOP			0x0000      /* Normal nop instruction */
#define NOP_EXIT		0x0001      /* End of simulation */
#define NOP_REPORT		0x0002      /* Simple report */
#define NOP_PUTC		0x0004      /* Simputc instruction */
#define NOP_CNT_RESET		0x0005      /* Reset statistics counters */
#define NOP_GET_TICKS		0x0006      /* Get # ticks running */
#define NOP_GET_PS		0x0007      /* Get picosecs/cycle */
#define NOP_TRACE_ON		0x0008      /* Turn on tracing */
#define NOP_TRACE_OFF		0x0009      /* Turn off tracing */
#define NOP_RANDOM		0x000a      /* Return 4 random bytes */
#define NOP_OR1KSIM		0x000b      /* Return non-zero if this is Or1ksim */
#define NOP_EXIT_SILENT		0x000c      /* End of simulation, quiet version */

#define RESET_TIME		2

vluint64_t main_time = 0;       // Current simulation time
// This is a 64-bit integer to reduce wrap over issues and
// allow modulus.  You can also use a double, if you wish.

double sc_time_stamp () {       // Called by $time in Verilog
    return main_time;           // converts to double, to match
    // what SystemC does
}

void INThandler(int signal)
{
    printf("\nCaught ctrl-c\n");
    done = true;
}

static int parse_opt(int key, char *arg, struct argp_state *state)
{
    switch (key) {
        case ARGP_KEY_INIT:
            state->child_inputs[0] = state->input;
            break;
            // Add parsing of custom options here
    }

    return 0;
}

static int parse_args(int argc, char **argv, VerilatorTbUtils* tbUtils)
{
    struct argp_option options[] = {
        // Add custom options here
        { 0 }
    };
    struct argp_child child_parsers[] = {
        { &verilator_tb_utils_argp, 0, "", 0 },
        { 0 }
    };
    struct argp argp = { options, parse_opt, 0, 0, child_parsers };

    return argp_parse(&argp, argc, argv, 0, 0, tbUtils);
}

int main(int argc, char **argv, char **env)
{
    uint32_t insn = 0;
    uint32_t wb_pc = 0;
    uint32_t r3 = 0;
    bool wb_freeze = 0;
    bool except_flushpipe = 0;
    bool ex_dslot = 0;
    long int clk_cnt = 0;

    Verilated::commandArgs(argc, argv);

    Vorpsoc_top* top = new Vorpsoc_top;
    VerilatorTbUtils* tbUtils =
        new VerilatorTbUtils(top->orpsoc_top->mem->ram0->mem);

    parse_args(argc, argv, tbUtils);

    signal(SIGINT, INThandler);

    top->wb_clk_i = 0;
    top->wb_rst_i = 1;

    top->trace(tbUtils->tfp, 99);

    // Logging
    FILE* f_exe = fopen("tb-executed.log", "w");
    FILE* f_out = fopen("tb-output.log", "w");

    char disass_insn[50];

    while (tbUtils->doCycle() && !done) {
        if (tbUtils->getTime() > RESET_TIME)
            top->wb_rst_i = 0;

        top->eval();

        top->wb_clk_i = !top->wb_clk_i;

        tbUtils->doJTAG(&top->tms_pad_i, &top->tdi_pad_i, &top->tck_pad_i, top->tdo_pad_o);

        insn = top->orpsoc_top->or1200_top0->or1200_cpu->or1200_ctrl->wb_insn;
        wb_pc = top->orpsoc_top->or1200_top0->or1200_cpu->or1200_except->wb_pc;
        r3 = top->orpsoc_top->or1200_top0->or1200_cpu->or1200_rf->rf_a->get_gpr(3);

        wb_freeze = top->orpsoc_top->or1200_top0->or1200_cpu->or1200_ctrl->wb_freeze;
        except_flushpipe = top->orpsoc_top->or1200_top0->or1200_cpu->or1200_except->except_flushpipe;
        ex_dslot = top->orpsoc_top->or1200_top0->or1200_cpu->or1200_except->ex_dslot;

        if(top->wb_clk_i){
            // Count clock cycles
            clk_cnt++;
            if(!wb_freeze){
                if (((bit_range(insn,31,26) != OR1200_OR32_NOP) | !(insn & (1 << 16))) && !(except_flushpipe && ex_dslot)){
                    decode(insn, disass_insn); 
                    fprintf(f_exe, "%08x %s\n", wb_pc, disass_insn);
                }
            }
            if(insn == (0x15000000 | NOP_PUTC)){
                /* printf("%c", r3); */
                fprintf(f_out, "%c", r3);
            }
        }

        if (insn == (0x15000000 | NOP_EXIT) || insn == (0x15000000 | NOP_EXIT_SILENT)) {
            printf("Success! Got NOP_EXIT. Exiting (%lu)\n",
                    tbUtils->getTime());
            done = true;
        }
    }

    printf("Simulation ended at PC = %08x (%lu)\n",
            wb_pc, tbUtils->getTime());
    printf("Total clock cycles = %d", clk_cnt);

    fclose(f_exe);
    fclose(f_out);

    delete tbUtils;
    exit(0);
}
