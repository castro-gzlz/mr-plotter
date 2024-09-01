| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| n_cols | one or two | Make the plot in one-column or two-column. **Default**: one |
| color_min | Any | Minimum **value** for the color coding. **Default:** median of the 5% minimum values |
| color_max | Any | Maximum **value** for the color coding. **Default:** median of the 5% maximum values |
| log_x | True or False | Logarithmic scale on the $X$-axis. **Default:** True |
| log_y | True of False| Logarithmic scale on the $Y$-axis. **Default:** True |
| xlim | Any, Any | Limits of the plot on the $X$-axis. **Default:** 0.5, 21 |
| ylim | Any, Any | Limits of the plot on the $Y$-axis. **Default:** 0.9, 2.8 |
| size_NEA_planets | Any | Size of NEA planets. **Default:** 120 |
| size_my_planets | Any | Size of my planets. **Default:** 200 |
| low_density_superEarths | True or False | Plot the low-density super-Earths region shown in [Castro-González et al. (2023)](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract). **Default:** False|
| shade_below_pure_iron | True or False | Include a grey shade below the 100% iron model by [Zeng et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract). **Default**: True |
| loc_legend | best, upper left, center, etc | Location of the legend. **Default:** lower right|
| cmap | Any [matplotlib colormap](https://matplotlib.org/stable/tutorials/colors/colormaps.html) | Color map for the color-coded diagrams. **Default:** rainbow |
