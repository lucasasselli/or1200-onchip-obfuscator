#ifndef SUPPORT_H                                                                                                                                             
#define SUPPORT_H

#include <stdarg.h>
#include <stddef.h>
#include <limits.h>

#define NOP_EXIT         0x0001
#define NOP_REPORT       0x0002
#define NOP_REPORT_SR    0x000d

void exit(int i);

void report(unsigned long value);

void report_sr();

#endif
