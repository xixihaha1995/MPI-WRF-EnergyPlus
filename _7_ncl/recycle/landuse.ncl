load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
  ;f0=addfile("./geo_em.d01urban.nc","r")
  ;f0=addfile("~/NWP4.5/WRF/test/em_real/saved_normal_bem_010000.nc","r")
  f0=addfile("~/NWP4.5/WPS/geo_em.d01.nc","r")
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