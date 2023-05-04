load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
  ;f0=addfile("./geo_em.d01urban.nc","r")
  f0=addfile("./wrfout_d01_2023-05-01_06:00:00urban.nc","r")
  ;f0=addfile("./met_em.d01.2023-05-01_00:00:00.nc","r")
  ;lon=f0->XLONG_M(0,:,:)
  ;lat=f0->XLAT_M(0,:,:)
  lu=f0->LU_INDEX(0,:,:)
  ;lu = f0->LANDUSEF(0,58,:,:)
  print(lu)
  ;printVarSummary(lon)
  ;printVarSummary(lat)
  printVarSummary(lu)
   cmap = read_colormap_file("./cmap_Qgis_CGLC_MOD_LCZ.txt")
  wks = gsn_open_wks("x11","landuse")
  gsn_define_colormap(wks,cmap)
  ;gsn_define_colormap(wks,"BlueYellowRed")

    res                  = True               ; plot mods desired
    res@cnFillOn         = True               ; color Fill
    plot = gsn_csm_contour_map(wks, lu, res)

end