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

### Example 1: The easiest case. Contextualizing a new planet
In this example we contextualize and hihglight the location of a new planet ([TOI-244 b](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract)) in the mass-radius diagram of known planets, and include the theoretical models for rocky planets of [Zeng et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract), which consider different proportions of iron and silicates in their interiors.

```
python mr-plotter.py example1.ini
```
![example1](https://github.com/castro-gzlz/mr-plotter/assets/132309889/e557494f-9af6-4ec5-b105-0f42bb9f69cc)

### Example 2: [Colourig my worlds](https://www.youtube.com/watch?v=fKtwi3cNtEs) and including steam water models

In this example we include three models computed from [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) equations which consider a steam water atmosphere over a canonical rocky composition. As we can see, a small amount of steam water (0.3%-5% in mass) forming an extense hydrosphere would be enough to explain the composition of the [emerging group of low-density super-Earths](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract). Besides, **we include a color code** according to the stellar host metallicity. Wait! do you see what I'm seeing? **All low-density super-Earths are hosted by metal-poor stars!** For more insights on this take a look at our paper [An unusually low-density super-Earth transiting the bright early-type M-dwarf GJ 1018 (TOI-244)](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract).


```
python mr-plotter.py example2.ini
```
![example2](https://github.com/castro-gzlz/mr-plotter/assets/132309889/2d4ba7af-e095-4e66-995e-5cdce211955f)

### Example 3: Custom color maps

In this example we plot the iconic system [LHS 1140](https://ui.adsabs.harvard.edu/abs/2020A%26A...642A.121L/abstract). The color code indicates the received insolation flux, spanning from 1 to 2 Earth fluxes, which roughly corresponds to fluxes received by planets in the habitable zone (HZ) of their stars. LHS 1140 b stands out as one of the only characterized HZ planets in the rocky domain. In this plot we have used the *summer* color map, but **any matplotlib color map can be easyly selected accordig to your preferences**. 

```
python mr-plotter.py example3.ini
```
![example3](https://github.com/castro-gzlz/mr-plotter/assets/132309889/83ca68f5-ae8c-4813-9e43-a138f98fcddc)

### Example 4: Exploring other theoretical models

Althogh in the [original paper](https://ui.adsabs.harvard.edu/abs/2023arXiv230504922C/abstract) where *mr-plotter* was presented we have only used the Zeng et al. ([2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z/abstract), [2019](https://ui.adsabs.harvard.edu/abs/2019PNAS..116.9723Z/abstract)) and [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) models, **we have included additional models from the literature**. For example, if you have a puffy sub-Neptune planet, you might want to consider the H/H2 atmosphere models by [Lopez & Fortney (2014)](https://ui.adsabs.harvard.edu/abs/2014ApJ...792....1L/abstract). You might also want to discuss the possibility that your (highly irradiated) planet has a water-rich composition but is less dense than the density corresponding to the 5% water mass fraction, where [Turbet et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A..41T/abstract) models are no longer valid. In this case you might want to use [Aguichine et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021ApJ...914...84A/abstract) mass-radius relationships. In this example, we use the [K2-3 system](https://ui.adsabs.harvard.edu/abs/2018A%26A...615A..69D/abstract) to illustrate how these two set of models can be used through *mr-plotter*. 

```
python mr-plotter.py example4.ini
```
![example4](https://github.com/castro-gzlz/mr-plotter/assets/132309889/d263e412-0196-4f26-b941-c32701c1efd4)




