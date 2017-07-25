#define DEBUG 0
#define DBGFINE 0
#define N 10

#include "../../support/support.h"

void buserr_except(){}
void dpf_except(){}
void ipf_except(){}
void lpint_except(){}
void align_except(){}
void illegal_except(){}
void hpint_except(){}
void dtlbmiss_except(){}
void itlbmiss_except(){}
void range_except(){}
void syscall_except(){}
void res1_except(){}
void trap_except(){}
void res2_except(){}

extern void test(long a, long b);

// Xorshift
static unsigned long x=123456789, y=362436069, z=521288629;
unsigned long xorshf96(void) {
    unsigned long t;
    x ^= x << 16;
    x ^= x >> 5;
    x ^= x << 1;

    t = x;
    x = y;
    y = z;
    z = t ^ x ^ y;

    return z;
}

int main()
{	
    int i=0;
    long res;
    long in1, in2;

#if DEBUG
    report(0xcafecafe);	
#endif

    // Execute test
    for(i=0; i<N; i++){
        in1 = xorshf96();
        in2 = xorshf96();
        test(in1, in2);
    }

    return 0;
}
