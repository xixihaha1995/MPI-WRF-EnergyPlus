load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

begin

    a=addfile("~/NWP/WPS/geo_em.d04.nc","r")
    ;a=addfile("~/NWP/WRF/test/em_real/wrfout_d02_2023-05-01_05:00:00.nc","r")
    wks = gsn_open_wks("x11","landuse")
    lu=a->LU_INDEX(0,:,:)
    ;print(lu)
    printVarSummary(lu)
    ter = wrf_user_getvar(a, "LU_INDEX",0)

    res = True
    res@cnFillOn  = True
    res@gsnDraw   = True    ; Forces the plot to be drawn
    res@gsnFrame  = True    ; Frame advance
    contour = wrf_contour(a,wks,ter,res)

    mpres = True
    pltres = True

    plot = wrf_map_overlays(a,wks,(/contour/),pltres,mpres)
end