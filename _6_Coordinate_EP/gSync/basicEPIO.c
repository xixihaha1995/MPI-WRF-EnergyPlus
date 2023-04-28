#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <EnergyPlus/api/state.h>
#include <EnergyPlus/api/datatransfer.h>
#include <EnergyPlus/api/runtime.h>

#define MPI_MAX_PROCESSOR_NAME 128

int handlesRetrieved = 0;
int simHVACSensor = 0;

void endSysTimeStepHandler(EnergyPlusState state) {
    if (handlesRetrieved == 0) {
        if (!apiDataFullyReady(state)) {
            printf("Data not fully ready\n");
            return;
        }
        handlesRetrieved = 1;
        simHVACSensor = getVariableHandle(state, "HVAC System Total Heat Rejection Energy", "SIMHVAC");
        if (simHVACSensor < 0)
        {
            printf("Error: simHVACSensor = %d\n", simHVACSensor);
            exit(1);
        }
    }

    int warmUp = warmupFlag(state);
    if (warmUp) {
        return;
    }
    int whichperid = kindOfSim(state);
    if (whichperid != 3) {
        return;
    }
    Real64 simTimeInHours = currentSimTime(state);
    Real64 simTime = simTimeInHours * 3600;
    Real64 simHVAC = getVariableValue(state, simHVACSensor);
    printf("Current Sim Time: %.2f (s), HVAC Waste: %.2f (J)\n", simTime, simHVAC);
}

int main(int argc, char** argv) {
    EnergyPlusState state = stateNew();
    callbackEndOfSystemTimeStepAfterHVACReporting(state, endSysTimeStepHandler);
    requestVariable(state, "SITE OUTDOOR AIR DRYBULB TEMPERATURE", "ENVIRONMENT");
    requestVariable(state, "SITE OUTDOOR AIR DEWPOINT TEMPERATURE", "ENVIRONMENT");
    requestVariable(state, "HVAC System Total Heat Rejection Energy", "SIMHVAC");

    char* output_path = "./ep_trivial";
    char* idfFilePath = "./resources/in_11.idf";
    char* weather_file_path = "./resources/USA_NY_Buffalo-Greater.Buffalo.Intl.AP.725280_TMY3.epw";
    const char* sys_args[] = {"-d", output_path, "-w", weather_file_path, idfFilePath, NULL};
    int argc_ = sizeof(sys_args) / sizeof(char*) - 1;
    printf("argc_ = %d\n", argc_);
    for (int i = 0; i < argc_; i++) {
        printf("sys_args[%d] = %s\n", i, sys_args[i]);
    }
    energyplus(state,argc_, sys_args);
    return 0;
}
