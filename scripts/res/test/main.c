#include "support/support.h"

#define N 10

extern void test(long a, long b);

// Xorshift
static unsigned long x=123456790, y=362436069, z=521288629;
unsigned long xorshift(void) {
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
    long in1, in2;

    // Execute test
    for(i=0; i<N; i++){
        in1 = xorshift();
        in2 = xorshift();
        test(in1, in2);
    }

    return 0;
}
