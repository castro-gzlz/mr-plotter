If you want to download the most recent NEA catalog, just include the following parameter: 

| Parameter  | Possible values | Description |
| ------------- | ------------- | ------------- |
| web_or_local  | web or local  | Download it from the [*Nasa Exoplanet Archive*](https://exoplanetarchive.ipac.caltech.edu/index.html) (**web**) or pick it up from *[catalog_data/NEA](https://github.com/castro-gzlz/mr-plotter/tree/main/catalog_data/NEA)* (**local**)**<sup>1</sup>** |

**<sup>1</sup>** <sub> If **web**, *mr-plotter* will connect to the NEA through a TAP protocol, which might last a bit (i.e., a couple of minutes). If **local**, you should have a comma-separated table downloaded from the NEA inside the *[catalog_data/NEA](https://github.com/castro-gzlz/mr-plotter/tree/main/catalog_data/NEA)* folder. Please do not change the default name of the downloaded tables. If you have several NEA tables, *mr-plotter* will automatically select the most recently downloaded.

