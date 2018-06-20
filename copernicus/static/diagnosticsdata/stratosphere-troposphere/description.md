This python tool is based on the algorithm proposed by [Baldwin and Thompson, 2009], and requires the daily geopotential height field on pressure levels as input. The method is based on an EOF/PC decomposition of the zonally averaged geopotential height, with the leading pattern of variability representative of the (zonal mean) NAM. The calculation is independently repeated at each available pressure level. The daily index can be used to characterize episodic variability of the stratosphere-troposphere connection, while regression on the monthly averaged index is used to quantify the signature of the NAM on the hemispheric climate.

To evaluate the modelled strat-trop coupling, the metric is based on the spatial patterns of the zonal mean NAM index. This is obtained by projecting monthly anomalies of the geopotential height field onto the monthly averaged index, then normalized. The well-known annular pattern emerges at upper levels, and it is generally less longitudinally symmetric moving towards the surface.
Having calculated the reanalysis-based spatial patterns, it is possible to compute the difference between these patterns and those reproduced by climate models. The resulting spatial patterns can be used to assess the differences in the strength of this mode of variability and the latitudinal extent.

![example output](diagnosticsdata/stratosphere-troposphere/test250.png "Example Output")

### Description of user-changeable settings on webpage

1) Selection of model;

2) Selection of period;

3) Selection of supplementary pressure levels


