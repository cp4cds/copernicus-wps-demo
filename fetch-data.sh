#!/bin/bash

CERT="cert.pem"
ARCHIVE="/path/to/cmip5/archive"

CMD=wget --certificate $CERT --private-key $CERT --ca-certificate $CERT -N -x -P $ARCHIVE

$CMD http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output1/MPI-M/MPI-ESM-LR/historical/mon/atmos/Amon/r1i1p1/v20120315/ta/ta_Amon_MPI-ESM-LR_historical_r1i1p1_200001-200512.nc
$CMD http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output1/MPI-M/MPI-ESM-LR/historical/mon/atmos/Amon/r1i1p1/v20120315/pr/pr_Amon_MPI-ESM-LR_historical_r1i1p1_185001-200512.nc
$CMD http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output1/MPI-M/MPI-ESM-LR/historical/mon/atmos/Amon/r1i1p1/v20120315/tas/tas_Amon_MPI-ESM-LR_historical_r1i1p1_185001-200512.nc
