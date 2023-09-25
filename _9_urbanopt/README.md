```
ConvergenceLimits,
  0,                       !- Minimum System Timestep {minutes}
  25;                      !- Maximum HVAC Iterations
  
Schedule:File,
  New York 2019 Historical Hourly Emissions Sch,  !- Name
  Emissions Sch File Type Limits,  !- Schedule Type Limits Name
  future_hourly_co2e_2030.csv,  !- File Name
```  

https://docs.urbanopt.net/urbanopt-geojson-gem/schemas/building-properties.html
https://www.mapdevelopers.com/area_finder.php

/c/URBANopt-cli-0.9.2/setup-env.sh
/usr/local/urbanopt-cli-0.9.3/setup-env.sh
. ~/.env_uo.sh

uo create -p C:\\Users\\wulic\\uo9.2

uo create -s uo9.2/example_project.json
uo run -s uo9.2/baseline_scenario.csv -f uo9.2/example_project.json


Double click `IDFVersionUpdater` to executate

<!-- The following is used to filer only eplustbl.htm for further processing -->
```bash
find IDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_IDFs38_ep_temp \;

mkdir copy_100mIDFs38_ep_temp
find 100mIDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_100mIDFs38_ep_temp \;
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_100mIDFs38_ep_temp 100mIDFs38_ep_temp\

mkdir copy_july1_100mIDFs38_ep_temp
find july1_100mIDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_july1_100mIDFs38_ep_temp \;
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_july1_100mIDFs38_ep_temp july1_100mIDFs38_ep_temp\

find july2_100mIDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_july2_100mIDFs38_ep_temp \;
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_july2_100mIDFs38_ep_temp july2_100mIDFs38_ep_temp\

find . -type f \( -name "online.log.energyplus" -o -name "offline.log.energyplus" \) -exec cp --parents {} ./all_Logs \;

scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/all_Logs all_Logs\

find TMY3_WY_IDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_TMY3_WY_IDFs38_ep_temp \;
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_TMY3_WY_IDFs38_ep_temp TMY3_WY_IDFs38_ep_temp\

find TMY3_LA_IDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_TMY3_LA_IDFs38_ep_temp \;
find la_72hrs500m_IDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_la_72hrs500m_IDFs38_ep_temp \;

scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_la_72hrs500m_IDFs38_ep_temp la_72hrs500m_IDFs38_ep_temp\
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_TMY3_LA_IDFs38_ep_temp TMY3_LA_IDFs38_ep_temp\

scp -r  lichenwu@cheyenne.ucar.edu:/glade/u/home/lichenwu/project/NWP/WRF-la-on-72hrs/test/em_real/rsl.out.0000 override.rsl.out.0000

find 1000m-30flrs -name "eplustbl.htm" -exec cp --parents {} copy-1000m-30flrs \;
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/ASHRAE2024/copy-1000m-30flrs 1000m-30flrs\
```
