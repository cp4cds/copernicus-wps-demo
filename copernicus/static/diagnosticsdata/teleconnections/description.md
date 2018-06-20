This functionality is implemented in the namelist MId-Latitude Evaluation System (MiLES), also available as stand-alone package (https://github.com/oloapinivad/MiLES). The tool works on daily 500hPa geopotential height data (with data interpolated on a common 2.5x2.5 grid) and calculates the following diagnostics':'
  -  Z500 Empirical Orthogonal Functions':' Based on CDO "eofs" function. First 4 EOFs for North Atlantic (over the 90W-40E 20N-85N box) and Northern Hemisphere (20N-85N). North Atlantic Oscillation, East Atlantic Pattern, and Arctic Oscillation are thus computed. Figures showing linear regression of PCs on monthly Z500 are provided. PCs and eigenvectors, as well as the variances explained are provided in NetCDF4 Zip format.
  -  North Atlantic Weather Regimes (beta)':' following k-means clustering of 500hPa geopotential height. 4 weather regimes over North Atlantic (80W-40E 30N-87.5N) are evaluted using anomalies from daily seasonal cycle. North Atlantic 4 EOFs are computed to reduce the phase-space dimension and then k-means clustering using Hartigan-Wong algorithm with k=4 is computed. Figures report patterns and frequencies of occurrence. NetCDF4 Zip data are saved. Only 4 regimes and DJF supported so far. 

![example output](diagnosticsdata/teleconnections/EOF1_MPI-ESM-P_r1_1951_2005_DJF.png "NAO EOF1")
![example output](diagnosticsdata/teleconnections/Regime2_MPI-ESM-P_r1_1951_2005_DJF.png "Regimes")

### Description of user-changeable settings on webpage: 

1) Selection of model

2) Selection of reference dataset

3) Selection of period 

4) Selection of season

5) Teleconnection mode (NAO, AO)
