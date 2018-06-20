This tool performs joint timeseries and trend calculation for the HyInt hydroclimatic indices and ETCCDI climate extremes indices over pre-selected continental scale regions or user defined regions. The hydroclimatic indices were selected following Giorgi et al. (2014)':' the simple precipitation intensity index (SDII), the maximum dry spell length (DSL) and wet spell length (WSL), the hydroclimatic intensity index (HY-INT = normalized(SDII) x normalized(DSL)), a measure of the overall behaviour of the hydroclimatic cycle (Giorgi et al., 2011), and the precipitation area (PA), i.e. the area over which at any given day precipitation occurs, (Giorgi et al., 2014). The 27 ETCCDI indices are included in the analysis upon selection from the user. Trends are calculated using the R lm function and significance testing performed with a Student T test on non-null coefficients hypothesis. Trend coefficients are stored together with their statistics which include standard error, t value and Pr(>|t|). The tool produces a variety of types of plots including timeseries with their spread, trend lines and summary plots of trend coefficients.

Figure: output figure type 12 for selected indices and regions calculated for EC-Earth rcp85 over 1976-2100
![example output](diagnosticsdata/hyint_timeseries/hyint_timeseries.png "Example Output")

Figure: output figure type 14 for selected indices and regions calculated for EC-Earth rcp85 over 1976-2100
![example output](diagnosticsdata/hyint_timeseries/hyint_trends1.png "Example Output")
![example output](diagnosticsdata/hyint_timeseries/hyint_trends2.png "Example Output")

### Description of user-changeable settings on webpage:

1)  Selection of model

2)  Selection of period

3)  Selection of reference normalization period to be used for normalized indices

4)  Selection of indices to be plotted from the following list (order-sensitive): "SDII", "DSL", "WSL", "HY-INT", "ABS_INT", "ABS_DSL", "ABS_WSL", "PA", "R95", "altcddETCCDI", "altcsdiETCCDI", "altcwdETCCDI", "altwsdiETCCDI", "cddETCCDI", "csdiETCCDI", "cwdETCCDI", "dtrETCCDI", "fdETCCDI", "gslETCCDI", "idETCCDI", "prcptotETCCDI", "r10mmETCCDI", "r1mmETCCDI", "r20mmETCCDI", "r95pETCCDI", "r99pETCCDI", "rx1dayETCCDI", "rx5dayETCCDI", "sdiiETCCDI", "suETCCDI", "tn10pETCCDI", "tn90pETCCDI", "tnnETCCDI", "tnxETCCDI", "trETCCDI", "tx10pETCCDI", "tx90pETCCDI", "txnETCCDI", "txxETCCDI", "wsdiETCCDI"

5) Select regions for timeseries and maps from the following list: World, World60 (60S/60N), Tropics (30S/30N), South America, Africa, North America, India, Europe, East-Asia, Australia

6) Type of figure: [11] timeseries over required individual region/exp, [12] timeseries over multiple regions/exp, [13] timeseries with multiple models, [14] summary trend coefficients multiple regions, [15] summary trend coefficients multiple models

