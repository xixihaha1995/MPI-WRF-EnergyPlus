
#include <stdio.h>

extern void hello_world(void);

int numCalls = 0;

void hello_world(void)
{
    numCalls++;
    printf("Hello WRF, this is real c world! %d\n", numCalls);
}
