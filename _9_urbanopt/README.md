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
