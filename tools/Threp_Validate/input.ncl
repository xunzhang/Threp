load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
   
begin

cdf = addfile("real_T42_Gaussian2POP43.nc", "r")                        ;   open netCDF file for lat/lon information

nlat = 128									; if nlat/nlon is not in netcdf file
nlon = 192
;nlat = cdf->nlats
;nlon = cdf->nlons
;varunits = getfilevaratts(cdf, "grid_center_lat")
;print(varunits(0))

;rad2deg = 180 / 3.14159265359				; if units is radians
rad2deg = 1.0								; if units is degrees
lat1d = cdf->grid_center_lat * rad2deg;
lon1d = cdf->grid_center_lon * rad2deg;
lat2d = onedtond(lat1d, (/nlat, nlon/));
lon2d = onedtond(lon1d, (/nlat, nlon/));

; lat/lon for drawing
lats=lat2d(:,0);
lons=lon2d(0,:);
lats@units="degrees_north";
lons@units="degrees_east";

; values to draw
error = cdf->physical_variable

; from 1D to 2D
error2d = onedtond(error, (/nlat, nlon/));
error2d@lat2d=lat2d;
error2d@lon2d=lon2d;

print("Finish data preparation");
; create plot: reference="www.ncl.ucar.edu/Applications/Scripts/proj_1.ncl"

res                     = True;
res@mpProjection        = "CylindricalEquidistant";
res@mpGridAndLimbOn     = True;
res@mpPerimOn           = False;
res@mpGridLatSpacingF   = 30.;
res@mpGridLonSpacingF   = 30.;
res@mpFillOn            = False;

res@mpLimitMode         = "Corners";        choose range of map
res@mpLeftCornerLatF    = - 90.0;
res@mpLeftCornerLonF    = - 180.0;
res@mpRightCornerLatF   =   90.0;
res@mpRightCornerLonF   =   180.0;

res@mpRelativeCenterLon = True;
res@mpCenterLonF        = 0;
res@mpCenterLatF        = 0;
res@tfDoNDCOverlay      = False;
res@cnFillOn            = True;
;res@cnLineLabelOn       = False;
res@cnLinesOn           = False;
res@txFontHeightF       = 0.015;

res@vpXF                = 0.1;
res@vpYF                = 0.9;
res@vpWidthF            = 0.8;
res@vpHeightF           = 0.9;

res@gsnSpreadColors     = True;
res@gsnSpreadColorStart = 2;
res@gsnSpreadColorEnd   = -3;
res@lbLabelFontHeightF  = 0.008
res@lbLabelAngleF       = 45;

res@tiMainFontHeightF   = 0.018

wks_type = "png";
;wks_type = "ps";
wks1 = gsn_open_wks(wks_type, "input_dest_fieldfile tbot");

gsn_define_colormap(wks1, "gui_default");

print("Draw graph 1");
res@tiMainString        = "input destination field tbot"
contour = gsn_csm_contour_map(wks1, error2d(:,:), res);

end
