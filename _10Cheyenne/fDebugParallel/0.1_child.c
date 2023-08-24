#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <EnergyPlus/api/state.h>
#include <EnergyPlus/api/datatransfer.h>
#include <EnergyPlus/api/runtime.h>
#include <EnergyPlus/api/func.h>
#include <math.h>

#define MPI_MAX_PROCESSOR_NAME 128
#define NBR_IDF 3
#define NBR_WRF 1
#define HOR_LEN_TAG 3
#define VER_LEN_TAG 4
#define LAT_TAG 1
#define LONG_TAG 2
#define COUPLING_TAG 5
#define MAPPING_TAG 6
#define EARTH_RADIUS_KM 6371.0

int IDF_Coupling = 2; //0, offline; 1, waste; 2, waste + surface;

typedef struct {
    int gridIdx;
    int wrfIdx;
} Mapping_Index;

double degreesToRadians(double degrees) {
    return degrees * M_PI / 180.0;
}

double distanceBetweenPoints(double lat1, double long1, double lat2, double long2) {
    // Convert latitude and longitude from degrees to radians
    lat1 = degreesToRadians(lat1);
    long1 = degreesToRadians(long1);
    lat2 = degreesToRadians(lat2);
    long2 = degreesToRadians(long2);

    // Haversine formula
    double dlat = lat2 - lat1;
    double dlong = long2 - long1;
    double a = pow(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * pow(sin(dlong / 2), 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    
    // Calculate the distance in kilometers
    double distance = EARTH_RADIUS_KM * c;
    return distance;
}

typedef struct {
    int id;
    double lat;
    double lon;
} Building;

typedef struct {
    int id;
    int bot[4];
    int *mid;
    int midcount;
    int top[4];
    int roof;
} GeoUWyo;

GeoUWyo geoUWyoMyRank; // Global variable

typedef struct {
    int botHandle[4];
    int* midHandle;
    int topHandle[4];
    int roofHandle;
} SurfaceHandles;

typedef struct {
    Real64 botVal[4];
    Real64* midVal;
    Real64 topVal[4];
    Real64 roofVal;
} SurfaceValues;

SurfaceHandles surHandles;
SurfaceValues surValues;

int midLen = 0;

int handlesRetrieved = 0, weatherHandleRetrieved = 0;
int simHVACSensor = 0, odbActHandle = 0, orhActHandle = 0, odbSenHandle = 0, ohrSenHandle = 0;
int rank = -1, performanc_length =15;
float msg_arr[3] = {-1, -1, -1};
int allDomainLen[NBR_WRF];
float *longall[NBR_WRF], *latall[NBR_WRF];
int *mappings[NBR_WRF];

Building buildings[NBR_IDF]; 
float footprintm2[38] = {
    162.15, 2513.40, 37.75, 355.15, 1049.87, 415.98,
    2608.08, 115.65, 1793.84, 2785.14,958.38,2745.55,
    1292.35,347.83,2464.88,9048.44,548.43,185.96,
    828.75,91.38,107.44,90.02,181.64,1698.19,
    4090.41,24400.54,158.22,4229.28,92.32,108.30,
    3781.44,123.20,3298.50,257.05,841.63,80.27,
    1808.91,889.49
};
int weatherMPIon = 1, wasteMPIon = 1;

MPI_Comm parent_comm;
MPI_Status status;


Real64* tempMidVal;


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
        printf("rank = %d, bot[%d] = %d, top[%d] = %d\n", rank, i, geoUWyo.bot[i], i, geoUWyo.top[i]);
        sprintf(surfaceName, "Surface %d", geoUWyo.bot[i]);
        requestVariable(state, "Surface Outside Face Temperature", surfaceName);
        sprintf(surfaceName, "Surface %d", geoUWyo.top[i]);
        requestVariable(state, "Surface Outside Face Temperature", surfaceName);
    }
    for (int i = 0; i < midLen; i++) {
        printf("rank = %d, mid[%d] = %d\n", rank, i, geoUWyo.mid[i]);
        sprintf(surfaceName, "Surface %d", geoUWyo.mid[i]);
        requestVariable(state, "Surface Outside Face Temperature", surfaceName);
    }

    printf("rank = %d, roof = %d\n", rank, geoUWyo.roof);
    sprintf(surfaceName, "Surface %d", geoUWyo.roof);
    requestVariable(state, "Surface Outside Face Temperature", surfaceName);
}

void getSurHandle(EnergyPlusState state, GeoUWyo geoUWyo) {
    // This function is used to iterate bot, mid, top surfaces. get their handles
    char surfaceName[100];
    for (int i = 0; i < 4; i++) {
        sprintf(surfaceName, "Surface %d", geoUWyo.bot[i]);
        surHandles.botHandle[i] = getVariableHandle(state, "Surface Outside Face Temperature", surfaceName);
        sprintf(surfaceName, "Surface %d", geoUWyo.top[i]);
        surHandles.topHandle[i] = getVariableHandle(state, "Surface Outside Face Temperature", surfaceName);
        // printf("rank%d, getSurHandles, bot[%d] = %d, top[%d] = %d\n", rank, i, surHandles.botHandle[i], i, surHandles.topHandle[i]);
        if (surHandles.botHandle[i] < 0 || surHandles.topHandle[i] < 0) {
            printf("Error: rank %d, surHandles.botHandle[%d] = %d, surHandles.topHandle[%d] = %d, geoUWyo.top[%d] = %d\n",
                   rank, i, surHandles.botHandle[i], i, surHandles.topHandle[i], i, geoUWyo.top[i]);
            exit(1);
        }
    }
    for (int i = 0; i < midLen; i++) {
        sprintf(surfaceName, "Surface %d", geoUWyo.mid[i]);
        // printf("rank%d, getSurHandles, mid[%d] = %d\n", rank, i, geoUWyo.mid[i]);
        surHandles.midHandle[i] = getVariableHandle(state, "Surface Outside Face Temperature", surfaceName);
        if (surHandles.midHandle[i] < 0) {
            printf("Error: surHandles.midHandle[%d] = %d\n", i, surHandles.midHandle[i]);
            exit(1);
        }
    }

    sprintf(surfaceName, "Surface %d", geoUWyo.roof);
    // printf("rank%d, getSurHandles, roof = %d\n", rank, geoUWyo.roof);
    surHandles.roofHandle = getVariableHandle(state, "Surface Outside Face Temperature", surfaceName);
    if (surHandles.roofHandle < 0) {
        printf("Error: surHandles.roofHandle = %d\n", surHandles.roofHandle);
        exit(1);
    }

}

void getSurVal(EnergyPlusState state, SurfaceHandles surHandles) {
    // This function is used to iterate bot, mid, top surfaces. get their values
    for (int i = 0; i < 4; i++) {
        surValues.botVal[i] = getVariableValue(state, surHandles.botHandle[i]);
        surValues.topVal[i] = getVariableValue(state, surHandles.topHandle[i]);
        // printf("rank = %d, getSurVal, botVal[%d] = %.2f, topVal[%d] = %.2f\n", rank, i, surValues.botVal[i], i, surValues.topVal[i]);
    }

    for (int i = 0; i < midLen; i++) {
        surValues.midVal[i] = getVariableValue(state, surHandles.midHandle[i]);
        // printf("rank = %d, getSurVal, midVal[%d] = %.2f\n", rank, i, surValues.midVal[i]);
    }

    surValues.roofVal = getVariableValue(state, surHandles.roofHandle);
    // printf("rank = %d, getSurVal, roofVal = %.2f\n", rank, surValues.roofVal);
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
    // msg_arr[0] += 10; //mannually increase OAT_C by 10 to get Heatwave event
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
        getSurHandle(state, geoUWyoMyRank);
        
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

    getSurVal(state, surHandles);
    // for surValues.midVal, its length is a multiple of 4. Average it into 4 values
    Real64 avgMidVal[4];
    for (int i = 0; i < midLen; i++) {
        avgMidVal[i % 4] += surValues.midVal[i];
    }
    for (int i = 0; i < 4; i++) {
        int num = midLen / 4;
        avgMidVal[i] /= num;
        printf("Botom surface %d temperature = %.2f (C)\n", i, surValues.botVal[i]);
        printf("Mid surface %d temperature = %.2f (C)\n", i, avgMidVal[i]);
        printf("Top surface %d temperature = %.2f (C)\n", i, surValues.topVal[i]);
    }
    // printf("Roof surface temperature = %.2f (C)\n", surValues.roofVal);

    // free(tempMidVal);
    if (!wasteMPIon)
    {
        printf("Child rank = %d wasteMPIon=0, No more MPI, simTime = %.2f (s), simHVAC_W = %.2f (W), \n", rank, simTime, simHVAC_W);
        return;
    }

    float data[performanc_length];
    data[0] = footprintm2[rank%5];
    if (IDF_Coupling == 0)
        data[1] = -66.0;
    else
        data[1] = (float) simHVAC_W;
    // // bot 4, mid 4, top 4
    for (int i = 0; i < 4; i++) {
        data[i + 2] = (float) (surValues.botVal[i] + 273.15);
        data[i + 6] = (float) (avgMidVal[i] + 273.15);
        data[i + 10] = (float) (surValues.topVal[i] + 273.15);
    }
    data[performanc_length - 1] = surValues.roofVal + 273.15;

    MPI_Send(&data, performanc_length, MPI_FLOAT,status.MPI_SOURCE, 0, parent_comm);
    printf("Child %d sent flootaream2 = %.2f (m2), simHVAC_W = %.2f (W),"
        "data[0], data[1] = %.2f, %.2f, data[performanc_length - 1] = %.2f\n", 
        rank, data[0], simHVAC_W, data[0], data[1], data[performanc_length - 1]);
    
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

Mapping_Index closetGridIndex(float bldlat, float bldlong){
    // go through all grids latall, longall, find the closest grid
    double minDist = 1000000000;
    Mapping_Index mapping_index;
    mapping_index.gridIdx = -1;
    mapping_index.wrfIdx = -1;
    for (int j = 0; j < NBR_WRF; j++) {
        for (int i = 0; i < allDomainLen[j]; i++) {
            // double dist = (bldlat - latall[j][i]) * (bldlat - latall[j][i]) + (bldlong - longall[j][i]) * (bldlong - longall[j][i]);
            double dist = distanceBetweenPoints((double) bldlat, (double) bldlong, (double) latall[j][i], (double) longall[j][i]);
            // printf("dist = %.2f, minDist = %.2f\n", dist, minDist);
            if (dist < minDist) {
                minDist = dist;
                mapping_index.gridIdx = i;
                mapping_index.wrfIdx = j;
                // printf("minDist = %.2f, gridIdx = %d, wrfIdx = %d\n", minDist, mapping_index.gridIdx, mapping_index.wrfIdx);
            }
        }
    }

    return mapping_index;
}

void receiveLongLat(void) {
    int horLen = 0, verLen = 0;
    for (int i = 0; i < NBR_WRF; i++) {
        MPI_Recv(&horLen, 1, MPI_INT, i, HOR_LEN_TAG, parent_comm, &status);
        MPI_Recv(&verLen, 1, MPI_INT, i, VER_LEN_TAG, parent_comm, &status);
        printf("Child %d received horLen = %d, verLen = %d from parent %d\n", rank, horLen, verLen, status.MPI_SOURCE);
        allDomainLen[i] = horLen * verLen;
        longall[i] = malloc(allDomainLen[i] * sizeof(float));
        latall[i] = malloc(allDomainLen[i] * sizeof(float));
        mappings[i] = malloc(allDomainLen[i] * sizeof(int) * NBR_IDF);

        for (int j = 0; j < allDomainLen[i] * NBR_IDF; j++) {
            mappings[i][j] = -1;
        }

        MPI_Recv(latall[i], allDomainLen[i], MPI_FLOAT, i, LAT_TAG, parent_comm, &status);
        MPI_Recv(longall[i], allDomainLen[i], MPI_FLOAT, i, LONG_TAG, parent_comm, &status);

        // print the received latlongalls
        for (int k = 0; k < allDomainLen[i]; k++) {
            // // print the received data with higheset precision
            // printf("Child %d received info from WRF %d, longall[%d] = %.10f, latall[%d] = %.10f\n", 
            // rank,i, k, longall[i][k], k, latall[i][k]);
        }
    }

    FILE *file = fopen("./la-resources-23-1-0/la_centroid.csv", "r");
    if (file == NULL) {
        printf("Failed to open la_centroid.csv file.\n");
    }
    // Skip the first line (header) in centroid.csv
    char line[100];
    fgets(line, sizeof(line), file);

    int id;
    double lat, lon;
    for (int i = 0; i < NBR_IDF; i++) {
        fscanf(file, "%d, %lf, %lf", &id, &lat, &lon);
        Mapping_Index mapping_index;
        mapping_index = closetGridIndex(lat, lon);
        mappings[mapping_index.wrfIdx][mapping_index.gridIdx * NBR_IDF + i] = id;

        printf("Building id = %d, lat = %.14lf, lon = %.14lf,"
            "is assigned to WRF#%d, grid %d, lat = %.14lf, lon = %.14lf\n",
            id, lat, lon, mapping_index.wrfIdx, mapping_index.gridIdx,
            latall[mapping_index.wrfIdx][mapping_index.gridIdx],
            longall[mapping_index.wrfIdx][mapping_index.gridIdx]);
    }
    fclose(file);

    for (int j = 0; j < NBR_WRF; j++) {
        MPI_Send(&IDF_Coupling, 1, MPI_INT, j, COUPLING_TAG, parent_comm);
        printf("Child %d sent IDF_Coupling %d to WRF%d\n", rank, IDF_Coupling, j);
        MPI_Send(mappings[j], allDomainLen[j] * NBR_IDF, MPI_INT, j, MAPPING_TAG, parent_comm);
        // for (int k = 0; k < allDomainLen[j] * NBR_IDF; k++) {
        //     printf("Child %d sent mappings[%d][%d] = %d to WRF%d\n", rank, j, k, mappings[j][k], j);
        // }
    }

    for (int i = 0; i < NBR_WRF; i++) {
        free(longall[i]);
        free(latall[i]);
        free(mappings[i]);
    }

}

void parseLine(const char *line, int currentRank) {
    char *lineCopy = strdup(line); // Perform a deep copy of the line
    
    char *token;
    token = strtok(lineCopy, ";"); // Split the line into parts
    
    // Parse id
    sscanf(token, "%d", &geoUWyoMyRank.id);
    // printf("id = %d\n", geoUWyoMyRank.id);
    // Parse bot values
    token = strtok(NULL, ";");
    sscanf(token, "%d, %d, %d, %d", 
        &geoUWyoMyRank.bot[0], &geoUWyoMyRank.bot[1], &geoUWyoMyRank.bot[2], &geoUWyoMyRank.bot[3]);
    // printf("bot = %d %d %d %d\n", 
    //     geoUWyoMyRank.bot[0], geoUWyoMyRank.bot[1], geoUWyoMyRank.bot[2], geoUWyoMyRank.bot[3]);
    
    // Parse midcount
    token = strtok(NULL, ";");
    sscanf(token, "%d", &geoUWyoMyRank.midcount);
    midLen = geoUWyoMyRank.midcount;

    // printf("midcount = %d\n", geoUWyoMyRank.midcount);
    
    // Parse mid values
    geoUWyoMyRank.mid = malloc(geoUWyoMyRank.midcount * sizeof(int));
    surHandles.midHandle = malloc(geoUWyoMyRank.midcount * sizeof(int));
    surValues.midVal = malloc(geoUWyoMyRank.midcount * sizeof(Real64));

    token = strtok(NULL, ",");
    for (int i = 0; i < geoUWyoMyRank.midcount; i++) {
        // printf("Rank = %d, mid %d token = %s\n", currentRank, i, token);
        sscanf(token, "%d", &geoUWyoMyRank.mid[i]);
        if (i < geoUWyoMyRank.midcount - 2) {
            token = strtok(NULL, ",");
        } else if (i == geoUWyoMyRank.midcount - 2) {
            token = strtok(NULL, ";");
        }
    }

    // printf("mid = ");
    // for (int i = 0; i < geoUWyoMyRank.midcount; i++) {
    //     printf("%d ", geoUWyoMyRank.mid[i]);
    // }
    // Parse top values
    token = strtok(NULL, ";");
    sscanf(token, "%d, %d, %d, %d", 
        &geoUWyoMyRank.top[0], &geoUWyoMyRank.top[1], &geoUWyoMyRank.top[2], &geoUWyoMyRank.top[3]);
    printf("Rank %d, top = %d %d %d %d\n", currentRank,
        geoUWyoMyRank.top[0], geoUWyoMyRank.top[1], geoUWyoMyRank.top[2], geoUWyoMyRank.top[3]);
    // Parse roof value
    token = strtok(NULL, ";");
    sscanf(token, "%d", &geoUWyoMyRank.roof);
    printf("Rank %d, roof = %d\n", currentRank, geoUWyoMyRank.roof);

    // Free memory allocated for mid array
    free(lineCopy); // Free the deep copied line
}

void assignGeoData(int currentRank) {
    FILE *file = fopen("./la-resources-23-1-0/surfaceNames.txt", "r");
    if (file == NULL) {
        perror("Failed to open file");
        exit(1);
    }

    char line[1000];
    for (int i = 0; i < currentRank + 2; i++) {
        if (fgets(line, sizeof(line), file) == NULL) {
            fprintf(stderr, "Invalid rank %d and currentRank %d\n", rank, currentRank);
            fclose(file);
            exit(1);
        }
    }

    printf("Rank = %d, line = %s\n", currentRank, line);
    parseLine(line, currentRank);
    fclose(file);
    // free(geoUWyoMyRank.mid);
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
    MPI_Barrier(MPI_COMM_WORLD);
    printf("Child %d: after receiveLongLat\n", rank);
    assignGeoData(rank%5);
    char output_path[MPI_MAX_PROCESSOR_NAME];
    char idfFilePath[MPI_MAX_PROCESSOR_NAME];
    EnergyPlusState state = stateNew();
    callbackBeginZoneTimestepBeforeSetCurrentWeather(state, overwriteEpWeather);
    callbackEndOfSystemTimeStepAfterHVACReporting(state, endSysTimeStepHandler);
    requestVariable(state, "Site Outdoor Air Drybulb Temperature", "ENVIRONMENT");
    requestVariable(state, "Site Outdoor Air Humidity Ratio", "ENVIRONMENT");
    requestVariable(state, "HVAC System Total Heat Rejection Energy", "SIMHVAC");
    requestSur(state, geoUWyoMyRank);
    char curpath[256];
    getcwd(curpath, sizeof(curpath));
    const char* base_path = (strstr(curpath, "glade")) ? "/glade/scratch/lichenwu/ep_temp" : ".";
    // Choose the appropriate folder based on IDF_Coupling value
    printf("base_path = %s\n", base_path);
    sprintf(output_path, "%s/LA_saved_%s_ep_trivial_%d", base_path,
            (IDF_Coupling == 0) ? "offline" : (IDF_Coupling == 1) ? "online1_waste" : "online2_waste_surf",
            rank + 1);
    sprintf(idfFilePath, "./la-resources-23-1-0/in_la_%d.idf",  rank % 5 + 1);
    // printf("output_path = %s\n", output_path);

    char* weather_file_path = "./resources-23-1-0/USA_CA_Hawthorne-Jack.Northrop.Field.722956_TMY3.epw";
    const char* sys_args[] = {"-d", output_path, "-w", weather_file_path, idfFilePath, NULL};
    int argc_ = sizeof(sys_args) / sizeof(char*) - 1;
    printf("argc_ = %d\n", argc_);
    for (int i = 0; i < argc_; i++) {
        printf("sys_args[%d] = %s\n", i, sys_args[i]);
    }
    energyplus(state,argc_, sys_args);
 

    return 0;
}