This namelist calls RainFARM (https://github.com/jhardenberg/RainFARM.jl). RainFARM is a Julia library and command-line tools implementing the RainFARM stochastic precipitation downscaling method adapted for climate models. The stochastic method is a weather generator which allows to generate fine-scale precipitation fields with a realistic correlation structure, extrapolating to fine scales information  simulated by climate models at regional scales.  RainFARM exploits the nonlinear transformation of a Gaussian random precipitation field obtained extrapolating to small scales the large-scale power spectrum of the fields. It conserves average precipitation at coarse scale (Rebora et al. 2006, D'Onofrio et al. 2014). Description of user-changeable settings on webpage 1) Selection of model; 2) Selection of period; 3) Selection of longitude and latitude.

Figure: original precipitation (mm/day) field (left) and the downscaled field (right) for the EC-Earth model over central Europe.
![example output](diagnosticsdata/rainfarm/RainFARM_example_8x8.png "Example Output")
![example output](diagnosticsdata/rainfarm/RainFARM_example_64x64.png "Example Output")


### Description of user-changeable settings on webpage

1) Selection of model;

2) Selection of period;

3) Selection of longitude and latitude: [lon1,lon2,lat1,lat2], with lon(0/360). Subsetting of region where calculation is to be performed. The selected region needs to have equal number of longitude and latitude grid points;

4) Regridding (preprocessing option): default option false;

5) spatial spectral slope adopted to produce data at local scale (computed from large scales if not specified);

6) number of ensemble members to be calculated;

7) number of subdivisions for downscaling
