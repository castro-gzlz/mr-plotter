# **mr-plotter**
**Mister plotter** (*mr-plotter*) is an **user-friendly** Python tool which creates **paper-ready mass-radius diagrams** with your favourite theoretical models. It also includes the ability to **color-code diagrams** based on any published stellar or planetary property collected in the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/).

![logo_mr-plotter](https://github.com/castro-gzlz/mr-plotter/assets/132309889/6ee7dbb3-4d5c-4f8c-b4fe-9d69131f66fd)

## Installation & Requirements

Just **clone or download** this folder into your computer. All the dependencies are very well-known and probably you already have them installed. However, if this is not the case, you can just enter the folder via terminal and type

```
pip install -r requirements.txt
```
If you have any problem with the installation you can drop me an issue [here](https://github.com/castro-gzlz/mr-plotter/issues) :smiley:.

## Usage

To run *mr-plotter* you just need to create a **.ini** file and then type

```
python mr-plotter.py my_config_file.ini
```
The file *my_config_file.ini* should contain all the necessary information to make your plot, which will be **saved into the output** folder both in **.pdf** and **.png** formats. **In the [config.ini file] you can find a detailed explanation of each option than can be used**. If this is your first time using *mr-plotter*, I invite you to follow along with the tutorial and see some examples that I have prepared to illustrate the operation of the package in diferent scenarios (some of them might be of interest for you!). 
## Usage examples

### Example 1: The simplest case. Contextualizing a new planet
In this example we contextualize and hihglight the location of a new planet ([TOI-244 b](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract)) in the mass-radius diagram of known planets, and include the theoretical models for **rocky planets** and **water wolds** from [Zeng et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract).
```
python mr-plotter.py example1.ini
```
![example1](https://github.com/castro-gzlz/mr-plotter/assets/132309889/057ee788-9216-4fc3-b4d4-72603d4bf2f0)


### Example 2: [Colourig my worlds](https://www.youtube.com/watch?v=fKtwi3cNtEs) and including steam water models

In this example we include three models computed from [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) equations, which consider a steam water atmosphere over a canonical rocky composition. As we can see, a small amount of steam water (0.3%-5% in mass) forming an extense hydrosphere would be enough to explain the composition of the [emerging group of low-density super-Earths](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract). Besides, **we include a color code** according to the stellar host metallicity. Wait! do you see what I'm seeing? **All low-density super-Earths are hosted by metal-poor stars!** For more insights on this take a look at our paper [An unusually low-density super-Earth transiting the bright early-type M-dwarf GJ 1018 (TOI-244)](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract).


```
python mr-plotter.py example2.ini
```
![example2](https://github.com/castro-gzlz/mr-plotter/assets/132309889/5707be78-bc83-4a27-a2c5-3ef810ec962b)


### Example 3: Custom color maps

In this example we plot the iconic system [LHS 1140](https://ui.adsabs.harvard.edu/abs/2020A%26A...642A.121L/abstract). The color code now indicates the received **insolation flux**, spanning from 1 to 2 Earth fluxes, which roughly corresponds to fluxes received by planets in the habitable zone (HZ) of their stars. LHS 1140 b stands out as one of the only well-characterized HZ planets in the rocky domain. In this plot we have used the *summer* color map, but **any matplotlib color map can be easily selected**. 

```
python mr-plotter.py example3.ini
```
![example3](https://github.com/castro-gzlz/mr-plotter/assets/132309889/81a9729a-f1d6-4ca4-8fc1-1956ec3011a9)


### Example 4: Exploring other theoretical models

Althogh in the [original paper](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract) where *mr-plotter* was presented we have only used the Zeng et al. ([2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [2019](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)) and [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) models, **we have included additional models from the literature**. For example, if you have a puffy sub-Neptune planet, you might want to consider the H/He atmosphere models by [Lopez & Fortney (2014)](https://ui.adsabs.harvard.edu/abs/2014ApJ...792....1L/abstract). You might also want to discuss the possibility that your (highly irradiated) planet has a water-rich composition but perhaps it is less dense than the density corresponding to a 5% water mass fraction (WMF), where [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) models are no longer valid. In this case you might want to use [Aguichine et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract) mass-radius relationships, which are valid for any WMF. In this example, we use the [K2-3 system](https://ui.adsabs.harvard.edu/abs/2018A%26A...615A..69D/abstract) to illustrate how these two set of models can be used through *mr-plotter*. 

```
python mr-plotter.py example4.ini
```
![example4](https://github.com/castro-gzlz/mr-plotter/assets/132309889/e60f55ca-98b6-453e-9925-d16a25051407)

### Example 5: More models and isodensity curves

In this example we include the model by [Marcus et al. (2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...712L..73M/abstract) corresponding to the maximum density curve for a planet subjected to mantle stripping. We highlight the earth-sized mercurian-density planet K2-229 b, with the size of the Earth and density of Mercury, it is located just above that curve. Besides, we show how to include isodensity curves. 

```
python mr-plotter.py example5.ini
```

![example5](https://github.com/castro-gzlz/mr-plotter/assets/132309889/1643a8fe-c6b6-49a2-9e29-29768bc26d55)

## Inclusion of additional models, issues, improvements, and suggestions

If your favourite model is not yet included in *mr-plotter*, or you have any issue when using the package, or you think it can be improved in any way, don't hesitate to contact me at [acastro@cab.inta-csic.es](acastro@cab.inta-csic.es).


## Credits

**If you use mr-plotter, please give credit to the following [paper](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract)**: 

```
@ARTICLE{2023arXiv230504922C,
       author = {{Castro-Gonz{\'a}lez}, A. and {Demangeon}, O.~D.~S. and {Lillo-Box}, J. and {Lovis}, C. and {Lavie}, B. and {Adibekyan}, V. and {Acu{\~n}a}, L. and {Deleuil}, M. and {Aguichine}, A. and {Zapatero Osorio}, M.~R. and {Tabernero}, H.~M. and {Davoult}, J. and {Alibert}, Y. and {Santos}, N. and {Sousa}, S.~G. and {Antoniadis-Karnavas}, A. and {Borsa}, F. and {Winn}, J.~N. and {Allende Prieto}, C. and {Figueira}, P. and {Jenkins}, J.~M. and {Sozzetti}, A. and {Damasso}, M. and {Silva}, A.~M. and {Astudillo-Defru}, N. and {Barros}, S.~C.~C. and {Bonfils}, X. and {Cristiani}, S. and {Di Marcantonio}, P. and {Gonz{\'a}lez Hern{\'a}ndez}, J.~I. and {Lo Curto}, G. and {Martins}, C.~J.~A.~P. and {Nunes}, N.~J. and {Palle}, E. and {Pepe}, F. and {Seager}, S. and {Su{\'a}rez Mascare{\~n}o}, A.},
        title = "{An unusually low-density super-Earth transiting the bright early-type M-dwarf GJ 1018 (TOI-244)}",
      journal = {arXiv e-prints},
     keywords = {Astrophysics - Earth and Planetary Astrophysics},
         year = 2023,
        month = may,
          eid = {arXiv:2305.04922},
        pages = {arXiv:2305.04922},
          doi = {10.48550/arXiv.2305.04922},
archivePrefix = {arXiv},
       eprint = {2305.04922},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
**Please give also credit to the models used in your research:**
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













