#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <EnergyPlus/api/state.h>
#include <EnergyPlus/api/datatransfer.h>
#include <EnergyPlus/api/runtime.h>
#include <EnergyPlus/api/func.h>

#define MPI_MAX_PROCESSOR_NAME 128

int handlesRetrieved = 0, weatherHandleRetrieved = 0;
int simHVACSensor = 0, odbActHandle = 0, orhActHandle = 0, odbSenHandle = 0, ohrSenHandle = 0;
int rank = -1;
Real64 msg_arr[3] = {-1, -1, -1};
int weatherMPIon = 1, wasteMPIon = 1;
MPI_Comm parent_comm;
MPI_Status status;

void overwriteEpWeather(EnergyPlusState state) {
    if (weatherHandleRetrieved == 0) {
        // if (!apiDataFullyReady(state)) {
        //     printf("set weather API not fully ready\n");
        //     return;
        // }
        weatherHandleRetrieved = 1;
        odbActHandle = getActuatorHandle(state, "Weather Data", "Outdoor Dry Bulb", "ENVIRONMENT");
        orhActHandle = getActuatorHandle(state, "Weather Data", "Outdoor Relative Humidity", "ENVIRONMENT");
        odbSenHandle = getVariableHandle(state, "SITE OUTDOOR AIR DRYBULB TEMPERATURE", "ENVIRONMENT");
        ohrSenHandle = getVariableHandle(state, "Site Outdoor Air Humidity Ratio", "ENVIRONMENT");

        if (odbActHandle < 0 || orhActHandle < 0 || odbSenHandle < 0 || ohrSenHandle < 0)
        {
            printf("Error: odbActHandle = %d, orhActHandle = %d, odbSenHandle = %d, ohrSenHandle = %d\n",
                   odbActHandle, orhActHandle, odbSenHandle, ohrSenHandle);
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

    if (! weatherMPIon)
    {
        printf("Child rank = %d weatherMPIon=0, No more MPI\n", rank);
        return;
    }
    // MPI_Barrier(MPI_COMM_WORLD);
    MPI_Recv(&msg_arr, 3, MPI_DOUBLE, MPI_ANY_SOURCE, MPI_ANY_TAG, parent_comm, &status);
    if (status.MPI_TAG == 886)
    {
        printf("EnergyPlus(BEMs):%d received 'ending messsage 886', "
               "to reach collective barrier, only WRF call free MPI_Finalize().\n", rank);
        weatherMPIon = 0;
    }
    Real64 rh = 100 * psyRhFnTdbWPb(state, msg_arr[0], msg_arr[1], msg_arr[2]);
        printf("Child %d received weather %.2f (OAT_C), %.5f (Abs_Hum kgw/kga), %.2f (Pa)"
            " and calculated RH = %.2f (%%) from parent %d, at time %.2f(s)\n",
            rank, msg_arr[0], msg_arr[1], msg_arr[2], rh, status.MPI_SOURCE, 3600*currentSimTime(state));

    setActuatorValue(state, odbActHandle, msg_arr[0]);
    setActuatorValue(state, orhActHandle, rh);

    Real64 odbSen = getVariableValue(state, odbSenHandle);
    Real64 ohrSen = getVariableValue(state, ohrSenHandle);

}

void endSysTimeStepHandler(EnergyPlusState state) {
    if (handlesRetrieved == 0) {
        if (!apiDataFullyReady(state)) {
            printf("ep results API not fully ready\n");
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

    if (! wasteMPIon)
    {
        printf("Child rank = %d wasteMPIon=0, No more MPI, simTime = %.2f (s), simHVAC = %.2f (J), \n", rank, simTime, simHVAC);
        return;
    }

    MPI_Send(&simHVAC, 1, MPI_DOUBLE, status.MPI_SOURCE, 0, parent_comm);
    printf("Child %d sent heat %.2f (J) to it, at time %.2f(s)\n",
           rank,simHVAC, simTime);
    
    if (!weatherMPIon) {
        MPI_Barrier(parent_comm);
        printf("Child %d reached collective barrier, all my siblings here, let's end MPI. \n", rank);
        wasteMPIon = 0;
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
    callbackBeginZoneTimestepBeforeSetCurrentWeather(state, overwriteEpWeather);
    callbackEndOfSystemTimeStepAfterHVACReporting(state, endSysTimeStepHandler);
    requestVariable(state, "Site Outdoor Air Drybulb Temperature", "ENVIRONMENT");
    requestVariable(state, "Site Outdoor Air Humidity Ratio", "ENVIRONMENT");
    requestVariable(state, "HVAC System Total Heat Rejection Energy", "SIMHVAC");

    sprintf(output_path, "./ep_trivial_%d", rank);
    sprintf(idfFilePath, "./resources/in_uwyo_1.idf");

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