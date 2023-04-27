#include <stdio.h>

// Declare a global variable to keep track of how many times myFunction has been called
int numCalls = 0;

void myFunction() {
    numCalls++;  // Increment the number of calls to myFunction
    printf("myFunction has been called %d times.\n", numCalls);
    // Your function code here
}
