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
#define INNERMOST_POINTS 26
#define NBR_IDF 3
#define NBR_WRF 4
#define LAT_TAG 1
#define LONG_TAG 2

int weatherMPIon = 1, wasteMPIon = 1, toSendMap = NBR_WRF;
int IDF_Coupling = 1; //0, offline; 1, waste; 2, waste + surface;
int handlesRetrieved = 0, weatherHandleRetrieved = 0;
int simHVACSensor = 0, odbActHandle = 0, orhActHandle = 0, odbSenHandle = 0, ohrSenHandle = 0;
int rank = -1, performanc_length = 14; 
float footprintm2[38] = {
    162.15, 2513.40, 37.75, 355.15, 1049.87, 415.98,
    2608.08, 115.65, 1793.84, 2785.14,958.38,2745.55,
    1292.35,347.83,2464.88,9048.44,548.43,185.96,
    828.75,91.38,107.44,90.02,181.64,1698.19,
    4090.41,24400.54,158.22,4229.28,92.32,108.30,
    3781.44,123.20,3298.50,257.05,841.63,80.27,
    1808.91,889.49
};

int midNames[] = {38, 50, 56, 44, 68, 80, 86, 74};
int midLen = sizeof(midNames) / sizeof(midNames[0]);
Real64* tempMidVal;

typedef struct {
    float footPrintM2;
    int bot[4];
    int* mid;
    int top[4];
} GeoUWyo;

GeoUWyo uwyo1 = {
    .footPrintM2 = 162.15,
    .bot = {8, 20, 26, 14},
    .mid = midNames,
    .top = {98, 110, 116, 104}
};


typedef struct {
    int id;
    double lat;
    double lon;
} Building;



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

//performance_length are area, waste, and 12 surface temperatures, which are 14
float msg_arr[3] = {-1, -1, -1};
float longall[NBR_WRF][INNERMOST_POINTS * INNERMOST_POINTS], latall[NBR_WRF][INNERMOST_POINTS * INNERMOST_POINTS];
float tmp_longall[INNERMOST_POINTS * INNERMOST_POINTS], tmp_latall[INNERMOST_POINTS * INNERMOST_POINTS];
int mappings[NBR_WRF][INNERMOST_POINTS * INNERMOST_POINTS * NBR_IDF];

Building buildings[NBR_IDF]; 

MPI_Comm parent_comm;
MPI_Status status;
SurfaceHandles surHandles;
SurfaceValues surValues;


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
    MPI_Recv(&msg_arr, 3, MPI_FLOAT, MPI_ANY_SOURCE, MPI_ANY_TAG, parent_comm, &status);
    if (status.MPI_TAG == 886)
    {
        printf("EnergyPlus(BEMs):%d received 'ending messsage (EP 886, WRF-886)', "
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
        // surHandles = getSurHandle(state, uwyo1);
        
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
    Real64 simHVAC_W = simHVAC_J/ 3600;

    // surValues = getSurVal(state, surHandles);
    // // for surValues.midVal, its length is a multiple of 4. Average it into 4 values
    // Real64 avgMidVal[4];
    // for (int i = 0; i < midLen; i++) {
    //     avgMidVal[i % 4] += surValues.midVal[i];
    // }
    // for (int i = 0; i < 4; i++) {
    //     int num = midLen / 4;
    //     avgMidVal[i] /= num;
    //     // printf("Botom surface %d temperature = %.2f (C)\n", i, surValues.botVal[i]);
    //     // printf("Mid surface %d temperature = %.2f (C)\n", i, avgMidVal[i]);
    //     // printf("Top surface %d temperature = %.2f (C)\n", i, surValues.topVal[i]);
    // }

    // free(tempMidVal);
    if (! wasteMPIon)
    {
        printf("Child rank = %d wasteMPIon=0, No more MPI, simTime = %.2f (s), simHVAC_W = %.2f (W), \n", rank, simTime, simHVAC_W);
        return;
    }

    float data[performanc_length];
    data[0] = footprintm2[rank];
    if (IDF_Coupling == 0)
        data[1] = -66.0;
    else
        data[1] = (float) simHVAC_W;
    // bot 4, mid 4, top 4
    // for (int i = 0; i < 4; i++) {
    //     data[i + 2] = (float) (surValues.botVal[i] + 273.15);
    //     data[i + 6] = (float) (avgMidVal[i] + 273.15);
    //     data[i + 10] = (float) (surValues.topVal[i] + 273.15);
    // }

    MPI_Send(&data, performanc_length, MPI_FLOAT,status.MPI_SOURCE, 0, parent_comm);
    printf("Child %d sent flootaream2 = %.2f (m2), simHVAC_W = %.2f (W),"
        "data[0], data[1] = %.2f, %.2f\n", rank, footprintm2[rank], simHVAC_W, data[0], data[1]);
    
    if (!weatherMPIon) {
        printf("Child %d reached collective barrier, all my siblings here, let's end MPI. \n", rank);
        MPI_Barrier(MPI_COMM_WORLD);
        // MPI_Barrier(parent_comm);
        wasteMPIon = 0;
        int sleeptimeP8S = 1200000;
        usleep(sleeptimeP8S*100);
        MPI_Finalize();
    }
    
}

int closetGridIndex(float bldlat, float bldlong){
    // go through all grids latall, longall, find the closest grid
    double minDist = 1000000000;
    int minIndex = -1, minWRFIdx = -1;
    for (int j = 0; j < NBR_WRF; j++) {
        for (int i = 0; i < INNERMOST_POINTS * INNERMOST_POINTS; i++) {
            double dist = (bldlat - latall[j][i]) * (bldlat - latall[j][i]) + (bldlong - longall[j][i]) * (bldlong - longall[j][i]);
            if (dist < minDist) {
                minDist = dist;
                minIndex = i;
                minWRFIdx = j;
            }
        }

    }

    return minIndex, minWRFIdx;
}

void receiveLongLat(void) {
    // MPI_Recv(&msg_arr, 3, MPI_FLOAT, MPI_ANY_SOURCE, MPI_ANY_TAG, parent_comm, &status);
    // MPI_Send(&data, performanc_length, MPI_FLOAT,status.MPI_SOURCE, 0, parent_comm);

    while (toSendMap > 0) {
        MPI_Recv(&tmp_longall, INNERMOST_POINTS * INNERMOST_POINTS, MPI_FLOAT, 
            MPI_ANY_SOURCE, LAT_TAG, parent_comm, &status);
        MPI_Recv(&tmp_latall, INNERMOST_POINTS * INNERMOST_POINTS, MPI_FLOAT,
            MPI_ANY_SOURCE, LONG_TAG, parent_comm, &status);
        memcpy(latall[status.MPI_SOURCE], tmp_latall, INNERMOST_POINTS * INNERMOST_POINTS * sizeof(float));
        memcpy(longall[status.MPI_SOURCE], tmp_longall, INNERMOST_POINTS * INNERMOST_POINTS * sizeof(float));
        printf("Child %d received singnal from WRF%d\n",rank, status.MPI_SOURCE);
        toSendMap--;
    }


    
    // print the received latlongalls
    // for (int k = 0; k < INNERMOST_POINTS * INNERMOST_POINTS; k++) {
    //     // print the received data with higheset precision
    //     printf("Child %d received longall[%d] = %.10f, latall[%d] = %.10f\n", rank, k, longall[k], k, latall[k]);
    // }

    FILE *file = fopen("./resources-23-1-0/centroid.csv", "r");
    if (file == NULL) {
        printf("Failed to open centroid.csv file.\n");
    }
    // Skip the first line (header) in centroid.csv
    char line[100];
    fgets(line, sizeof(line), file);
    for (int j = 0; j < NBR_WRF; j++) {
        for (int i = 0; i < INNERMOST_POINTS * INNERMOST_POINTS * NBR_IDF; i++) {
            mappings[j][i] = -1;
        }
    }


    int id;
    double lat, lon;
    for (int i = 0; i < NBR_IDF; i++) {
        fscanf(file, "%d, %lf, %lf", &id, &lat, &lon);
        buildings[i].id = id;
        buildings[i].lat = lat;
        buildings[i].lon = lon;
        int gridIndex, wrfIndex;
        gridIndex, wrfIndex = closetGridIndex(lat, lon);
        printf("Building id = %d, lat = %.14lf, lon = %.14lf,"
            "is assigned to WRF#%d, grid %d, lat = %.14lf, lon = %.14lf\n",
            id, lat, lon, wrfIndex, gridIndex, latall[wrfIndex][gridIndex], longall[wrfIndex][gridIndex]);
        mappings[wrfIndex][gridIndex * NBR_IDF + i] = 1;
    }
    fclose(file);

    for (int j = 0; j < NBR_WRF; j++) {
        // MPI_Send(&mappings, INNERMOST_POINTS * INNERMOST_POINTS * NBR_IDF, MPI_INT, status.MPI_SOURCE, 0, parent_comm);
        // MPI_Send(&IDF_Coupling, 1, MPI_INT, status.MPI_SOURCE, 0, parent_comm);
        MPI_Send(&mappings[j], INNERMOST_POINTS * INNERMOST_POINTS * NBR_IDF, MPI_INT, j, 0, parent_comm);
        MPI_Send(&IDF_Coupling, 1, MPI_INT, j, 0, parent_comm);
        printf("Child %d sent mappings to WRF%d\n", rank, j);
    }

    // for (int i = 0; i < INNERMOST_POINTS * INNERMOST_POINTS; i++) {
    //     for (int j = 0; j < NBR_IDF; j++) {
    //         printf("%d ", mappings[i * NBR_IDF + j]);
    //     }
    //     printf("\n");
    // }

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
    if (rank == 0) {
        receiveLongLat();
    }
    printf("Child %d is processing IDF settings\n", rank);
    char output_path[MPI_MAX_PROCESSOR_NAME];
    char idfFilePath[MPI_MAX_PROCESSOR_NAME];
    EnergyPlusState state = stateNew();
    callbackBeginZoneTimestepBeforeSetCurrentWeather(state, overwriteEpWeather);
    callbackEndOfSystemTimeStepAfterHVACReporting(state, endSysTimeStepHandler);
    requestVariable(state, "Site Outdoor Air Drybulb Temperature", "ENVIRONMENT");
    requestVariable(state, "Site Outdoor Air Humidity Ratio", "ENVIRONMENT");
    requestVariable(state, "HVAC System Total Heat Rejection Energy", "SIMHVAC");
    // requestSur(state, uwyo1);
    char curpath[256];
    getcwd(curpath, sizeof(curpath));
    printf("where am I? %s\n", curpath);
    const char* base_path = (strstr(curpath, "glade")) ? "/glade/scratch/lichenwu/ep_temp" : ".";
    // Choose the appropriate folder based on IDF_Coupling value
    printf("base_path = %s\n", base_path);
    sprintf(output_path, "%s/saved_%s_ep_trivial_%d", base_path,
            (IDF_Coupling == 0) ? "offline" : (IDF_Coupling == 1) ? "online1_waste" : "online2_waste_surf",
            rank + 1);
    sprintf(idfFilePath, "./resources-23-1-0/in_uwyo_%d.idf", rank+1);
    printf("output_path = %s\n", output_path);

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