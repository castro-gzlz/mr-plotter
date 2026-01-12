This model is an updated version of Aguichine et al. (2021) and describes the **thermal and structural evolution of steam worlds** as planets progressively lose their internal heat through their atmospheres. The rocky interior is fixed to an **Earth-like composition**.

The model is provided as a **multidimensional grid** spanning planetary mass, water mass fraction, equilibrium temperature, host-star properties, and age. An **interpolation scheme** allows any parameter value within the model validity range to be explored. While extrapolation is technically possible, it is **not recommended**.


| Parameter | Possible values | Description |
| ------------- | ------------- | ------------- |
| spt_aguich2025 | M or G<sup>**1**</sup> | Spectral type of the host star |
| WMF_aguich2025 | 0.1, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 (%) | Water mass fraction of the hydrosphere |
| Teq_aguich2025 | 400, 500, 700, 900, 1100, 1300, 1500 (K) | Equilibrium temperature of your planet |
| age_aguich2025 | 0.001, 0.0015, 0.002, 0.003, 0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10, 20 (Gyr) | Age of the host star |
| colors_aguich2025 | Any color | Colors of each model |

<sup>**1**</sup> <sub> Interpolation between host star spectral type is not possible </sub>
