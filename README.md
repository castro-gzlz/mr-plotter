# **mr-plotter: Mass-Radius Diagrams Plotter**

<p>
  <img src="https://github.com/user-attachments/assets/8fce48e4-944f-4389-a38d-c3006b8c4e8d"
       align="left"
       width="320"
       style="margin-right: 20px; margin-bottom: 10px;"
       alt="Example mass–radius diagram">

*mr-plotter* is a **user-friendly** tool designed to produce **paper-quality mass–radius diagrams** based on a **broad selection of** [state-of-the-art models](#models--include-theoretical-models) of **planetary interiors and atmospheres**.

It allows you to **contextualize new planets**, **infer their possible internal structures**, and **explore population-level correlations** through flexible **color-coding** based on planetary and stellar properties available in different catalogs.

If your favorite model is not yet implemented, if you encounter any usage issues, or if you have suggestions for improvement, feel free to [contact me](mailto:amadeo.castro-gonzalez@unige.ch). The code is open to [contributors](https://github.com/castro-gzlz/mr-plotter?tab=readme-ov-file#contributors-and-change-log) 🙂. For interactive mass–radius diagrams with sliders, check out [MARDIGRAS](https://github.com/an0wen/MARDIGRAS).

## Installation & Requirements

Simply **clone or download the repository** to your local machine. Most dependencies are widely used, but if any are missing, you can install them by navigating to the project directory and running:

```bash
pip install -r requirements.txt
```

If you encounter any installation issues, please open an issue [here](https://github.com/castro-gzlz/mr-plotter/issues).

## Usage

#### From the terminal

Create a configuration file named *[my_config_file.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/my_config_file.ini)* inside the [*config*](https://github.com/castro-gzlz/mr-plotter/tree/main/config) folder, and run:

```bash
python mr-plotter.py my_config_file.ini
```

The configuration file should contain all the information required to generate the plot, which will be saved in the [*output*](https://github.com/castro-gzlz/mr-plotter/tree/main/output) folder. All available parameters (both [mandatory](#mandatory-parameters) and [optional](#optional-parameters)) are described in the [**Configuration file**](#configuration-file) section.

#### From a Jupyter Notebook

Since September 2024 (v1+), *mr-plotter* can also be used from a Jupyter Notebook (`mr-plotter.ipynb`). As in the terminal workflow, simply select a configuration file (`config_file`) and run all cells.

## Is this your first time using *mr-plotter*?

If so, don’t worry about the large number of available parameters. **In most cases, you will only need a few**. To **get familiar with the main options** and **gain a first hands-on experience** with *mr-plotter*, we encourage you to check the [**Usage examples**](#usage-examples) section, which illustrates the package workflow in **several key scenarios**. All example configuration files can be found in the [*config*](https://github.com/castro-gzlz/mr-plotter/tree/main/config) folder. Enjoy 🙂.


## Usage examples

### Example 1: The simplest case. Contextualizing a new planetary system
In this example, we contextualize the planet TOI-244 b using data from the [NEA](https://exoplanetarchive.ipac.caltech.edu/) catalog. We also include several theoretical mass–radius models for **rocky planets**, **water worlds**, and **gas dwarfs** from [Zeng et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract).

```bash
python mr-plotter.py example1_toi244.ini
```

We can also contextualize multiple planets within the same diagram. In the following example, a **faint appearance** is used to better highlight the planets HD 21520 b, TOI-469 b, TOI-469 d, and LHS 1140 c. In this case, we use the [Exoplanet.eu](https://exoplanet.eu/home/) catalog and include planet names in the legend to avoid excessively overloading the figure.

```bash
python mr-plotter.py example1_misc.ini
```

![example1_joint](https://github.com/user-attachments/assets/2457c704-9e5d-47d5-9a02-33683583e0db)

### Example 2: [Colouring my worlds](https://www.youtube.com/watch?v=fKtwi3cNtEs) and including steam water atmospheres

We now **include a color code** based on the stellar host metallicity. We also include three theoretical mass–radius models derived from the equations of [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract). These models consider a **steam water atmosphere** over a rocky composition. As shown, a small amount of steam (0.3–5% in mass) forming an extended hydrosphere can naturally explain the composition of the [emerging population of low-density super-Earths](https://ui.adsabs.harvard.edu/abs/2023A%26A...675A..52C/abstract). These models are valid up to a **5% water mass fraction (WMF)**. Above this value, the models from [Aguichine et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract) are more appropriate, as they cover a validity range between **10% and 100% core mass fraction (CMF) and WMF**. We also include models from Aguichine et al. (2021): 30% CMF & 10% WMF (400 K), and 30% CMF & 20% WMF (400 K).

```bash
python mr-plotter.py example2_met.ini
```

We then run the same example using a color code based on the **received stellar insolation flux**. In both cases, we customize the planet marker sizes using the *size_catalog_planets* parameter, and control the color scale limits via the *color_min* and *color_max* parameters.

```bash
python mr-plotter.py example2_insol.ini
```

![example2_joint](https://github.com/user-attachments/assets/a2e09bee-5949-421b-bae0-79bc7ebbbf77)

Wait! do you see what I’m seeing? **Low-density super-Earths appear to be hosted by metal-poor stars and tend to receive relatively low insolation fluxes!** If you are interested in this result, see Sect. 5.3 of [this work](https://ui.adsabs.harvard.edu/abs/2023A%26A...675A..52C/abstract).

### Example 3: Evolutionary models (with interpolators!) of steam worlds and gas dwarfs

Early interior models traditionally focused on end-member compositions (e.g. Earth-like, 50% water). However, it is now known that planetary radii are also sensitive to **secondary parameters**, such as equilibrium temperature, system age, and host star properties. In recent years, interior structure models have increasingly been used to **precisely infer ranges of bulk compositions**, in part thanks to tools such as [smint](https://github.com/cpiaulet/smint). This has led to the publication of planetary radii in the form of **large multidimensional grids** spanning wide regions of parameter space, with intermediate values obtained via interpolation. In this example, we illustrate two such evolutionary models. 

First, an interior model adapted to **steam worlds** from [Aguichine et al. (2025)](https://ui.adsabs.harvard.edu/abs/2025ApJ...988..186A/abstract):

```bash
python mr-plotter.py example3_evolmodels_aguichine.ini
```
Second, an interior model adapted to **gas dwarfs** from [Tang et al. (2025)](https://ui.adsabs.harvard.edu/abs/2025ApJ...989...28T/abstract):

```bash
python mr-plotter.py example3_evolmodels_aguichine_tang.ini
```

<img width="5626" height="2441" alt="example3_joint" src="https://github.com/user-attachments/assets/95cd817c-1a21-429a-9162-6a81e04b0561" />

These models provide grids of radii as functions of **planet mass, composition, equilibrium temperature, age**, and **host star properties** (spectral type and envelope metallicity). Thanks to interpolation, **mass–radius relations can be generated for any value**, and not only for the discrete grid points. The interpolation scheme implemented here follows that of [MARDIGRAS](https://github.com/an0wen/MARDIGRAS). While extrapolation is technically possible, it is **not recommended**. A full list of input parameters and their respective validity ranges can be found in the [[MODELS]](#models--include-theoretical-models) section.

As an illustrative case, the planet TOI-270 d has measured properties (mass, radius, equilibrium temperature, but unknown age) that are compatible with a **50% steam envelope**, a **0.5% H₂-He envelope at 1×Solar metallicity**, or any intermediate configuration. Its transmission spectrum was recently obtained with JWST [Benneke et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024arXiv240303325B/abstract), revealing a **high-metallicity atmosphere (~50%)**.

### Example 4: Two-column plots, isodensity curves, and additional interior models

*mr-plotter* can also generate **two-column figures**. In this example, we contextualize the dense super-Earth K2-229 b by including several interior structure models and reference curves.

Specifically, we show:
- a set of **isodensity curves**
- the **maximum mantle collisional stripping** model from [Marcus et al. (2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M/abstract)
- the **BICEPS** model from [Haldemann et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024A%26A...681A..96H/abstract) for different pure-iron compositions (C0 and C1)
- the pioneering mass–radius relations for **pure-rock** and **pure-water** compositions from [Seager et al. (2007)](https://ui.adsabs.harvard.edu/abs/2007ApJ...669.1279S/abstract)

```bash
python mr-plotter.py example4.ini
```

<img width="4968" height="2293" alt="example4" src="https://github.com/user-attachments/assets/02123950-a6df-41c3-90ea-14d39028272a" />


### Example 5: Empirical mass–radius relations and TSM/ESM color coding

In this example, we illustrate how *mr-plotter* can be used to **visualize empirical mass–radius relations** for small, intermediate, and giant planets, together with **observational prioritization metrics** such as the Transmission and Emission Spectroscopy Metrics (**TSM and ESM**). We include the empirical relations derived by [Parc et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract). The planetary sample is taken from the [*PlanetS*](https://dace.unige.ch/exoplanets/) catalog ([Otegi et al. 2020](https://ui.adsabs.harvard.edu/abs/2020A%26A...634A..43O/abstract); [Parc et al. 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract)), which also served as the basis for deriving these relations.

```bash
python mr-plotter.py example5_TSM.ini
```

The same visualization can be produced using the **ESM**. The transition between small and intermediate planets is marked by the **20% water composition line at 650 K** from [Luo et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024NatAs.tmp..205L/abstract), while the boundary between intermediate and giant planets is defined by the **138 M<sub>⊕</sub> iso-mass line**, following Parc et al. (2024).

```bash
python mr-plotter.py example5_ESM.ini
```

<img width="5608" height="2254" alt="example5_joint" src="https://github.com/user-attachments/assets/22940d4b-745b-44bd-bd43-646cc294504d" />


### Example 6: Non-numerical color coding and dark plots. The TESS legacy

Some parameters, such as **discovery year**, **discovery facility**, or **discovery technique**, are naturally **categorical rather than numerical**. Since v1+, *mr-plotter* allows these quantities to be used for **group-based color coding**. In this example, we first generate a mass–radius diagram of small planets, **color-coded by discovery year**:

```bash
python mr-plotter.py example6_year.ini
```

This representation highlights the rapid pace of recent exoplanet discoveries. We then produce the same diagram by distinguishing between the three main space-based planet-hunting missions: **Kepler**, **K2**, and **TESS**:

```bash
python mr-plotter.py example6_facility.ini
```

This visualization clearly illustrates the remarkable legacy of **TESS**, driven by its continuous monitoring of the bright sky. It also demonstrates how to generate **dark, poster-ready and presentation-ready** mass–radius diagrams suitable for conferences and outreach.

<img width="5596" height="2414" alt="example6_joint" src="https://github.com/user-attachments/assets/6286dacf-8acb-4160-ac61-868353feff0e" />

</br>

Finally, this example shows how to contextualize an individual planet (in this case **L 98-59 d**) using:

- a **custom color not present in the original color map** (left panel), and
- a color assigned according to a **non-numerical category** (right panel; L 98-59 d was discovered by **TESS**)

## Configuration file

### Mandatory parameters

#### [CATALOG_DATA] | Include data from the *NASA Exoplanet Archive*, *Exoplanet.eu*, or *PlanetS* catalogs

| Parameter          | Possible values                                   | Description                          |
|--------------------|---------------------------------------------------|--------------------------------------|
| catalog            | NEA, Exoplanet.eu, or PlanetS                     | Exoplanet catalog to visualize       |
| precision_mass     | From 0 to 100 (%)                                 | Minimum precision in mass            |
| precision_radius   | From 0 to 100 (%)                                 | Minimum precision in radius          |
| color_coding       | none, st_met, pl_insol, st_teff, sy_kmag, etc<sup>**1,2**</sup> | Color coding of the plot             |

**<sup>1</sup>** <sub>The full list of parameters that can be used to color *mr-plots* can be found [here](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/color_codes.md).</sub><br />
**<sup>2</sup>** <sub>For non-numerical color codes (e.g. `disc_facility`), the groups to display and their associated colors must be defined (see how [here](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/non_numerical_config.md)).</sub>

The package can access catalog data **locally** from different folders inside [*catalog_data*](https://github.com/castro-gzlz/mr-plotter/tree/main/catalog_data). Although we try to keep these catalogs up to date, we recommend downloading the most recent versions from the original sources:

- [NEA Planetary Systems](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS) (**.csv** format)  
- [Exoplanet.eu catalog](https://exoplanet.eu/catalog/#downloads-section) (**.csv** format)  
- [PlanetS catalog](https://dace.unige.ch/exoplanets/) (**VOTable** format)

NEA data can also be accessed via the **TAP protocol** ([see how](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/TAP_NEA.md)). 

**Note:** When selecting the NEA option, the [Planetary Systems](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS&constraint=default_flag%20%3E0) catalog is used by default. Alternatively, the  
[Planetary Systems Composite Data](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars) catalog can also be selected ([see how](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/composite_NEA_data.md)).


### Optional parameters

#### [MY_DATA] | Include data for custom planets

This section allows you to manually include one or more planets that are **not present in the selected catalog**, or to highlight specific objects of interest.

| Parameter        | Possible values                  | Description |
|------------------|----------------------------------|-------------|
| m_p1             | Any ($\rm M_{\oplus}$)           | Mass of planet 1 |
| m_p1_err_up      | Any ($\rm M_{\oplus}$)           | Upper uncertainty on the mass of planet 1 |
| m_p1_err_down    | Any ($\rm M_{\oplus}$)           | Lower uncertainty on the mass of planet 1 |
| r_p1             | Any ($\rm R_{\oplus}$)           | Radius of planet 1 |
| r_p1_err_up      | Any ($\rm R_{\oplus}$)           | Upper uncertainty on the radius of planet 1 |
| r_p1_err_down    | Any ($\rm R_{\oplus}$)           | Lower uncertainty on the radius of planet 1 |
| c_p1<sup>1</sup> | Any color or value               | Color or value associated with planet 1 |
| name_p1          | Any string                       | Name of planet 1 (e.g. *TOI-244 b*) |
| dis_x_p1<sup>2</sup> | Any ($\rm M_{\oplus}$)     | Horizontal offset of the planet label (*X*-axis) |
| dis_y_p1<sup>2</sup> | Any ($\rm R_{\oplus}$)     | Vertical offset of the planet label (*Y*-axis) |
| ...              | ...                              | Additional planets can be added following the same naming pattern |

**<sup>1</sup>** <sub> If color_coding = none, provide a valid color name (e.g. blue). If color_coding = st_met, pl_insol, etc., provide the corresponding **numerical value** for the planet so it can be color-coded consistently with catalog planets. </sub> **<sup>2</sup>** <sub> If not specified, the planet name(s) will be displayed in the legend instead of directly on the plot.
</sub>


#### [MODELS] | Include theoretical models

In this section, we list all theoretical and empirical models implemented in *mr-plotter* and show how to include them in your plots. Some models are activated using a **single option**, while others require a **combination of parameters** (e.g. composition, temperature). Below, we illustrate both cases using the models from Zeng et al. (2016, 2019) as an example of single-option models, and Aguichine et al. (2021) as an example of multi-parameter models. **For all other models, detailed tables listing the available options, allowed values, and descriptions can be accessed through the corresponding hyperlinks.**

**[Zeng et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract)** and **[Zeng et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)**. Rocky planets, water worlds, and gas dwarfs | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-1-the-simplest-case-contextualizing-a-new-planetary-system)

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| models_zeng | zeng_2019_earth_like, zeng_2019_pure_rock, etc<sup>**1**</sup> | Models from Zeng et al. ([2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [2019](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)) |

<sup>**1**</sup> <sub> In [this table](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/zeng_2016_2019.md) we include all the **Possible values** corresponding to the Zeng et al. ([2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [2019](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)) models. </sub>

[**Aguichine et al. (2021)**](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract). Rocky planets with extensive atmospheres of steam and supercritical water | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-2-colourig-my-worlds-and-including-steam-water-atmospheres) 

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| x_core_aguich2021 | From 0.0 to 0.9 in steps of 0.1 | Core mass fraction |
| x_H2O_aguich2021 | From 0.1 to 1.0 in steps of 0.1 | Water mass fraction of the hydrosphere |
| Tirr_aguich2021 | From 400 to 1300 K in steps of 100 K | Equilibrium temperature of your planet |
| colors_aguich2021 | Any color | Colors of each model |

[**Seager et al. (2007)**](https://ui.adsabs.harvard.edu/abs/2007ApJ...669.1279S/abstract). 100% iron, 100% silicates, and 100% condensed water models | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/seager_2007.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models) <br />

[**Marcus et al. (2010)**](https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M/abstract). Maximum collisional stripping of planetary mantles | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/marcus_2010.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models) <br />

[**Lopez & Fortney et al. (2014)**](https://ui.adsabs.harvard.edu/abs/2014ApJ...792....1L/abstract). Rocky planets with H<sub>2</sub>/He atmospheres | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/lopez&fortney_2014.md) | [Example]() <br />

[**Otegi et al. (2020)**](https://ui.adsabs.harvard.edu/abs/2020A%26A...634A..43O/abstract). Empirical mass-radius relationships based on the PlanetS catalog | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/otegi_2020.md) |  [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-3-the-planets-catalog-empirical-relations-and-color-coding-based-on-homogeneous-transmission-and-emission-spectroscopy-metrics-tsm-and-esm) <br />

[**Turbet et al. (2020)**](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract). Rocky planets with atmospheres of steam and supercritical water | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/turbet_2020.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-2-colourig-my-worlds-and-including-steam-water-atmospheres) <br />

[**Haldemann et al. (2024)**](https://ui.adsabs.harvard.edu/abs/2024A%26A...681A..96H/abstract). Iron core + silicate mantle + volatile-rich envelope | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/haldemann_2024.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models) <br />

[**Parc et al. (2024)**](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract). Revised empirical mass-radius relationships based on the PlanetS catalog | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/parc_2024.md) |  [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-3-the-planets-catalog-empirical-relations-and-color-coding-based-on-homogeneous-transmission-and-emission-spectroscopy-metrics-tsm-and-esm) 

[**Isodensity curves**](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/iso_density.md). Mass-radius relations corresponding to a constant density | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/isodensity.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models)

[**Aguichine et al. (2025)**](https://ui.adsabs.harvard.edu/abs/2025ApJ...988..186A/abstract). Evolutionary mass–radius models for steam worlds with Earth-like rocky interiors | [Description and Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/aguichine_2025.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-3-evolutionary-models-with-interpolators-of-steam-worlds-and-gas-dwarfs)

[**Tang et al. (2025)**](https://ui.adsabs.harvard.edu/abs/2025ApJ...989...28T/abstract). Updated version of the Lopez & Fortney (2014) model, featuring a **more detailed mineralogy for the Earth-like core** and improved treatments of several physical approximations. The model also accounts for **atmospheric boil-off**, which sets an upper limit on the amount of gas a planet can retain. This model is provided as a **multidimensional grid with interpolation**, allowing any parameter value within the validity range to be explored (extrapolation is technically possible but **not recommended**) | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/tang_2025.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-3-evolutionary-models-with-interpolators-of-steam-worlds-and-gas-dwarfs) 


#### [OPTIONAL_CONFIG] | Optional configuration

*mr-plotter* is designed with a graphical setup that produces **paper-quality figures out of the box**. However, you may want to customize specific aspects of the plot, such as **X- and Y-axis limits**, **marker sizes**, **color maps**, or other stylistic options. All these customizations can be handled through [OPTIONAL_CONFIG]. A complete list of available parameters is provided in [**this table**](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/optional_config.md), many of which are illustrated in the [**Usage examples**](#usage-examples) section.

## Contributors and Change log

Mister plotter has been developed by [Amadeo Castro-González](https://github.com/castro-gzlz) with contributions from [Léna Parc](https://github.com/ParcLena), [Artem Aguichine](https://github.com/an0wen), [Jorge Lillo-Box](https://github.com/jlillo), and [Katharine Hesse](https://github.com/katharinehesse). Check out the [changelog](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/changelog.md) with the main updates!

## Contributors and change log

*mr-plotter* has been developed by [Amadeo Castro-González](https://github.com/castro-gzlz), with contributions from [Artem Aguichine](https://github.com/an0wen), [Katharine Hesse](https://github.com/katharinehesse), [Jorge Lillo-Box](https://github.com/jlillo), and [Léna Parc](https://github.com/ParcLena). A summary of the main updates can be found in the [changelog](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/changelog.md).

## Credits

If you use *mr-plotter*, please give credit to the [work](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract) where we present it: 

```
@ARTICLE{2023A&A...675A..52C,
       author = {{Castro-Gonz{\'a}lez}, A. and {Demangeon}, O.~D.~S. and {Lillo-Box}, J. and {Lovis}, C. and {Lavie}, B. and {Adibekyan}, V. and {Acu{\~n}a}, L. and {Deleuil}, M. and {Aguichine}, A. and {Zapatero Osorio}, M.~R. and {Tabernero}, H.~M. and {Davoult}, J. and {Alibert}, Y. and {Santos}, N. and {Sousa}, S.~G. and {Antoniadis-Karnavas}, A. and {Borsa}, F. and {Winn}, J.~N. and {Allende Prieto}, C. and {Figueira}, P. and {Jenkins}, J.~M. and {Sozzetti}, A. and {Damasso}, M. and {Silva}, A.~M. and {Astudillo-Defru}, N. and {Barros}, S.~C.~C. and {Bonfils}, X. and {Cristiani}, S. and {Di Marcantonio}, P. and {Gonz{\'a}lez Hern{\'a}ndez}, J.~I. and {Curto}, G. Lo and {Martins}, C.~J.~A.~P. and {Nunes}, N.~J. and {Palle}, E. and {Pepe}, F. and {Seager}, S. and {Su{\'a}rez Mascare{\~n}o}, A.},
        title = "{An unusually low-density super-Earth transiting the bright early-type M-dwarf GJ 1018 (TOI-244)}",
      journal = {\aap},
     keywords = {planets and satellites: individual: TOI-244 b, planets and satellites: detection, planets and satellites: composition, stars: individual: GJ 1018, techniques: radial velocities, techniques: photometric, Astrophysics - Earth and Planetary Astrophysics},
         year = 2023,
        month = jul,
       volume = {675},
          eid = {A52},
        pages = {A52},
          doi = {10.1051/0004-6361/202346550},
archivePrefix = {arXiv},
       eprint = {2305.04922},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2023A&A...675A..52C},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
and add the following sentence within the acknowledgements section:

> This work made use of \texttt{mr-plotter} (available in \url{https://github.com/castro-gzlz/mr-plotter})

Please also give credit to the catalog(s) used: Nasa Exoplanet Archive ([Akeson et al. 2013](https://ui.adsabs.harvard.edu/abs/2013PASP..125..989A/abstract)), Exoplanet.eu ([Schneider et al. 2011](https://ui.adsabs.harvard.edu/abs/2011A%26A...532A..79S/abstract)), and PlanetS ([Otegi et al. 2020](https://ui.adsabs.harvard.edu/abs/2020A%26A...634A..43O/abstract); [Parc et al. 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract)), as well as to the interior models: The ADS site of each work can be accessed by clicking on the hyperlinks of Section [[MODELS]](#models--include-theoretical-models).
