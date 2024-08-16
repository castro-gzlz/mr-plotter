# **mr-plotter: Mass-Radius Diagrams Plotter**
**Mister plotter** (*mr-plotter*) is a **user-friendly** Python tool that creates **paper-ready mass-radius diagrams** with a wide range of theoretical models. It also includes the ability to **color-code diagrams** based on any published stellar or planetary property collected in the [*NASA Exoplanet Archive*](https://exoplanetarchive.ipac.caltech.edu/).


![logo_mr-plotter](https://github.com/castro-gzlz/mr-plotter/assets/132309889/6ee7dbb3-4d5c-4f8c-b4fe-9d69131f66fd)

## Installation & Requirements

Just **clone or download** this folder on your computer. All the dependencies are widely used, so you probably already have them installed. However, if this is not the case, you can just enter the folder via the terminal and type
```
pip install -r requirements.txt
```
If you have any problems with the installation, you can drop me an issue [here](https://github.com/castro-gzlz/mr-plotter/issues).

## Usage

You just need to create a configuration file *[my_config_file.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/my_config_file.ini)* inside the [*config*](https://github.com/castro-gzlz/mr-plotter/tree/main/config) folder and then type

```
python mr-plotter.py my_config_file.ini
```
The file *[my_config_file.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/my_config_file.ini)* should contain all the necessary information to make your plot, which will be saved into the *[output](https://github.com/castro-gzlz/mr-plotter/tree/main/output)* folder. In the [**Configuration file**](#configuration-file) section we describe **all the parameters** ([mandatory](#mandatory-parameters) and [optional](#optional-parameters)) that can be used in the configuration files.

### Is this your first time using *mr-plotter*?

If so, please don't be overwhelmed by the large number of parameters. In most cases you will only use a few! To **get familiarized** with the main parameters and **have a first contact** with *mr-plotter*, we invite you to take a look at the [**Usage examples**](#usage-examples) section, which illustrates the operation of the package in **diferent key scenarios** through didactic examples. You can find **all the example configuration files** inside the [*config*](https://github.com/castro-gzlz/mr-plotter/tree/main/config) folder. Enjoy :smiley:.

## Configuration file

### Mandatory parameters

#### Section [NEA_DATA] | Include data from the [*Nasa Exoplanet Archive (NEA)*](https://exoplanetarchive.ipac.caltech.edu/index.html)

| Parameter  | Possible values | Description |
| ------------- | ------------- | ------------- |
| web_or_local  | web or local  | Download the data from the [*Nasa Exoplanet Archive*](https://exoplanetarchive.ipac.caltech.edu/index.html) (**web**) or pick it up from the *[NEA_data](https://github.com/castro-gzlz/mr-plotter/tree/main/NEA_data)* folder (**local**)**<sup>1</sup>** |
| ps_or_composite | ps or composite  | Indicates which table to use: *[Planetary Systems](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS&constraint=default_flag%20%3E0)* (**ps**) or *[Planetary Systems Composite Data](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars)* (**composite**)**<sup>2</sup>** |
| precision_mass | From 0 to 100 (%) | Minimum precision in mass to plot NEA planets |
| precision_radius | From 0 to 100 (%) | Minimum precision in radius to plot NEA planets |
| color_coding | none, st_met, pl_insol, st_teff, sy_kmag, etc<sup>**3**</sup> | Color coding of the plot |

**<sup>1</sup>** If **web**, it will connect to the NEA through a TAP protocol, which might last a bit (i.e., a couple of minutes). If **local**, you should have a comma-separated table downloaded from the NEA inside the *[NEA_data](https://github.com/castro-gzlz/mr-plotter/tree/main/NEA_data)* folder. Please don't change the default name of the downloaded tables. If you have several tables, *mr-plotter* wil automatically select the most recently downloaded. <br /> **<sup>2</sup>** If you want to use the **composite** data in your research, please read [this](https://exoplanetarchive.ipac.caltech.edu/docs/pscp_about.html) first.  <br /> 
**<sup>3</sup>** All possible values: **none** (None),  **disc_year** (Discovery year), **pl_orbper** (Orbital period in days), **pl_orbsmax** (Semi-major axis  in AU), **pl_orbeccen** (Eccentricity), **pl_insol** (Insolation Flux in $\rm S_{\oplus}$), **pl_eqt** (Eq. temperature  in K), **st_teff** (Stellar effective temperature in K), **st_rad** (Stellar radius in $\rm R_{\odot}$), **st_mass** (Stellar mass in $\rm M_{\odot}$), **st_met** (Stellar metallicity in dex), **st_logg** (Stellar surface gravity in dex), **sy_dist** (Distance in pc), **sy_vmag** ($V$ magnitude), **sy_kmag** ($K_{\rm s}$ magnitude), **sy_gaiamag** ($Gaia$ magnitude).

### Optional parameters 

#### Section [MY_DATA] | Include data of your planets

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| m_p1  | Any ($\rm M_{\oplus}$) | Mass of your planet 1 |
| m_p1_err_up | Any ($\rm M_{\oplus}$) | Upper uncertainty on the mass of your planet 1 |
| m_p1_err_down | Any ($\rm M_{\oplus}$) | Lower uncertainty on the mass of your planet 1 |
| r_p1  | Any ($\rm R_{\oplus}$) | Radius of your planet 1 |
| r_p1_err_up | Any ($\rm R_{\oplus}$) | Upper uncertainty on the radius of your planet 1 |
| r_p1_err_down | Any ($\rm R_{\oplus}$) | Lower uncertainty on the radius of your planet 1 |
| c_p1 | Any color or any number<sup>**1**</sup>  | Color for your planet 1 |
| name_p1| Any name (e.g. TOI-244 b) | Name of your planet 1 to be plotted inside a box next to the planet location<sup>**2**</sup>  |
| dis_x_p1 | Any ($\rm M_{\oplus}$)  | Location of the text box in terms of the distance from the planet (*X*-axis)<sup>**2**</sup>  |
| dis_y_p1| Any ($\rm R_{\oplus}$)  | Location of the text box in terms of the distance from the planet (*Y*-axis)<sup>**2**</sup>  |
|....|....|....|


**<sup>1</sup>** If color_coding = **none**, type a color (e.g. **blue**). If color_coding = **st_met**, **pl_insol**,...etc, just type the corresponding **value** for your planet so it can be **color-coded** as the rest of the NEA planets. <br /> **<sup>2</sup>** These options should be **only specified** if you want to include **text boxes** next to your planets with their names.

#### Section [MODELS] | Include theoretical models

##### Zeng et al. (2016, 2019)

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| models_zeng | zeng_2019_earth_like, zeng_2019_pure_rock, etc<sup>**1**</sup> | Models from Zeng et al. ([2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [2019](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)) |

<sup>**1**</sup> In [this table](https://github.com/castro-gzlz/mr-plotter/blob/main/misc/zeng_2016_2019_table.md) we include all the Zeng et al. ([2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [2019](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)) models for **rocky planets**, **water worlds**, and **gas dwarfs**. 

##### Lopez & Fortney et al. (2014) 

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| age_lf2014 | 100Myr, 1Gyr, 10Gyr | Age of the system |
| opacity_lf2014 | solar or enhanced | Opacity of the star |
| Seff_lf2014 | 0.1, 10, 1000  ($\rm S_{\oplus}$) | Insolation received by the planet|
| H_He |0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, and 20 (%) | H/He mass fraction of the planet|
| colors_lf2014 | Any color | Colors of each curve |

**Note:** To plot several [Lopez & Fortney et al. (2014)](https://ui.adsabs.harvard.edu/abs/2014ApJ...792....1L/abstract) models you can include as many values as you want, separated by commas, similar to [example4.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/example4.ini). 

##### Turbet et al. (2020)

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| M_turb2020 | Any ($\rm M_{\oplus}$) | Mass of your planet |
| R_turb2020 | Any ($\rm M_{\oplus}$) | Radius of your planet |
| Seff_turb2020 | > 1.1 ($\rm S_{\oplus}$) | Insolation flux received by your planet |
| WMFs_turb2020 | From 0 to 0.05 | Water mass fractions (WMFs) of steam water |
| Core_turb2020 | earth, rock, or iron | Internal core composition over which the steam water resides |
| colors_turb2020 | Any color | Colors of each model |

**Note:** To plot several [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) models you can include as many values as you want, separated by commas, similar to [example2.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/example2.ini). 

##### Aguichine et al. (2021)

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| x_core_aguich2021 | From 0.0 to 0.9 in steps of 0.1 | Core mass fraction |
| x_H2O_aguich2021 | From 0.1 to 1.0 in steps of 0.1 | Water mass fraction of the hydrosphere |
| Tirr_aguich2021 | From 400 (K) to 1300 (K) in steps of 100 (K) | Equilibrium temperature of your planet |
| colors_aguich2021 | Any color | Colors of each model |

**Note:** To plot several [Aguichine et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract) models you can include as many values as you want, separated by commas, similar to [example4.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/example4.ini). 

##### Marcus et al. (2010)

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| models_marcus |  marcus_2010_maximum_collision_stripping | Maximum collision stripping model from [Marcus et al. (2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M/abstract) |


##### Isodensity curves

| Option | Possible values | Description |
| ------------- | ------------- | ------------- |
| density | Any ($\rm g \cdot cm^{-3}$) | Density |
| colors_density | Any color | Colors of each curve |

**Note:** To plot several curves you can include as many values as you want, separated by commas, similar to [example5.ini](https://github.com/castro-gzlz/mr-plotter/blob/main/config/example5.ini). 

#### Section [OPTIONAL_CONFIG] | Optional configuration

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


## Usage examples

### Example 1: The simplest case. Contextualizing a new planet
In this example, we contextualize a new planet ([TOI-244 b](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract)) in the mass-radius diagram of known planets, and include several theoretical models for **rocky planets**, **water worlds**, and **gas dwarfs** from [Zeng et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract).
```
python mr-plotter.py example1.ini
```
![example1](https://github.com/castro-gzlz/mr-plotter/assets/132309889/e57421f3-df1f-49d2-b9b6-4e344cc86eb1)


### Example 2: [Colourig my worlds](https://www.youtube.com/watch?v=fKtwi3cNtEs) and including steam water models

In this example, we include three models computed from [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) equations, which consider a steam water atmosphere over a canonical rocky composition. As we can see, a small amount of steam water (0.3%-5% in mass) forming an extense hydrosphere would be enough to explain the composition of the [emerging group of low-density super-Earths](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract). Besides, **we include a color code** according to the stellar host metallicity. Wait! Do you see what I'm seeing? **All low-density super-Earths are hosted by metal-poor stars!** For more insights on this, take a look at our paper [An unusually low-density super-Earth transiting the bright early-type M-dwarf GJ 1018 (TOI-244)](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract).


```
python mr-plotter.py example2.ini
```

![example2](https://github.com/castro-gzlz/mr-plotter/assets/132309889/f3fc554d-83e6-4c97-a137-58000d758a55)


### Example 3: Custom color maps

In this example, we plot the iconic system [LHS 1140](https://ui.adsabs.harvard.edu/abs/2020A%26A...642A.121L/abstract). The color code now indicates the received **insolation flux**, spanning from 1 to 2 Earth fluxes, which roughly correspond to fluxes received by planets in the habitable zone (HZ) of their stars. LHS 1140 b stands out as one of the only well-characterized HZ planets in the rocky domain. In this plot we have used the *summer* color map, but **any matplotlib color map can be easily selected**. 

```
python mr-plotter.py example3.ini
```
![example3](https://github.com/castro-gzlz/mr-plotter/assets/132309889/9b407bfa-8c66-4c50-84ec-8e8a8e2eb99d)


### Example 4: Exploring other theoretical models

Althogh in the [original paper](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract) where *mr-plotter* was presented we have only used the Zeng et al. ([2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [2019](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)) and [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) models, **we have included additional models from the literature**. For example, if you have a puffy sub-Neptune planet, you might want to consider the H/He atmosphere models by [Lopez & Fortney (2014)](https://ui.adsabs.harvard.edu/abs/2014ApJ...792....1L/abstract). You might also want to discuss the possibility that your (highly irradiated) planet has a water-rich composition, but perhaps it is less dense than the density corresponding to a 5% water mass fraction (WMF), where [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) models are no longer valid. In this case, you might want to use [Aguichine et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract) mass-radius relationships, which are valid for any WMF. In this example, we use the [K2-3](https://ui.adsabs.harvard.edu/abs/2018A%26A...615A..69D/abstract) system to illustrate how these two sets of models can be used through *mr-plotter*. 

```
python mr-plotter.py example4.ini
```
![example4](https://github.com/castro-gzlz/mr-plotter/assets/132309889/7529aa53-40c0-4977-8a8d-fc12b3a5984a)


### Example 5: More models, isodensity curves, and two-column plots

In this example, we include the model by [Marcus et al. (2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M/abstract) corresponding to the **maximum density curve for a planet subjected to mantle stripping**. We highlight the earth-sized, mercurian-density planet [K2-229 b](https://ui.adsabs.harvard.edu/abs/2018NatAs...2..393S/abstract), which having the size of the Earth and density of Mercury, is located just above that curve. Besides, we illustrate **how to include isodensity curves** as well as **how to prepare paper-ready plots in two-column format**. 

```
python mr-plotter.py example5.ini
```
![example5](https://github.com/castro-gzlz/mr-plotter/assets/132309889/7c07326e-ea36-4084-9b2d-5c4cb99f4b2b)


## Inclusion of additional models, issues, improvements, and suggestions

If your favorite model is not yet included in *mr-plotter*, you have any issues when using the package, or you think it can be improved in any way, don't hesitate to contact me at [acastro@cab.inta-csic.es](acastro@cab.inta-csic.es).

## Contributors

[Amadeo Castro-González](https://github.com/castro-gzlz), [Jorge Lillo-Box](https://github.com/jlillo), [Artem Aguichine](https://github.com/an0wen), [Léna Parc](https://github.com/ParcLena), and [Katharine Hesse](https://github.com/katharinehesse).


## Credits

**If you use *mr-plotter*, please give credit to the following [paper](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract)**: 

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
**and add the following sentence within the acknowledgements section**:
> This work made use of \texttt{mr-plotter} (https://github.com/castro-gzlz/mr-plotter), which has been developed with financial support from the Spanish Ministry of Science through MCIN/AEI/10.13039/501100011033 grant PID2019-107061GB-C61.

## Credits to the models used

#### Marcus et al. (2010)

```
@ARTICLE{2010ApJ...712L..73M,
       author = {{Marcus}, Robert A. and {Sasselov}, Dimitar and {Hernquist}, Lars and {Stewart}, Sarah T.},
        title = "{Minimum Radii of Super-Earths: Constraints from Giant Impacts}",
      journal = {\apjl},
     keywords = {planetary systems, planets and satellites: formation, Astrophysics - Earth and Planetary Astrophysics},
         year = 2010,
        month = mar,
       volume = {712},
       number = {1},
        pages = {L73-L76},
          doi = {10.1088/2041-8205/712/1/L73},
archivePrefix = {arXiv},
       eprint = {1003.0451},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

#### Lopez & Fortney et al. (2014)

```
@ARTICLE{2014ApJ...792....1L,
       author = {{Lopez}, Eric D. and {Fortney}, Jonathan J.},
        title = "{Understanding the Mass-Radius Relation for Sub-neptunes: Radius as a Proxy for Composition}",
      journal = {\apj},
     keywords = {planets and satellites: composition, planets and satellites: formation, planets and satellites: interiors, planets and satellites: physical evolution, Astrophysics - Earth and Planetary Astrophysics},
         year = 2014,
        month = sep,
       volume = {792},
       number = {1},
          eid = {1},
        pages = {1},
          doi = {10.1088/0004-637X/792/1/1},
archivePrefix = {arXiv},
       eprint = {1311.0329},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2014ApJ...792....1L},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

#### Zeng et al. (2016)

```
@ARTICLE{2016ApJ...819..127Z,
       author = {{Zeng}, Li and {Sasselov}, Dimitar D. and {Jacobsen}, Stein B.},
        title = "{Mass-Radius Relation for Rocky Planets Based on PREM}",
      journal = {\apj},
     keywords = {planets and satellites: composition, planets and satellites: general, planets and satellites: interiors, Astrophysics - Earth and Planetary Astrophysics},
         year = 2016,
        month = mar,
       volume = {819},
       number = {2},
          eid = {127},
        pages = {127},
          doi = {10.3847/0004-637X/819/2/127},
archivePrefix = {arXiv},
       eprint = {1512.08827},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
#### Zeng et al. (2019)

```
@ARTICLE{2019PNAS..116.9723Z,
       author = {{Zeng}, Li and {Jacobsen}, Stein B. and {Sasselov}, Dimitar D. and {Petaev}, Michail I. and {Vanderburg}, Andrew and {Lopez-Morales}, Mercedes and {Perez-Mercader}, Juan and {Mattsson}, Thomas R. and {Li}, Gongjie and {Heising}, Matthew Z. and {Bonomo}, Aldo S. and {Damasso}, Mario and {Berger}, Travis A. and {Cao}, Hao and {Levi}, Amit and {Wordsworth}, Robin D.},
        title = "{Growth model interpretation of planet size distribution}",
      journal = {Proceedings of the National Academy of Science},
     keywords = {Astrophysics - Earth and Planetary Astrophysics, Physics - Geophysics},
         year = 2019,
        month = may,
       volume = {116},
       number = {20},
        pages = {9723-9728},
          doi = {10.1073/pnas.1812905116},
archivePrefix = {arXiv},
       eprint = {1906.04253},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

#### Turbet et al. (2020)

```
@ARTICLE{2020A&A...638A..41T,
       author = {{Turbet}, Martin and {Bolmont}, Emeline and {Ehrenreich}, David and {Gratier}, Pierre and {Leconte}, J{\'e}r{\'e}my and {Selsis}, Franck and {Hara}, Nathan and {Lovis}, Christophe},
        title = "{Revised mass-radius relationships for water-rich rocky planets more irradiated than the runaway greenhouse limit}",
      journal = {\aap},
     keywords = {planets and satellites: terrestrial planets, planets and satellites: composition, planets and satellites: atmospheres, planets and satellites: individual: TRAPPIST-1, planets and satellites: interiors, methods: numerical, Astrophysics - Earth and Planetary Astrophysics, Physics - Atmospheric and Oceanic Physics, Physics - Geophysics},
         year = 2020,
        month = jun,
       volume = {638},
          eid = {A41},
        pages = {A41},
          doi = {10.1051/0004-6361/201937151},
archivePrefix = {arXiv},
       eprint = {1911.08878},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2020A&A...638A..41T},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

#### Aguichine et al. (2021)

```
@ARTICLE{2021ApJ...914...84A,
       author = {{Aguichine}, Artyom and {Mousis}, Olivier and {Deleuil}, Magali and {Marcq}, Emmanuel},
        title = "{Mass-Radius Relationships for Irradiated Ocean Planets}",
      journal = {\apj},
     keywords = {Exoplanets, Hydrosphere, Planetary interior, Planetary theory, Exoplanet astronomy, Exoplanet structure, Computational methods, 498, 770, 1248, 1258, 486, 495, 1965, Astrophysics - Earth and Planetary Astrophysics},
         year = 2021,
        month = jun,
       volume = {914},
       number = {2},
          eid = {84},
        pages = {84},
          doi = {10.3847/1538-4357/abfa99},
archivePrefix = {arXiv},
       eprint = {2105.01102},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```



