This namelist implements the HyInt tool to calculate a set of 6 indices that allow to evaluate the response of the hydrological cycle to global warming with a joint view of both wet and dry extremes. The indices were selected following Giorgi et al. (2014)':' the simple precipitation intensity index (SDII), the maximum dry spell length (DSL) and wet spell length (WSL), the hydroclimatic intensity index (HY-INT = normalized(SDII) x normalized(DSL)), a measure of the overall behaviour of the hydroclimatic cycle (Giorgi et al., 2011), and the precipitation area (PA), i.e. the area over which at any given day precipitation occurs, (Giorgi et al., 2014). The tool can then produce multi-model and multi-indices maps including the 27 ETCDDI climate extreme indices.

Figure: output figure type 1 for the hyint index calculated for EC-Earth rcp85 multi year mean over 1976-2100 with boxes for user-selected regions

![example output](diagnosticsdata/hyint/hyint_EC-Earth_rcp85_r8i1p1_r320x160_1976_2100_ALL_myear-mean_Globe_map.png "Example Output")

### Description of user-changeable settings on webpage:

1)  Selection of model

2)  Selection of period

3)  Selection of reference normalization period to be used for normalized indices

4)  Selection of indices to be plotted from the following list (order-sensitive): "SDII", "DSL", "WSL", "HY-INT", "ABS_INT", "ABS_DSL", "ABS_WSL", "PA", "R95", "altcddETCCDI", "altcsdiETCCDI", "altcwdETCCDI", "altwsdiETCCDI", "cddETCCDI", "csdiETCCDI", "cwdETCCDI", "dtrETCCDI", "fdETCCDI", "gslETCCDI", "idETCCDI", "prcptotETCCDI", "r10mmETCCDI", "r1mmETCCDI", "r20mmETCCDI", "r95pETCCDI", "r99pETCCDI", "rx1dayETCCDI", "rx5dayETCCDI", "sdiiETCCDI", "suETCCDI", "tn10pETCCDI", "tn90pETCCDI", "tnnETCCDI", "tnxETCCDI", "trETCCDI", "tx10pETCCDI", "tx90pETCCDI", "txnETCCDI", "txxETCCDI", "wsdiETCCDI"

5) Type of figure: 1) lon/lat maps per individual field/exp/multi-year mean, 2) lon/lat maps per individual field exp-ref-diff/multi-year mean, 3) lon/lat maps multi-field/exp-ref-diff/multi-year mean (figure type 3 resembles Giorgi et al. 2011).
