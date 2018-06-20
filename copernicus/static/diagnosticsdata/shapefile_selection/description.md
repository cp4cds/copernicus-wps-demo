![example output](diagnosticsdata/shapefile_selection/Basin_grid2.png "Example Output")

### Description
The user provides a shapefile with one or more polygons. For each polygon, a new timeseries, or CII, is produced with only one time series per polygon. The spatial information is reduced to a representative point ('representative') or as an average of all grid points within the polygon ('mean_inside').     If there are no grid points strictly inside the polygon, 'mean_inside' method defaults to 'representative' for that polygon. Outputs are in the form of a NetCDF file, or as ascii code in csv format.
