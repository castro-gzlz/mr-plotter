# **mr-plotter: Mass-Radius Diagrams Plotter**
**Mister plotter** (*mr-plotter*) is a **user-friendly** Python tool developed to create **paper-quality mass-radius diagrams** based on a **wide range of** [**state-of-the-art models**](#models--include-theoretical-models) **of planetary interiors and atmospheres**.

![mr-plotter_logo_v1-cropped](https://github.com/user-attachments/assets/46b08ef3-1d05-4020-9992-5cf7477ada28)

It can be used to **contextualize your favorite planets and infer their possible internal structures**. It can also be used to **search for correlations** at a population level thanks to its **color-coding option** based on any property collected in the [*NASA Exoplanet Archive*](https://exoplanetarchive.ipac.caltech.edu/), [*PlanetS*](https://dace.unige.ch/exoplanets/), and [*Exoplanet.eu*](http://www.exoplanet.eu/) catalogs. 

If your favorite model is not yet included in *mr-plotter*, you have any usage problems, or you came up with an improvement, don't hesitate to contact me at [acastro@cab.inta-csic.es](acastro@cab.inta-csic.es). Mister plotter is open to [contributors](https://github.com/castro-gzlz/mr-plotter?tab=readme-ov-file#contributors-and-change-log) :smiley:

For an **interactive** manipulation of mass-radius diagrams with **sliders** check out [MARDIGRAS](https://github.com/an0wen/MARDIGRAS)!


## Installation & Requirements

Just **clone or download** this folder on your computer. All the dependencies are widely used, so you probably already have them installed. However, if this is not the case, you can just enter the folder via the terminal and type
```
pip install -r requirements.txt
```
If you have any problems with the installation, you can drop an issue [here](https://github.com/castro-gzlz/mr-plotter/issues).

## Usage

#### Python through the terminal

You just need to create a configuration file *[my_config_file.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/my_config_file.ini)* inside the [*config*](https://github.com/castro-gzlz/mr-plotter/tree/main/config) folder and then type

```
python mr-plotter.py my_config_file.ini
```
The file *[my_config_file.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/my_config_file.ini)* should contain all the necessary information to make your plot, which will be saved into the *[output](https://github.com/castro-gzlz/mr-plotter/tree/main/output)* folder. In the [**Configuration file**](#configuration-file) section we describe **all the parameters** ([mandatory](#mandatory-parameters) and [optional](#optional-parameters)) that can be used in the configuration files.


#### Python through Jupyter Notebook

Since September 2024 (v1+), *mr-plotter* can also be used via Jupyter notebook (mr-plotter.ipynb). Similarly to the terminal version, you just need to select a configuration file (config_file) and run all cells.

## Is this your first time using *mr-plotter*?

If so, please don't be overwhelmed by the large number of parameters. In most cases, you will only use a few! To **get familiarized** with the main options and **have a first contact** with *mr-plotter*, we invite you to take a look at the [**Usage examples**](#usage-examples) section, which illustrates the operation of the package in **different key scenarios**. You can find **all the example configuration files** inside the [*config*](https://github.com/castro-gzlz/mr-plotter/tree/main/config) folder. Enjoy :smiley:.

## Usage examples

### Example 1: The simplest case. Contextualizing a new planetary system
In this example, we contextualize a new planet (TOI-244 b; [Castro-González et al. 2023](https://ui.adsabs.harvard.edu/abs/2023A%26A...675A..52C/abstract)) in the [NEA catalog](https://exoplanetarchive.ipac.caltech.edu/) and include several theoretical models for **rocky planets**, **water worlds**, and **gas dwarfs** from [Zeng et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract).
```
python mr-plotter.py example1_toi244.ini
```

We can also contextualize different planets in the same plot. In this example, we use a **faint appearance** to better see the planets HD 21520 b ([Nies et al. 2024](https://ui.adsabs.harvard.edu/abs/2024arXiv240609595N/abstract)), TOI-469 b&d ([Damasso et al. 2023](https://ui.adsabs.harvard.edu/abs/2023A%26A...679A..33D/abstract); [Egger et al. 2024](https://ui.adsabs.harvard.edu/abs/2024arXiv240618653E/abstract)), and LHS 1140 c ([Lillo-Box et al. 2020](https://ui.adsabs.harvard.edu/abs/2020A%26A...642A.121L/abstract); [Cardieux et al. 2024](https://ui.adsabs.harvard.edu/abs/2024ApJ...960L...3C/abstract)). In this case, we have used the [Exoplanet.eu](https://exoplanet.eu/home/) catalog and included the planet names in the legend to avoid excessively overloading the figure. 

```
python mr-plotter.py example1_misc.ini
```

![example1_joint](https://github.com/user-attachments/assets/2457c704-9e5d-47d5-9a02-33683583e0db)


### Example 2: [Colourig my worlds](https://www.youtube.com/watch?v=fKtwi3cNtEs) and including steam water atmospheres

We now **include a color code** according to the stellar host metallicity. We also include three models based on [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) equations. These models consider a steam water atmosphere over a rocky composition. As we can see, a small amount of steam water (0.3%-5% in mass) forming an extensive hydrosphere can explain very well the composition of the [emerging group of low-density super-Earths](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract). These models are valid up to a 5% water mass fraction (WMF). Above this value, you might want to use the models from [Aguichine et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract), which have a validity range between 10% and 100% core mass fractions (CMF) and WMF. In this example, we also include two models from [Aguichine et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract): 30% CMF & 10 WMF (400K), and 30% CMF & 20% WMF (400K). 

```
python mr-plotter.py example2_met.ini
```

We now run the same example by including a color code based on the received stellar insolation flux. We note that in both examples we customized the size of the planets through the *size_catalog_planets* keyword and the maximum and minimum values of the color map through the *color_min* and *color_max* keywords.

```
python mr-plotter.py example2_insol.ini
```

![example2_joint](https://github.com/user-attachments/assets/a2e09bee-5949-421b-bae0-79bc7ebbbf77)


Wait! Do you see what I'm seeing? **All low-density super-Earths are hosted by metal-poor stars and tend to receive relatively low insolation fluxes!** If you are interested in this result I invite you to look at Sect. 5.3 of [An unusually low-density super-Earth transiting the bright early-type M-dwarf GJ 1018 (TOI-244)](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract).


### Example 3: The *PlanetS catalog*, empirical relations, and color coding based on homogeneous Transmission and Emission Spectroscopy metrics (TSM and ESM)

In this example, we use the [*PlanetS*](https://dace.unige.ch/exoplanets/) catalog ([Otegi et al. 2020](https://ui.adsabs.harvard.edu/abs/2020A%26A...634A..43O/abstract); [Parc et al. 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract)). This catalog contains published planets characterized robustly and accurately (relative error in mass < 25% and relative error in radius < 8%). It collects many parameters from the [NEA](https://exoplanetarchive.ipac.caltech.edu/), stellar parameters from [*Gaia* DR3](https://ui.adsabs.harvard.edu/abs/2023A%26A...674A...1G/abstract), and also includes homogeneous calculations of $S_{\rm eff}$, $T_{\rm eq}$, TSM, ESM, etc. In this example, we plot the entire catalog color-coded according to the planetary TSM. We also show how we can include a new planetary system (TOI-5005; Castro-González et al. 2024) consistently colored with the catalog. In addition, we plot the **empirical relationships** for small, intermediate, and giant planets derived by [Parc et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract). You might have noticed that we have changed the color code! By default, *mr-plotter* uses *rainbow*, but any [matplotlib's color map](https://matplotlib.org/stable/users/explain/colors/colormaps.html) can be easily chosen. 

```
python mr-plotter.py example3_TSM.ini
```

Of course, we can do the same for the ESM! As in [Parc et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract), the transition between the small and intermediate planet populations corresponds to the composition line of 20% water at 650 K from [Luo et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024NatAs.tmp..205L/abstract), and the transition between the intermediate and giant planet population corresponds to the iso-mass line at 138 M<sub>⊕</sub>.

```
python mr-plotter.py example3_ESM.ini
```

![example3_joint](https://github.com/user-attachments/assets/75d18651-4b05-4552-a6ae-7c71c6f6429a)


### Example 4: Non-numerical color codings and dark plots | The TESS legacy

There are several parameters such as the discovery year, facility, or technique, that you might want to **separate by groups**. This is now possible to implement in *mr-plotter* (v1+). In this example, we first build the mass-radius diagram of small planets colored according to their discovery year. 

```
python mr-plotter.py example4_year.ini
```
It's amazing to see the exciting era we live in, right?! We can also make the same plot by differentiating between the three main space-based planet-hunting missions: *Kepler*, *K2*, and *TESS*.

```
python mr-plotter.py example4_facility.ini
```

This plot evidences the invaluable legacy that *TESS* is providing thanks to its incessant monitoring of the bright sky. This example also shows how to make dark poster-ready and presentation-ready diagrams for conferences!

![example4_joint](https://github.com/user-attachments/assets/b7cf7e8c-695d-4728-8e53-1aeb33fc1492)

In this example, we can also see how to contextualize a planet (in this case L 98-59 d; [Demangeon et al. 2021](https://ui.adsabs.harvard.edu/abs/2021A%26A...653A..41D/abstract)) with a new color not included in the color map (left panel), and a color following the non-numerical color code (right panel; L 98-59 d was discovered by TESS).


### Example 5: Two-column plots, isodensity curves and more interior models!

*mr-plotter* can also produce **paper-ready two-column plots**. In this example, we contextualize the dense super-Earth K2-229 b ([Santerne et al. 2018](https://ui.adsabs.harvard.edu/abs/2018NatAs...2..393S/abstract)) by including the maximum mantle collisional stripping model by [Marcus et al. (2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M/abstract), the BICEPS model ([Haldemann et al. 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...681A..96H/abstract)) for different pure-iron compositions (C0 and C1 compositions), and some isodensity curves. We also show how to implement the pioneer M-R relations for pure-rock and pure-water compositions from [Seager et al. (2007)](https://ui.adsabs.harvard.edu/abs/2007ApJ...669.1279S/abstract). The procedure to include any other model from the literature is very similar to that shown in this and previous examples. In Section [[MODELS]](#models--include-theoretical-models) you can find the complete set of models implemented in *mr-plotter*.

```
python mr-plotter.py example5.ini
```

![example5](https://github.com/user-attachments/assets/85a72cd7-36e5-448e-8cf0-4510f4d6d0ca)


## Configuration file

### Mandatory parameters

#### [CATALOG_DATA] | Include data from the  [*NASA Exoplanet Archive*](https://exoplanetarchive.ipac.caltech.edu/), [*Exoplanet.eu*](https://exoplanet.eu/home/), or [*PlanetS*](https://dace.unige.ch/exoplanets/) catalogs. 


| Parameter  | Possible values | Description |
| ------------- | ------------- | ------------- |
| catalog | NEA, Exoplanet.eu, or PlanetS | Exoplanet catalog to visualize |
| precision_mass | From 0 to 100 (%) | Minimum precision in mass |
| precision_radius | From 0 to 100 (%) | Minimum precision in radius |
| color_coding | none, st_met, pl_insol, st_teff, sy_kmag, etc<sup>**1,2**</sup> | Color coding of the plot |

**<sup>1</sup>** <sub> The full list of parameters that you can use to color your *mr-plots* can be found [here](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/color_codes.md). <br /> 
**<sup>2</sup>** If a non-numerical color code is chosen (e.g. disc_year, disc_facility, etc), the grups to display and their colors have to be defined (see how [here](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/non_numerical_config.md)).  </sub>

The package can access the catalog data **locally** from different folders inside [*catalog_data*](https://github.com/castro-gzlz/mr-plotter/tree/main/catalog_data). We try to maintain the catalogs updated, but we recommend downloading the most recent ones from: <br />

[NEA Planetary Systems](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS) (in **.csv** format)  <br /> 
[Exoplanet.eu catalog](https://exoplanet.eu/catalog/#downloads-section) (in **.csv** format)  <br />
[PlanetS catalog](https://dace.unige.ch/exoplanets/) (in **VOTable** format) <br />

The NEA data can be also accessed through a **TAP protocol** ([see how](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/TAP_NEA.md)). We note that when selecting the NEA option, the [Planetary Systems](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS&constraint=default_flag%20%3E0) catlog will be considered by default. However, it is also possible to use the [Planetary Systems Composite Data](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars) catalog ([see how](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/composite_NEA_data.md)). 

### Optional parameters 

#### [MY_DATA] | Include data of your planets

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| m_p1  | Any ($\rm M_{\oplus}$) | Mass of your planet 1 |
| m_p1_err_up | Any ($\rm M_{\oplus}$) | Upper uncertainty on the mass of your planet 1 |
| m_p1_err_down | Any ($\rm M_{\oplus}$) | Lower uncertainty on the mass of your planet 1 |
| r_p1  | Any ($\rm R_{\oplus}$) | Radius of your planet 1 |
| r_p1_err_up | Any ($\rm R_{\oplus}$) | Upper uncertainty on the radius of your planet 1 |
| r_p1_err_down | Any ($\rm R_{\oplus}$) | Lower uncertainty on the radius of your planet 1 |
| c_p1<sup>**1**</sup>   | Any color/value| Color of your planet 1 |
| name_p1| Any name | Name of your planet 1 (e.g. TOI-244 b) |
| dis_x_p1<sup>**2**</sup>  | Any ($\rm M_{\oplus}$)  | Location of a text box in terms of distance from the planet (*X*-axis) |
| dis_y_p1<sup>**2**</sup> | Any ($\rm R_{\oplus}$)  | Location of a text box in terms of distance from the planet (*Y*-axis) |
|....|....|....|

**<sup>1</sup>** <sub> If color_coding = **none**, type a color (e.g. **blue**). If color_coding = **st_met**, **pl_insol**,...etc, type the corresponding **value** for your planet so it can be **color-coded** as the rest of the catalog planets. <br /> **<sup>2</sup>** If not defined, the name of the planet(s) will be included in the legend of the plot. </sub>

#### [MODELS] | Include theoretical models

In this section, we list the complete set of models implemented in *mr-plotter*. Their inclusion into your *mr-plots* is really easy! You just need to select as many **Possible values** as models you want to visualize separated by commas, as in these examples: Example1, Example2, etc. In some cases, a model is simply defined by **one Option**, and in others it is defined by a combination of **a few Options**. In the following, we show an example of both kinds of operation: the models from  Zeng et al. 2016,2019 (single option) and Aguichine et al. 2021 (several options). For the remaining models, their corresponding tables with the **Options**, **Possible values**, and **Descriptions** can be accessed through the corresponding **hyperlinks**. 

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
| Tirr_aguich2021 | From 400 (K) to 1300 (K) in steps of 100 (K) | Equilibrium temperature of your planet |
| colors_aguich2021 | Any color | Colors of each model |

[**Seager et al. (2007)**](https://ui.adsabs.harvard.edu/abs/2007ApJ...669.1279S/abstract). 100% iron, 100% silicates, and 100% condensed water models | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/seager_2007.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models) <br />

[**Marcus et al. (2010)**](https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M/abstract). Maximum collisional stripping of planetary mantles | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/marcus_2010.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models) <br />

[**Lopez & Fortney et al. (2014)**](https://ui.adsabs.harvard.edu/abs/2014ApJ...792....1L/abstract). Rocky planets with H<sub>2</sub>/He atmospheres | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/lopez&fortney_2014.md) | [Example]() <br />

[**Dorn et al. (2015)**](). **TBD**. 

[**Otegi et al. (2020)**](https://ui.adsabs.harvard.edu/abs/2020A%26A...634A..43O/abstract). Empirical mass-radius relationships based on the PlanetS catalog | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/otegi_2020.md) |  [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-3-the-planets-catalog-empirical-relations-and-color-coding-based-on-homogeneous-transmission-and-emission-spectroscopy-metrics-tsm-and-esm) <br />

[**Turbet et al. (2020)**](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract). Rocky planets with atmospheres of steam and supercritical water | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/turbet_2020.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-2-colourig-my-worlds-and-including-steam-water-atmospheres) <br />

[**Haldemann et al. (2024)**](https://ui.adsabs.harvard.edu/abs/2024A%26A...681A..96H/abstract). Iron core + silicate mantle + volatile-rich envelope | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/haldemann_2024.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models) <br />

[**Luo et al. (2024)**](). **TBD**. 

[**Parc et al. (2024)**](https://ui.adsabs.harvard.edu/abs/2024A%26A...688A..59P/abstract). Revised empirical mass-radius relationships based on the PlanetS catalog | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/parc_2024.md) |  [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-3-the-planets-catalog-empirical-relations-and-color-coding-based-on-homogeneous-transmission-and-emission-spectroscopy-metrics-tsm-and-esm)  <br />

[**Isodensity curves**](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/iso_density.md). Mass-radius relations corresponding to a constant density | [Usage](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/isodensity.md) | [Example](https://github.com/castro-gzlz/mr-plotter/tree/main?tab=readme-ov-file#example-5-two-column-plots-isodensity-curves-and-more-interior-models)

#### [OPTIONAL_CONFIG] | Optional configuration

*mr-plotter* has been designed to have a default graphic configuration able to generate paper-quality plots. However, there are some particular aspects such as the **X- and Y-axis limits**, **size of the data points**, **color map**, **etc**, that you might want to modify at your ease. This is also possible with [OPTIONAL_CONFIG]! Check out **all the available options** in [**this table**](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/tables/optional_config.md) (most of them were used in the [**Usage examples**](#usage-examples) section).

## Contributors and Change log

Mister plotter has been developed by [Amadeo Castro-González](https://github.com/castro-gzlz) with contributions from [Léna Parc](https://github.com/ParcLena), [Artem Aguichine](https://github.com/an0wen), [Jorge Lillo-Box](https://github.com/jlillo), and [Katharine Hesse](https://github.com/katharinehesse). Check out the [changelog](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/changelog.md) with the major updates!

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
