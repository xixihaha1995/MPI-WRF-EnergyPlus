#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <EnergyPlus/api/state.h>
#include <EnergyPlus/api/datatransfer.h>
#include <EnergyPlus/api/runtime.h>

#define MPI_MAX_PROCESSOR_NAME 128

int handlesRetrieved = 0;
int simHVACSensor = 0;
int rank = -1;
Real64 msg = -1;
int endingTimeSeconds = 6 * 24* 3600 - 100;
MPI_Comm parent_comm;
MPI_Status status;

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
//        printf("Not in run period, whichperid = %d\n", whichperid);
        return;
    }
    Real64 simTimeInHours = currentSimTime(state);
    Real64 simTime = simTimeInHours * 3600;
    Real64 simHVAC = getVariableValue(state, simHVACSensor);

    MPI_Recv(&msg, 1, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, parent_comm, &status);
    printf("Child %d received OAT %.2f (C) from %d of comm, and sent heat %.2f (J) to it, at time %.2f\n",
           rank, msg, status.MPI_SOURCE,simHVAC, simTime);
    if (simTime> endingTimeSeconds)
    {
        MPI_Send(&simHVAC, 1, MPI_DOUBLE, status.MPI_SOURCE, 886, parent_comm);
        MPI_Barrier(parent_comm);
        MPI_Finalize();
    } else
    {
        MPI_Send(&simHVAC, 1, MPI_DOUBLE, status.MPI_SOURCE, 0, parent_comm);
    }
}

int main(int argc, char** argv) {

    int size, namelen;
    char processor_name[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Comm_get_parent(&parent_comm);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Get_processor_name(processor_name, &namelen);
    printf("Child/parent %d/%d: rank=%d, size=%d, name=%s\n", rank, parent_comm, rank, size, processor_name);


    char output_path[MPI_MAX_PROCESSOR_NAME];
    char idfFilePath[MPI_MAX_PROCESSOR_NAME];
    EnergyPlusState state = stateNew();
    callbackEndOfSystemTimeStepAfterHVACReporting(state, endSysTimeStepHandler);
    requestVariable(state, "SITE OUTDOOR AIR DRYBULB TEMPERATURE", "ENVIRONMENT");
    requestVariable(state, "SITE OUTDOOR AIR DEWPOINT TEMPERATURE", "ENVIRONMENT");
    requestVariable(state, "HVAC System Total Heat Rejection Energy", "SIMHVAC");

    if (rank ==0)
    {
        strcpy(output_path, "./ep_trivial_1");
        strcpy(idfFilePath, "./resources/in_11.idf");
    } else if (rank == 1)
    {
        strcpy(output_path, "./ep_trivial_2");
        strcpy(idfFilePath, "./resources/in_2.idf");
    } else
    {
        strcpy(output_path, "./ep_trivial_3");
        strcpy(idfFilePath, "./resources/in_13.idf");
    }
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


