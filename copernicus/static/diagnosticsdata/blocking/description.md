This functionality is implemented in the namelist MId-Latitude Evaluation System (MiLES), also available as stand-alone package (https://github.com/oloapinivad/MiLES). The tool works on daily 500hPa geopotential height data (with data interpolated on a common 2.5x2.5 grid) and calculates the following diagnostics: 1D Atmospheric Blocking:
  Tibaldi and Molteni (1990) index for Northern Hemisphere. Computed at fixed latitude of 60N, with delta of -5,-2.5,0,2.5,5 deg, fiN=80N and fiS=40N. Full timeseries and climatologies are provided in NetCDF4 Zip format.
  2D Atmospheric blocking: following the index by Davini et al. (2012). It is a 2D version of Tibaldi and Molteni (1990) for Northern Hemisphere atmospheric blocking evaluating meridional gradient reversal at 500hPa. It includes also Meridional Gradient Index and Blocking Intensity index and Rossby wave orientation index, computing both Instantenous Blocking and Blocking Events frequency. Blocking Events allow the estimation of the blocking duration. A supplementary Instantaneous Blocking index with the GHGS2 conditon is also evaluted. Full timeseries and climatologies are provided in NetCDF4 Zip format.

![example output](diagnosticsdata/blocking/TM90_MPI-ESM-P_r1_1951_2005_DJF.png "Example Output")
![example output](diagnosticsdata/blocking/BlockEvents_MPI-ESM-P_r1_1951_2005_DJF.png "Example Output")

### Description of user-changeable settings on webpage: 

1) Selection of model

2) Selection of reference dataset 

3) Selection of period

4) Selection of season
