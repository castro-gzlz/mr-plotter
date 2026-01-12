To download the most recent version of the NEA catalog, include the following parameter:

| Parameter       | Possible values | Description |
|-----------------|-----------------|-------------|
| `web_or_local`  | `web` or `local` | Retrieve the catalog directly from the [*NASA Exoplanet Archive*](https://exoplanetarchive.ipac.caltech.edu/index.html) (**web**) or load it from the local folder *[catalog_data/NEA](https://github.com/castro-gzlz/mr-plotter/tree/main/catalog_data/NEA)* (**local**)<sup>1</sup> |

**<sup>1</sup>** <sub>
If `web` is selected, *mr-plotter* connects to the NEA via the **TAP protocol**, which may take a few minutes.  
If `local` is selected, a comma-separated table downloaded from the NEA must be present in the *[catalog_data/NEA](https://github.com/castro-gzlz/mr-plotter/tree/main/catalog_data/NEA)* folder. Please do not modify the default filenames. If multiple NEA tables are available, *mr-plotter* will automatically select the most recently downloaded one.
</sub>
