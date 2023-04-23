#include <EnergyPlus/api/state.h>
#include <stdio.h>
int main(int argc, const char * argv[]) {
        EnergyPlusState state = stateNew();
        stateReset(state);
        stateDelete(state);
        printf("simple ep test with c.\n");
}
