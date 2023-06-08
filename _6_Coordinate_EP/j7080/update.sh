#!/bin/bash

# Step 1: Copy a to b
cp saved.module_sf_bep_bem.F /home/xxx/NWP/WRF/phys/module_sf_bep_bem.F 
cp -r resources /home/xxx/NWP/WRF/test/em_real/
cp -r python_standard_lib /home/xxx/NWP/WRF/test/em_real/
make
cp -f child.exe /home/xxx/NWP/WRF/test/em_real/

# Step 3: Git add
git add .

# Step 4: Git commit
git commit -m "dummy"

# Step 5: Git push
git push
