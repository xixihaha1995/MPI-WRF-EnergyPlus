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

typedef struct {
    float footPrintM2;
    int bot[4];
    int* mid;
    int top[4];
} GeoUWyo;

typedef struct {
    int botHandle[4];
    int* midHandle;
    int topHandle[4];
} SurfaceHandles;

typedef struct {
    Real64 botVal[4];
    Real64* midVal;
    Real64 topVal[4];
} SurfaceValues;

int handlesRetrieved = 0, weatherHandleRetrieved = 0;
int simHVACSensor = 0, odbActHandle = 0, orhActHandle = 0, odbSenHandle = 0, ohrSenHandle = 0;
int rank = -1;
Real64 uwyoBld1AreaM2 = 162.15;
Real64 msg_arr[3] = {-1, -1, -1};
int weatherMPIon = 1, wasteMPIon = 1;
MPI_Comm parent_comm;
MPI_Status status;
SurfaceHandles surHandles;
SurfaceValues surValues;



int midNames[] = {38, 50, 56, 44, 68, 80, 86, 74};
int midLen = sizeof(midNames) / sizeof(midNames[0]);
Real64* tempMidVal;

GeoUWyo uwyo1 = {
    .footPrintM2 = 162.15,
    .bot = {8, 20, 26, 14},
    .mid = midNames,
    .top = {98, 110, 116, 104}
};



// I'd like add three more functions related with GeoUWyo1 surfaces,
// one is used to request the surface variables
// one is used to get surface handle, and check if it is valid
// one is used to get surface variable value.

void requestSur(EnergyPlusState state, GeoUWyo geoUWyo) {
    // char surfaceName[100];
    // sprintf(surfaceName, "Surface %d", geoUWyo.bot[0]);
    // requestVariable(state, "Surface Outside Face Temperature", surfaceName);
    // This function is used to iterate bot, mid, top surfaces. request them

    char surfaceName[100];
    for (int i = 0; i < 4; i++) {
        sprintf(surfaceName, "Surface %d", geoUWyo.bot[i]);
        requestVariable(state, "Surface Outside Face Temperature", surfaceName);
        sprintf(surfaceName, "Surface %d", geoUWyo.top[i]);
        requestVariable(state, "Surface Outside Face Temperature", surfaceName);
    }
    for (int i = 0; i < midLen; i++) {
        sprintf(surfaceName, "Surface %d", geoUWyo.mid[i]);
        requestVariable(state, "Surface Outside Face Temperature", surfaceName);
    }
}

SurfaceHandles getSurHandle(EnergyPlusState state, GeoUWyo geoUWyo) {
    // This function is used to iterate bot, mid, top surfaces. get their handles
    SurfaceHandles surHandles;
    char surfaceName[100];
    for (int i = 0; i < 4; i++) {
        sprintf(surfaceName, "Surface %d", geoUWyo.bot[i]);
        surHandles.botHandle[i] = getVariableHandle(state, "Surface Outside Face Temperature", surfaceName);
        sprintf(surfaceName, "Surface %d", geoUWyo.top[i]);
        surHandles.topHandle[i] = getVariableHandle(state, "Surface Outside Face Temperature", surfaceName);
        if (surHandles.botHandle[i] < 0 || surHandles.topHandle[i] < 0) {
            printf("Error: surHandles.botHandle[%d] = %d, surHandles.topHandle[%d] = %d\n",
                   i, surHandles.botHandle[i], i, surHandles.topHandle[i]);
            exit(1);
        }
    }
    for (int i = 0; i < midLen; i++) {
        sprintf(surfaceName, "Surface %d", geoUWyo.mid[i]);
        surHandles.midHandle[i] = getVariableHandle(state, "Surface Outside Face Temperature", surfaceName);
        if (surHandles.midHandle[i] < 0) {
            printf("Error: surHandles.midHandle[%d] = %d\n", i, surHandles.midHandle[i]);
            exit(1);
        }
    }
    return surHandles;
}

SurfaceValues getSurVal(EnergyPlusState state, SurfaceHandles surHandles) {
    // This function is used to iterate bot, mid, top surfaces. get their values
    SurfaceValues surValues;
    for (int i = 0; i < 4; i++) {
        surValues.botVal[i] = getVariableValue(state, surHandles.botHandle[i]);
        surValues.topVal[i] = getVariableValue(state, surHandles.topHandle[i]);
    }
    tempMidVal = malloc(midLen * sizeof(Real64));
    for (int i = 0; i < midLen; i++) {
        Real64 midVal = getVariableValue(state, surHandles.midHandle[i]);
        tempMidVal[i] = midVal;
    }
    surValues.midVal = tempMidVal;
    return surValues;
}

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
               "to reach collective barrier, EP wait WRF to finalize, then EP free MPI_Finalize().\n"
               "Then no more MPI at all on both sides.", rank);
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
        surHandles = getSurHandle(state, uwyo1);
        
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
    Real64 simHVAC_J = getVariableValue(state, simHVACSensor);
    Real64 simHVAC_Wm2 = simHVAC_J / uwyoBld1AreaM2 / 3600;

    surValues = getSurVal(state, surHandles);
    // for surValues.midVal, its length is a multiple of 4. Average it into 4 values
    Real64 avgMidVal[4];
    for (int i = 0; i < midLen; i++) {
        avgMidVal[i % 4] += surValues.midVal[i];
    }
    for (int i = 0; i < 4; i++) {
        avgMidVal[i] /= 4;
        printf("Botom surface %d temperature = %.2f (C)\n", i, surValues.botVal[i]);
        printf("Top surface %d temperature = %.2f (C)\n", i, surValues.topVal[i]);
        printf("Mid surface %d temperature = %.2f (C)\n", i, avgMidVal[i]);
    }

    free(tempMidVal);
    if (! wasteMPIon)
    {
        printf("Child rank = %d wasteMPIon=0, No more MPI, simTime = %.2f (s), simHVAC_Wm2 = %.2f (W_m2), \n", rank, simTime, simHVAC_Wm2);
        return;
    }

    MPI_Send(&simHVAC_Wm2, 1, MPI_DOUBLE, status.MPI_SOURCE, 0, parent_comm);
    printf("Child %d sent heat %.2f (W_m2) to it, at time %.2f(s)\n",
           rank,simHVAC_Wm2, simTime);
    
    if (!weatherMPIon) {
        printf("Child %d reached collective barrier, all my siblings here, let's end MPI. \n", rank);
        MPI_Barrier(parent_comm);
        wasteMPIon = 0;
        // sleep 5 seconds
        usleep(8000000);
        MPI_Finalize();
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
    requestSur(state, uwyo1);

    sprintf(output_path, "./ep_trivial_%d", rank);
    sprintf(idfFilePath, "./resources-23-1-0/in_uwyo_1.idf");

    char* weather_file_path = "./resources-23-1-0/USA_WY_Laramie-General.Brees.Field.725645_TMY3.epw";
    const char* sys_args[] = {"-d", output_path, "-w", weather_file_path, idfFilePath, NULL};
    int argc_ = sizeof(sys_args) / sizeof(char*) - 1;
    printf("argc_ = %d\n", argc_);
    for (int i = 0; i < argc_; i++) {
        printf("sys_args[%d] = %s\n", i, sys_args[i]);
    }
    energyplus(state,argc_, sys_args);
 

    return 0;
}