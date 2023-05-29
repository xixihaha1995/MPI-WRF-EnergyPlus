#!/usr/bin/env csh
#
# c-shell script to download selected files from rda.ucar.edu using Wget
# NOTE: if you want to run under a different shell, make sure you change
#       the 'set' commands according to your shell's syntax
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
# Experienced Wget Users: add additional command-line flags to 'opts' here
#   Use the -r (--recursive) option with care
#   Do NOT use the -b (--background) option - simultaneous file downloads
#       can cause your data access to be blocked
set opts = "-N"
#
# Check wget version.  Set the --no-check-certificate option 
# if wget version is 1.10 or higher
set v = `wget -V |grep 'GNU Wget ' | cut -d ' ' -f 3`
set a = `echo $v | cut -d '.' -f 1`
set b = `echo $v | cut -d '.' -f 2`
if(100 * $a + $b > 109) then
  set cert_opt = "--no-check-certificate"
else
  set cert_opt = ""
endif

set filelist= ( \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230501_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230501_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230501_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230501_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230502_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230502_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230502_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230502_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230503_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230503_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230503_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230503_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230504_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230504_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230504_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230504_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230505_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230505_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230505_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230505_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230506_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230506_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230506_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230506_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230507_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230507_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230507_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230507_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230508_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230508_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230508_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230508_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230509_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230509_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230509_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230509_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230510_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230510_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230510_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230510_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230511_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230511_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230511_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230511_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230512_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230512_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230512_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230512_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230513_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230513_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230513_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230513_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230514_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230514_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230514_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230514_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230515_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230515_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230515_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230515_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230516_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230516_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230516_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230516_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230517_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230517_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230517_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230517_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230518_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230518_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230518_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230518_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230519_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230519_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230519_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230519_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230520_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230520_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230520_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230520_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230521_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230521_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230521_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230521_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230522_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230522_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230522_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230522_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230523_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230523_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230523_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230523_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230524_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230524_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230524_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230524_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230525_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230525_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230525_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230525_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230526_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230526_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230526_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230526_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230527_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230527_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230527_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230527_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230528_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230528_06_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230528_12_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230528_18_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230529_00_00.grib2  \
  https://stratus.rda.ucar.edu/ds083.2/grib2/2023/2023.05/fnl_20230529_06_00.grib2  \
)
while($#filelist > 0)
  set syscmd = "wget $cert_opt $opts $filelist[1]"
  echo "$syscmd ..."
  $syscmd
  shift filelist
end
