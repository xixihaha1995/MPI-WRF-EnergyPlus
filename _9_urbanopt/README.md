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


<!-- The following is used to filer only eplustbl.htm for further processing -->
```bash
find IDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_IDFs38_ep_temp \;

mkdir copy_100mIDFs38_ep_temp
find 100mIDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_100mIDFs38_ep_temp \;
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_100mIDFs38_ep_temp 100mIDFs38_ep_temp\

mkdir copy_july1_100mIDFs38_ep_temp
find july1_100mIDFs38_ep_temp -name "eplustbl.htm" -exec cp --parents {} copy_july1_100mIDFs38_ep_temp \;
scp -r  lichenwu@cheyenne.ucar.edu:/glade/scratch/lichenwu/copy_july1_100mIDFs38_ep_temp july1_100mIDFs38_ep_temp\
```
