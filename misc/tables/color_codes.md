# Available color codes

This document lists all parameters that can be used for **color coding** in *mr-plotter*, depending on the selected exoplanet catalog.

---

## NASA Exoplanet Archive (NEA)

The following color codes can be used when selecting the **NEA** catalog.

### Non-numerical parameters
| Code            | Description            |
|-----------------|------------------------|
| `none`          | No color coding        |
| `disc_year`     | Discovery year         |
| `disc_facility` | Discovery facility     |
| `discoverymethod` | Discovery method    |

### Planetary parameters
| Code            | Description                          | Units |
|-----------------|--------------------------------------|-------|
| `pl_orbper`     | Orbital period                       | days  |
| `pl_orbsmax`    | Semi-major axis                      | AU    |
| `pl_orbeccen`   | Orbital eccentricity                 | —     |
| `pl_insol`      | Insolation flux                      | S⊕    |
| `pl_eqt`        | Equilibrium temperature              | K     |
| `pl_rvamp`      | Radial-velocity semi-amplitude       | m/s   |
| `pl_trandep`    | Transit depth                        | —     |

### Stellar parameters
| Code            | Description                          | Units |
|-----------------|--------------------------------------|-------|
| `st_teff`       | Stellar effective temperature        | K     |
| `st_rad`        | Stellar radius                       | R⊙    |
| `st_mass`       | Stellar mass                         | M⊙    |
| `st_met`        | Stellar metallicity                  | dex   |
| `st_logg`       | Stellar surface gravity              | dex   |
| `st_lum`        | Stellar luminosity                   | log(L⊙) |
| `st_age`        | Stellar age                          | Gyr   |

### System parameters
| Code            | Description          | Units |
|-----------------|----------------------|-------|
| `sy_dist`       | Distance             | pc    |
| `sy_vmag`       | V-band magnitude     | mag   |
| `sy_kmag`       | Ks-band magnitude    | mag   |
| `sy_gaiamag`    | Gaia G magnitude     | mag   |

---

## PlanetS catalog

The [*PlanetS*](https://dace.unige.ch/exoplanets/) catalog includes **all NEA parameters listed above**, and provides additional quantities computed **homogeneously for the full sample**.

### Spectroscopy metrics
| Code  | Description                         |
|-------|-------------------------------------|
| `TSM` | Transmission Spectroscopy Metric    |
| `ESM` | Emission Spectroscopy Metric        |

### Homogeneously computed planetary parameters
| Code                | Description                 | Units |
|---------------------|-----------------------------|-------|
| `pl_insol_PlanetS`  | Insolation flux             | S⊕    |
| `pl_eqt_PlanetS`    | Equilibrium temperature     | K     |

### Gaia DR3 stellar parameters
| Code              | Description                          | Units |
|-------------------|--------------------------------------|-------|
| `st_teff_gaia`    | Stellar effective temperature        | K     |
| `st_met_gaia`     | Stellar metallicity                  | dex   |
| `st_logg_gaia`    | Stellar surface gravity              | dex   |
| `st_age_gaia`     | Stellar age                          | Gyr   |
| `st_lum_gaia`     | Stellar luminosity                   | log(L⊙) |

---

## Exoplanet.eu catalog

The **Exoplanet.eu** catalog supports the **same color codes as the NASA Exoplanet Archive**.
