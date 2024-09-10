#!/usr/bin/env python
# coding: utf-8

# In[ ]:


############################
#@|++++++mr-plotter++++++#@|
############################


# In[ ]:


import os
import pyvo
import json
import argparse
import numpy as np
import pandas as pd
from scipy import interpolate
from astropy.constants import G
import matplotlib.pyplot as plt
import astropy.constants as const
from astropy.io.votable import parse
from configparser import ConfigParser


# In[ ]:


#@|+++++++++++++++++We load the dictionaries+++++++++++++++++++++++++
zeng_models_colors = json.load(open('misc/dicts/zeng_models_colors.txt'))
zeng_models_labels = json.load(open('misc/dicts/zeng_models_labels.txt'))
color_coding_labels = json.load(open('misc/dicts/color_coding_labels.txt'))


# In[ ]:


#@|++++Uncomment this for the mr-plotter.py version+++++++
parser = argparse.ArgumentParser()
parser.add_argument('config_file')
args = parser.parse_args()
config_file = args.config_file


# In[ ]:


#@|++++Uncomment this for the mr.plotter.ipynb version+++++
#config_file = 'example5.ini'
#@|++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# In[ ]:


path_models = 'theoretical_models/'


# In[ ]:


#|Turbet et al. (2020) theoretical M-R models
def turbet2020_MR():
    global R_pl_turb, M_pl_turb, m_pure_iron, m_earth_like, m_pure_rock, r_pure_iron, r_earth_like, r_pure_rock 

    #@|M-R relationships of the core of the planet based on Zeng et al. (2019)
    #@|Earth-like, pure iron, and pure rock 
    pure_iron_df = pd.read_csv('theoretical_models/zeng_2019_pure_iron', sep = "\t", header = None)
    earth_like_df = pd.read_csv('theoretical_models/zeng_2019_earth_like', sep = "\t", header = None)
    pure_rock_df = pd.read_csv('theoretical_models/zeng_2019_pure_rock', sep = "\t", header = None)

    m_pure_iron, r_pure_iron = pure_iron_df[0].values,  pure_iron_df[1].values
    m_earth_like, r_earth_like = earth_like_df[0].values,  earth_like_df[1].values
    m_pure_rock, r_pure_rock = pure_rock_df[0].values,  pure_rock_df[1].values

    Cores_db = np.array(['earth', 'rock', 'iron'])                          #@|Cores database
    R_db = np.array([r_earth_like, r_pure_rock, r_pure_iron], dtype=object) #@|Corresponding radius database
    M_db = np.array([m_earth_like, m_pure_rock, m_pure_iron], dtype=object) #@|Corresponding masses database

    R_Core, M_Core = [], []
    for core in Core_turb2020:
        idx = np.where(core==Cores_db)[0]
        R_Core.extend(R_db[idx])
        M_Core.extend(M_db[idx])


    R_pl_turb, M_pl_turb = [], []

    for i,frac in enumerate(WMFs_turb2020):

        r_core = R_Core[i]
        m_core = M_Core[i]

        R_cons,M_h20, Pt = 8.314, 1.8e-2, 0.1 # fixed
        g_core = G.value * m_core * const.M_earth.value / (r_core*const.R_earth.value)**2
        g = G.value * M_turb2020 * const.M_earth.value / (R_turb2020*const.R_earth.value)**2

        alpha_1, alpha_2, alpha_3, alpha_4, alpha_5, alpha_6 = -3.550, 1.310, 1.099, 4.683e-1, 7.664e-1, 4.224e-1
        beta_1, beta_2, beta_3, beta_4, beta_5 = 2.846, 1.555e-1, 8.777e-2, 6.045e-2, 1.143e-2
        beta_6, beta_7, beta_8, beta_9, beta_10 = 1.736e-2, 1.859e-2, 4.314e-2, 3.393e-2, -1.034e-2

        X = (np.log10(frac)-alpha_1) / alpha_2
        Y = (np.log10(g)-alpha_3) / alpha_4
        Z = (np.log10(Seff_turb2020)-alpha_5)/alpha_6

        X = (np.log10(frac)-alpha_1) / alpha_2
        Y = (np.log10(g)-alpha_3) / alpha_4
        Z = (np.log10(Seff_turb2020)-alpha_5)/alpha_6

        Teff = 10**(beta_1+beta_2*X+beta_3*Y+beta_4*Z+beta_5*X*Y+beta_6*Y**2+beta_7*X**3+beta_8*X**2*Y+beta_9*X*Y**2+beta_10*Y**4)

        #@|z_atm 
        a = np.log(frac / (1-frac) * g_core**2 / 4 / np.pi / G.value / Pt) 
        b = R_cons * Teff / M_h20 / g_core
        c = 1 / (r_core*const.R_earth.value)
        z_atm = (1 / a / b - c)**(-1)

        #r_new = (r_earth_like.values*const.R_earth.value + z_atm) / const.R_earth.value 
        #m_new = m_earth_like.values / (1-frac)

        r_pl = (r_core*const.R_earth.value + z_atm) / const.R_earth.value 
        m_pl = m_core / (1-frac)

        r_pl = np.array(r_pl)
        
        #@|####-Results-########
        R_pl_turb.append(r_pl)
        M_pl_turb.append(m_pl)
        #@|####################
        


# In[ ]:


def aguich2021_MR():
    
    global R_aguich2021, M_aguich2021

    R_aguich2021, M_aguich2021 = [], []
    for i in range(len(x_core_aguich2021)):

        idxs_aguich2021 = np.where((df_aguichine_2021['x_core'] == x_core_aguich2021[i]) &                                    (df_aguichine_2021['x_H2O'] == x_H2O_aguich2021[i]) &                                    (df_aguichine_2021['T_irr'] == Tirr_aguich2021[i]) &                                    (df_aguichine_2021['errcode'] == 0))[0] #@|only pick the errcode = 0 values

        r_aguich2021 = (df_aguichine_2021['R_b'].values + df_aguichine_2021['R_a'].values)[idxs_aguich2021]
        m_aguich2021 = (df_aguichine_2021['M_b'].values + df_aguichine_2021['M_a'].values)[idxs_aguich2021]


        R_aguich2021.append(r_aguich2021)
        M_aguich2021.append(m_aguich2021)
    

# In[ ]:


def luo2024_MR():
    
    global R_luo2024, M_luo2024

    R_luo2024, M_luo2024 = [], []
    for i in range(len(wmf_luo2024)):

        idxs_luo2024 = np.where((np.round(df_luo_2024['total WMF'],2) == wmf_luo2024[i]) &                                    (df_luo_2024['Teq [K]'] == teq_luo2024[i]))                                

        r_luo2024 = df_luo_2024['Radius [Rearth]'].values[idxs_luo2024]
        m_luo2024 = df_luo_2024['Mass [Mearth]'].values[idxs_luo2024]


        R_luo2024.append(r_luo2024)
        M_luo2024.append(m_luo2024)



# In[ ]:


def lopez_fortney2014_MR():
    
    global R_lf2014, M_lf2014
    
    R_lf2014, M_lf2014 = [], []
    
    for i in range(len(age_lf2014)):
        
        df_lf2014 = pd.read_csv(f'{path_models}/Lopez&Fortney_2014_{age_lf2014[i]}_{opacity_lf2014[i]}', sep = " ")
        
        idxs_flux_lf2014 = np.where(df_lf2014['Flux'].values == float(Seff_lf2014[1]))[0]
        
        
        m_lf2014 = df_lf2014['Mass'][idxs_flux_lf2014].values
        r_lf2014 = df_lf2014[f'{H_He[i]}'][idxs_flux_lf2014].values
        
        R_lf2014.append(r_lf2014)
        M_lf2014.append(m_lf2014)


# In[ ]:


def haldemann2024_MR():

    global R_haldemann2024, M_haldemann2024
    
    R_haldemann2024, M_haldemann2024 = [], []

    for i in range(len(models_haldemann2024)):
        
        df_haldemann2024 = pd.read_csv(f'{path_models}/Mass_Radius_{models_haldemann2024[i]}.dat',                                comment = '#', header = None)

        if T_out_haldemann2024[i] == 50:
            idx_R_haldemann2024 = 1
        if T_out_haldemann2024[i] == 300:
            idx_R_haldemann2024 = 2
        if T_out_haldemann2024[i] == 800:
            idx_R_haldemann2024 = 3
        if T_out_haldemann2024[i] == 1500:
            idx_R_haldemann2024 = 4
        if T_out_haldemann2024[i] == 2000:
            idx_R_haldemann2024 = 5


        m_haldemann2024 = df_haldemann2024[0].values
        r_haldemann2024 = df_haldemann2024[idx_R_haldemann2024].values
        
        R_haldemann2024.append(r_haldemann2024)
        M_haldemann2024.append(m_haldemann2024)
          


# In[ ]:


def seager2007_MR():
    
    global R_seager2007, M_seager2007
    
    R_seager2007, M_seager2007 = [], []
    
    m_seager2007 = np.linspace(0, 20, 1000)
    
    for i in range(len(models_seager2007)):
    
        if models_seager2007[i] == 'iron':
                   
            k1, k2, k3 = -0.209490, 0.0804, 0.394
            m1, r1 = 5.80, 2.52
        
        if models_seager2007[i] == 'rock':
                   
            k1, k2, k3 = -0.209594, 0.0799, 0.413
            m1, r1 = 10.55, 3.90

        if models_seager2007[i] == 'water':
                   
            k1, k2, k3 = -0.209396, 0.0807, 0.375
            m1, r1 = 5.52, 4.43
                    
        log_r_seager2007 = k1 + 1/3 * np.log10(m_seager2007/m1) - k2 * (m_seager2007/m1)**k3
        r_seager2007 = 10**log_r_seager2007
        r_seager2007 = r_seager2007 * r1

        
        M_seager2007.append(m_seager2007)
        R_seager2007.append(r_seager2007)
                    


# In[ ]:


def otegi2020_MR():
    
    global R_otegi_small, M_otegi_small, R_otegi_intermediate, M_otegi_intermediate
    
    M_otegi_small = np.linspace(0, 10, 100)
    M_otegi_intermediate = np.linspace(6, 138, 100)
    
    R_otegi_small = 1.03 * M_otegi_small**0.29
    R_otegi_intermediate = 0.70 * M_otegi_intermediate**0.63


# In[ ]:


def parc2024_MR():
    
    global R_parc_small, M_parc_small, R_parc_intermediate,    M_parc_intermediate, R_parc_giant, M_parc_giant,    R_parc_small_upper, R_parc_small_lower,    R_parc_intermediate_upper, R_parc_intermediate_lower,    R_parc_giant_upper, R_parc_giant_lower
    
    M_parc_small = np.linspace(0, 10, 100)
    M_parc_intermediate = np.linspace(6, 138, 100)
    M_parc_giant = np.linspace(138, 10000, 100)
    
    
    R_parc_small = 1.02 * M_parc_small**0.28
    R_parc_intermediate = 0.61 * M_parc_intermediate**0.67
    R_parc_giant = 11.9 * M_parc_giant**0.01

    R_parc_small_upper = (1.02+0.01) * M_parc_small**(0.28+0.01)
    R_parc_small_lower = (1.02-0.01) * M_parc_small**(0.28-0.01)
    
    R_parc_intermediate_upper = (0.61+0.04) * M_parc_intermediate**(0.67+0.02)
    R_parc_intermediate_lower = (0.61-0.04) * M_parc_intermediate**(0.67-0.02)
    
    R_parc_giant_upper = (11.9+0.7) * M_parc_giant**(0.01+0.01)
    R_parc_giant_lower = (11.9-0.7) * M_parc_giant**(0.01-0.01)
    

    

# In[ ]:


def iso_density():
    
    global Radii_iso, Masses_iso
    
    #@|idodensity curves
    radii = np.linspace(0, const.R_earth.value * 25, 10000)
    Radii_iso, Masses_iso = [], []
    for i in range(len(density)):
        
        masses = density[i] * 4 / 3 * np.pi *  radii**3
        
        Radii_iso.append(radii / const.R_earth.value)
        Masses_iso.append(masses / const.M_earth.value)


# In[ ]:





# In[ ]:


#@|Read the configuration file 'config.ini' into a config_object
config_object = ConfigParser()
config_object.read(f"config/{config_file}")

#@|Sections
try:
    CATALOG_DATA = config_object['CATALOG_DATA']
except:
    pass
try:
    MY_DATA = config_object['MY_DATA']
except:
    pass
try:
    MODELS = config_object['MODELS']
except:
    pass
try:
    OPTIONAL_CONFIG = config_object['OPTIONAL_CONFIG']
except:
    pass


# In[ ]:





# In[ ]:


#@|++++++Exoplanet catalog++++++++++
#@|NEA, Exoplanet.eu, or PlanetS
#@|++++++++++++++++++++++++++++++++++
catalog = CATALOG_DATA['catalog']


# In[ ]:


#@|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#@|Load data (df) from the NASA Exoplanet Archive (Confirmed planets)
#@|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if catalog == 'NEA':

    try:
        web_or_local = CATALOG_DATA['web_or_local']
    except: 
        web_or_local = 'local'
    
    try:
        ps_or_composite = CATALOG_DATA['ps_or_composite']
    except:
        ps_or_composite = 'ps'

    if web_or_local == 'web':

        if ps_or_composite == 'ps':
            print('Downloading the "Planetary Systems" table from the NASA Exoplanet Archive ... (this might take a while)')

        if ps_or_composite == 'composite':
            print('Downloading the "Planetary Systems Composite Data" table from the NASA Exoplanet Archive ... (this might take a while)')   

        request = pyvo.dal.TAPQuery('https://exoplanetarchive.ipac.caltech.edu/TAP', 'SELECT * FROM '+ps_or_composite)
        table = pyvo.dal.TAPQuery.execute(request)

        df = pd.DataFrame(table)

    if web_or_local == 'local':

        list_complete = sorted(os.listdir('catalog_data/NEA/'))
        #list_complete

        list_ps = []
        list_composite = []
        for item in list_complete:
            if item[0:10] == 'PSCompPars':
                list_composite.append(item)

            else:
                list_ps.append(item)

        if ps_or_composite == 'ps':

            df = pd.read_csv('catalog_data/NEA/'+list_ps[-1], comment = "#")

        if ps_or_composite == 'composite':

            df = pd.read_csv('catalog_data/NEA/'+list_composite[-1], comment = "#")
            
            
#@|+++++++++++++++++++++++++++++++++++++++++++
#@|Load data df from the Exoplanet.eu catalog 
#@|+++++++++++++++++++++++++++++++++++++++++++ 
    
    
if catalog == 'Exoplanet.eu':
    
    file = os.listdir('catalog_data/Exoplanet.eu/')[0]
    df = pd.read_csv('catalog_data/Exoplanet.eu/'+file)
    
    df = df.rename(columns={'orbital_period':'pl_orbper', 'semi_major_axis':'pl_orbsmax',                           'eccentricity':'pl_orbeccen','discovered':'disc_year',                             'temp_calculated':'pl_eqt_Exoplanet.eu', 'temp_measured':'pl_eqt',                            'log_g':'st_logg','mag_v':'V Mag', 'mag_k':'K Mag','star_distance': 'sy_dist',                            'star_metallicity':'st_met', 'star_mass':'st_mass', 'star_radius': 'st_rad',                            'star_age': 'st_age', 'star_teff':'st_teff',                            'mass':'pl_bmasse','mass_error_min':'pl_bmasseerr2',                            'mass_error_max':'pl_bmasseerr1','radius':'pl_rade',                            'radius_error_min':'pl_radeerr2','radius_error_max':'pl_radeerr1' })            
            
            
#@|++++++++++++++++++++++++++++++++++++++
#@|Load data df from the PlanetS catalog 
#@|++++++++++++++++++++++++++++++++++++++

if catalog == 'PlanetS':
 
    votable_PlanetS = parse("catalog_data/PlanetS/PLANETS.vot")
    table_PlanetS = votable_PlanetS.get_first_table().to_table()
    df = table_PlanetS.to_pandas()
    
    df = df.rename(columns={'Discovery Year':'disc_year', 'Discovery Method':'discoverymethod',                         'Discovery Facility':'disc_facility','Orbital Period [days]':'pl_orbper',                        'Orbit Semi-Major axis [au]':'pl_orbsmax','Eccentricity':'pl_orbeccen',                        'Insolation Flux [Earth Flux]':'pl_insol',                        'Insolation Flux [Earth Flux] - Computation':'pl_insol_PlanetS',                        'Equilibrium Temperature [K]':'pl_eqt',                        'Equilibrium Temperature [K] - Computation':'pl_eqt_PlanetS',                        'Stellar Effective Temperature [K]':'st_teff','Teff [K] (Gaia DR3)':'st_teff_gaia',                        'Stellar Radius [Rsun]':'st_rad','Stellar Mass [Msun]':'st_mass',                        'Stellar Metallicity [dex]':'st_met','[Fe/H] [dex] (Gaia DR3)':'st_met_gaia',                        'Stellar Surface Gravity [log(cm/s**2)]':'st_logg',                        'log(g) [log(cm/s**2)] (Gaia DR3)':'st_logg_gaia','Distance [pc]':'sy_dist',                        'V Mag':'sy_vmag','K Mag':'sy_kmag','Transmission Spectroscopy Metric (TSM) - Computation':'TSM',                        'Emission Spectroscopy Metric (ESM) - Computation':'ESM',                        'Measured Radial Velocity Semi-Amplitude [m/s]':'K_measured','Stellar Age [Gyr]':'st_age',                        'Stellar Age [Gyr] (Gaia DR3)':'st_age_gaia','Stellar Luminosity [log(Lsun)]':'st_lum',                        'Stellar Luminosity [log(Lsun)] (Gaia DR3)':'st_lum_gaia',                        'Planet Mass [Mjup]':'pl_bmasse','Planet Mass - Upper Unc [Mjup]':'pl_bmasseerr1',                        'Planet Mass - Lower Unc [Mjup]':'pl_bmasseerr2',                        'Planet Radius [Rjup]':'pl_rade','Planet Radius - Upper Unc [Rjup]':'pl_radeerr1',                        'Planet Radius - Lower Unc [Rjup]':'pl_radeerr2' })
    


# In[ ]:





# In[ ]:


#@|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#@|We remove those planets with a precision in mass and radius lower than precision_radius and precision_mass
#@|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

precision_radius = float(CATALOG_DATA['precision_radius'])
precision_mass = float(CATALOG_DATA['precision_mass'])


#@|mass precision better than thres
M_pl, M_pl_err = df['pl_bmasse'].values, (abs(df['pl_bmasseerr1'].values) +  abs(df['pl_bmasseerr2'].values)) / 2
idxs_M_pl_thres = np.where(M_pl_err / M_pl < (precision_mass / 100))[0]
#print(str(len(idxs_M_pl_thres))+' of '+str(n_planets)+' planets ('+str(int(len(idxs_M_pl_thres) / n_planets * 100))+'%) have a mass measurement precision below '+str(int(thres*100))+'%.')
df = df.iloc[idxs_M_pl_thres]

#@|radius precision better than thres
R_pl, R_pl_err = df['pl_rade'].values,(abs(df['pl_radeerr1'].values) + abs(df['pl_radeerr2'].values)) / 2
idxs_R_pl_thres = np.where(R_pl_err / R_pl < (precision_radius / 100))[0]
#print(str(len(idxs_R_pl_thres))+' of '+str(n_planets)+' planets ('+str(int(len(idxs_R_pl_thres) / n_planets * 100))+'%) have a mass and radius precision below '+str(int(thres*100))+'%.')
df = df.iloc[idxs_R_pl_thres]


# In[ ]:





# In[ ]:


color_coding = CATALOG_DATA['color_coding']

#@|+++++Numerical and non-numerical color coding++++++++++
if color_coding == 'disc_facility' or color_coding == 'disc_year' or color_coding == 'discoverymethod':
    numerical_color_coding = False
else:
    numerical_color_coding = True


try:
    groups = [str(x.strip()) for x in CATALOG_DATA['groups'].split(',')]
    
    if color_coding == 'disc_year':
        groups = np.array(groups).astype(int)
    
except:
    pass

try:
    colors_groups = [str(x.strip()) for x in CATALOG_DATA['colors_groups'].split(',')]
except:
    pass

try:
    plot_all_planets = CATALOG_DATA['plot_all_planets'] == 'True'
except:
    plot_all_planets = True


# In[ ]:





# In[ ]:


#@|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#@|We remove the rows from the df that have no 'color_coding'
#@|----------Only in the numerical color coding-------------
#@|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

cols = df.columns.values

if numerical_color_coding:
    

    if color_coding in cols:
        idxs_not_nan = np.where(~np.isnan(df[color_coding]))[0]
        df = df.iloc[idxs_not_nan]

    print('Your sample contains '+str(len(df))+' planets')

        
else:
    
    pass


# In[ ]:





# In[ ]:


#@|+++++++++++++++++++to be done++++++++++++++++++++++++++
#@|idxs_without_ttvs = np.where(df['ttv_flag'] == 0)
#@|df = df.iloc[idxs_without_ttvs]
#@print('Your sample contains '+str(len(df))+' planets')


# In[ ]:





# In[ ]:


#@|+++++++++++++++++++++++++++++++++++++++++++++++++++
#@|----Definition of the mass and radius arrays-----
#@|+++++++++++++++++++++++++++++++++++++++++++++++++++

#@|Note: The PlanetS catalog masses and radii are in Rjup. We convert them into Rearth. 

if catalog == 'PlanetS' or catalog == 'Exoplanet.eu':
    
    fac_R = const.R_jup.value / const.R_earth.value
    fac_M = const.M_jup.value / const.M_earth.value
    
else:
    
    fac_M, fac_R = 1, 1
    

R_catalog, R_catalog_err_up, R_catalog_err_down = df['pl_rade'].values, df['pl_radeerr1'].values, df['pl_radeerr2'].values
M_catalog, M_catalog_err_up, M_catalog_err_down = df['pl_bmasse'].values, df['pl_bmasseerr1'].values, df['pl_bmasseerr2'].values


R_catalog, R_catalog_err_up, R_catalog_err_down = R_catalog*fac_R, R_catalog_err_up*fac_R, R_catalog_err_down*fac_R
M_catalog, M_catalog_err_up, M_catalog_err_down = M_catalog*fac_M, M_catalog_err_up*fac_M, M_catalog_err_down*fac_M

#@|Mass and radius upper and lower errors in the same array (for the plots)

R_catalog_ERR = [(abs(R_catalog_err_down[i]), R_catalog_err_up[i]) for i in range(len(R_catalog))]
M_catalog_ERR = [(abs(M_catalog_err_down[i]), M_catalog_err_up[i]) for i in range(len(M_catalog))]
        


# In[ ]:





# In[ ]:


#@|#######--zeng et al. (2016,2019) config--##########
try:
    models_zeng = MODELS['models_zeng']
    models_zeng = [x.strip() for x in models_zeng.split(',')]
    zeng = True
except:
    zeng = False


# In[ ]:


#@|#######--marcus et al. 2010 config--##########
try:
    models_marcus = MODELS['models_marcus']
    models_marcus = [x.strip() for x in models_marcus.split(',')]
    marcus = True
except:
    marcus = False


# In[ ]:


#@|#######--turbet et al. 2020 config--##########
try:
    M_turb2020 = float(MODELS['M_turb2020'])
    R_turb2020 = float(MODELS['R_turb2020'])
    Seff_turb2020 =  float(MODELS['Seff_turb2020'])
    WMFs_turb2020 = [float(x.strip()) for x in MODELS['WMFs_turb2020'].split(',')]
    Core_turb2020 = [x.strip() for x in MODELS['Core_turb2020'].split(',')]
    colors_turb2020 = [x.strip() for x in MODELS['colors_turb2020'].split(',')]
    turb_2020 = True
    turbet2020_MR()
    
except:
    turb_2020 = False    


# In[ ]:


#@|#######--aguichine et al. 2020 config--##########
try:
    x_core_aguich2021 = [float(x.strip()) for x in MODELS['x_core_aguich2021'].split(',')]
    x_H2O_aguich2021 = [float(x.strip()) for x in MODELS['x_H2O_aguich2021'].split(',')]
    Tirr_aguich2021 = [float(x.strip()) for x in MODELS['Tirr_aguich2021'].split(',')]
    colors_aguich2021 = [x.strip() for x in MODELS['colors_aguich2021'].split(',')]
    df_aguichine_2021 = pd.read_csv('theoretical_models/aguichine_2021', comment = "#", sep = '\t')
    aguich2021 = True
    aguich2021_MR()
except:
    aguich2021 = False


# In[ ]:


#@|#######--luo et al. 2024 config--##########
try:
    wmf_luo2024 = [float(x.strip()) for x in MODELS['wmf_luo2024'].split(',')]
    teq_luo2024 = [float(x.strip()) for x in MODELS['teq_luo2024'].split(',')]
    colors_luo2024 = [x.strip() for x in MODELS['colors_luo2024'].split(',')]
    df_luo_2024 = pd.read_csv('theoretical_models/luo2024', comment = "#", sep = '\t')
    luo2024 = True
    luo2024_MR()
except:
    luo2024 = False


# In[ ]:


#@|#######--lopez & fortney et al. 2014 config--##########
try:
    age_lf2014 = [x.strip() for x in MODELS['age_lf2014'].split(',')]
    opacity_lf2014 = [x.strip() for x in MODELS['opacity_lf2014'].split(',')]
    Seff_lf2014 = [x.strip() for x in MODELS['Seff_lf2014'].split(',')]
    H_He = [x.strip() for x in MODELS['H_He'].split(',')]
    colors_lf2014 = [x.strip() for x in MODELS['colors_lf2014'].split(',')]
    lopez_fortney2014 = True
    lopez_fortney2014_MR()
except:
    lopez_fortney2014 = False


# In[ ]:


#@|#######----------haldemann et al. (2024) config---------##########
try:
    models_haldemann2024 = [x.strip() for x in MODELS['models_haldemann2024'].split(',')]
    T_out_haldemann2024 =  [float(x.strip()) for x in MODELS['T_out_haldemann2024'].split(',')]
    colors_haldemann2024 = [x.strip() for x in MODELS['colors_haldemann2024'].split(',')]

    haldemann2024 = True
    haldemann2024_MR()
except:
    haldemann2024 = False


# In[ ]:


#@|#######----------seager et al. (2007) config---------##########
try:
    models_seager2007 = [x.strip() for x in MODELS['models_seager2007'].split(',')]
    colors_seager2007 = [x.strip() for x in MODELS['colors_seager2007'].split(',')]

    seager2007 = True
    seager2007_MR()
except:
    seager2007 = False


# In[ ]:


#@|#######------otegi et al. 2020 config------##########
try:
    models_otegi2020 = MODELS['relations_otegi2020']
    models_otegi2020 = [x.strip() for x in models_otegi2020.split(',')]
    otegi2020 = True
    
    try:
        
        colors_otegi2020 = MODELS['colors_otegi2020']
        colors_otegi2020 = [x.strip() for x in colors_otegi2020.split(',')]
        
    except:
        
        colors_otegi2020[0] = 'k'
        colors_otegi2020[1] = 'k'
        
    try:
        
        linestyles_otegi2020 = MODELS['linestyles_otegi2020']
        linestyles_otegi2020 = [x.strip() for x in linestyles_otegi2020.split(',')]
        
    except:
        
        linestyles_otegi2020[0] = 'dashed'
        linestyles_otegi2020[1] = 'dashed'
         
except:
    
    otegi2020 = False


# In[ ]:


#@|#######------parc et al. 2024 config------##########
try:
    models_parc2024 = MODELS['relations_parc2024']
    models_parc2024 = [x.strip() for x in models_parc2024.split(',')]
    parc2024 = True
    
    try:
        
        colors_parc2024 = MODELS['colors_parc2024']
        colors_parc2024 = [x.strip() for x in colors_parc2024.split(',')]
        
    except:
        
        colors_parc2024[0] = 'k'
        colors_parc2024[1] = 'k'
        colors_parc2024[2] = 'k'
        
    try:
        
        linestyles_parc2024 = MODELS['linestyles_parc2024']
        linestyles_parc2024 = [x.strip() for x in linestyles_parc2024.split(',')]
        
    except:
        
        linestyles_parc2024[0] = 'dashed'
        linestyles_parc2024[1] = 'dashed'
        linestyles_parc2024[2] = 'dashed'

    try:

        uncertainties_parc2024 = MODELS['uncertainties_parc2024']

    except:
        
         uncertainties_parc2024 = False
        
except:
    
    parc2024 = False


# In[ ]:


#@|#######--Isodensity config--##########
try:
    density = [float(x.strip()) for x in MODELS['density'].split(',')]
    for i in range(len(density)):
        density[i] = density[i] * 1000
    colors_density = [x.strip() for x in MODELS['colors_density'].split(',')]
    isodensity = True
except:
    isodensity = False 


# In[ ]:





# In[ ]:


#@|optional configuration

#@|number of columns to make the plot (one or two)

try:
    n_cols = OPTIONAL_CONFIG['n_cols']
except:
    n_cols = 'one'

#@|#####--color_max and color_min--###########

if color_coding != 'none':
    
    if numerical_color_coding:
        
        try: 
            color_min = float(OPTIONAL_CONFIG['color_min'])

        except:
            
            five_per_cent = int(len(df[color_coding].values)*0.05)
            color_min = np.median(np.sort(df[color_coding].values)[:five_per_cent])


        try:
            color_max = float(OPTIONAL_CONFIG['color_max'])

        except:

            if catalog == 'NEA':

                five_per_cent = int(len(df[color_coding].values)*0.05)
                color_max = np.median(np.sort(df[color_coding].values)[-five_per_cent:])

            if catalog == 'PlanetS':

                five_per_cent = int(len(df[color_coding_S].values)*0.05)
                color_max = np.median(np.sort(df[color_coding_S].values)[-five_per_cent:])
    else:
        
        pass

        
    
#@|############--log_x and log_y--##########

try:
    log_x = OPTIONAL_CONFIG['log_x'] == 'True'
except:
    log_x = True
    
try:
    log_y = OPTIONAL_CONFIG['log_y'] == 'True'
except:
    log_y = True
    

#@|###########--xlim and ylim--###############

try:
    x_lims = [float(x.strip()) for x in OPTIONAL_CONFIG['xlim'].split(',')]
except:
    x_lims = [0.5, 21]
    
try:
    y_lims = [float(x.strip()) for x in OPTIONAL_CONFIG['ylim'].split(',')]
except:
    y_lims  = [0.9, 2.8]
    
    
#@|###########--legend location-###############

try:
    loc_legend = OPTIONAL_CONFIG['loc_legend']
except:
    loc_legend = 'upper right'
    
#@|############--plot the low-density super-Earths region--###############

try:
    low_d_sE = OPTIONAL_CONFIG['low_density_superEarths'] == 'True'
except:
    low_d_sE = False
    
    
#@|############--Markersize of the NEA and my planets--###############  
    
try:
    size_catalog_planets = int(OPTIONAL_CONFIG['size_catalog_planets'])
except:
    size_catalog_planets = 35
    
try:   
    size_my_planets = int(OPTIONAL_CONFIG['size_my_planets'])
except:
    size_my_planets = 150
    
    
#@|############--Grey shade below the 100% iron model by Zeng et al. (2019)--###############

try:
    shade_below_pure_iron = OPTIONAL_CONFIG['shade_below_pure_iron'] == 'True'
except:
    shade_below_pure_iron = True
    
    
    
#@|############--Dark background--##########

try:
    dark_background = OPTIONAL_CONFIG['dark_background'] == 'True'
except:
    dark_background = False
    
    
#@|#########---linewidths of the models-----#############

try:   
    lw_models = float(OPTIONAL_CONFIG['lw_models'])
except:
    lw_models = 1.6
    

#@|########-------numbers of columns in the legend--------######

try:   
    n_cols_legend = int(OPTIONAL_CONFIG['n_cols_legend'])
except:
    n_cols_legend = 1
    
    
#@|###########----capsizes-------#############

try:
    capsize = float(OPTIONAL_CONFIG['capsize'])
except:
    capsize = 0
    
    
#@|###########----appearance-------#############  

try:
    appearance = str(OPTIONAL_CONFIG['appearance'])
except:
    appearance = 'standard'
    
    
    
#@|###########----ec_catalog for the plots with no color code-------#############  

try:
    ec_catalog = str(OPTIONAL_CONFIG['ec_catalog'])
except:
    ec_catalog = 'grey' 
    
#@|###########----ec_catalog for the color coded plots-------#############  

try:
    ec_catalog_cc = str(OPTIONAL_CONFIG['ec_catalog_cc'])
except:
    ec_catalog_cc = 'whitesmoke'    
    
    
#@|###########--My planets--###############   
    
text_boxes = False    

mass_upper_limit = []

for i in range(1, 21):
    try:
        globals()['m_p'+str(i)] = float(MY_DATA['m_p'+str(i)])
        globals()['r_p'+str(i)] = float(MY_DATA['r_p'+str(i)])
        globals()['c_p'+str(i)] = MY_DATA['c_p'+str(i)]
    except:
        pass
    
    #|@uncertainties
    
    try:
        globals()['m_p'+str(i)+'_err_up'] = float(MY_DATA['m_p'+str(i)+'_err_up'])
        globals()['m_p'+str(i)+'_err_down'] = float(MY_DATA['m_p'+str(i)+'_err_down'])
        globals()['r_p'+str(i)+'_err_up'] = float(MY_DATA['r_p'+str(i)+'_err_up'])
        globals()['r_p'+str(i)+'_err_down'] = float(MY_DATA['r_p'+str(i)+'_err_down'])
        mass_upper_limit.append(False)
        
    except:
        
        try:
            globals()['m_p'+str(i)+'_err_down'] = float(MY_DATA['m_p'+str(i)+'_err_down'])
            globals()['r_p'+str(i)+'_err_up'] = float(MY_DATA['r_p'+str(i)+'_err_up'])
            globals()['r_p'+str(i)+'_err_down'] = float(MY_DATA['r_p'+str(i)+'_err_down'])
            mass_upper_limit.append(True)
            
        except:
            pass
    
    #@|text boxes
    
    try:
        globals()['name_p'+str(i)] = MY_DATA['name_p'+str(i)]
        #@|location of the text boxes
        globals()['dis_x_p'+str(i)] = float(MY_DATA['dis_x_p'+str(i)])
        globals()['dis_y_p'+str(i)] = float(MY_DATA['dis_y_p'+str(i)])
        text_boxes = True  
    except:
        pass
    
mass_upper_limit = np.array(mass_upper_limit)
    


# In[ ]:





# In[ ]:


def plot_low_density_SE_region():
    
    x = [1.55, 1.58,  2., 2.5, 3.5, 2.6, 1.9]
    y = [1.35, 1.5, 1.67, 1.68, 1.6, 1.38, 1.30]
    #ax.scatter(x, y, zorder=3)

    tck, u = interpolate.splprep([x + x[:1], y + y[:1]], s=0, per=True)
    unew = np.linspace(0, 1, 100)
    basic_form = interpolate.splev(unew, tck)
    ax.plot(basic_form[0], basic_form[1], color='blue', lw=2,alpha = 0.7)
    ax.fill(basic_form[0], basic_form[1], color='dodgerblue', alpha=0.2)


# In[ ]:





# In[ ]:


###########################
#@|--------Main---------#@|
###########################

#@|plot config_object
zorder_lines = -100


ec_my_planets = 'black'
  
    
if dark_background:
    plt.style.use("dark_background")
    ec_my_planets = 'white'
    zeng_models_colors['zeng_2019_pure_iron'] = 'white'

try:
    cmap = OPTIONAL_CONFIG['cmap']
except:
    cmap = 'rainbow'


#@|+++++++++++++++++++++++ 
#@|+++++Color coding++++++            
#@|+++++++++++++++++++++++ 

    
if color_coding in cols:
    if n_cols == 'one':
    
        plt.figure(figsize = (10, 6.56))
        
    if n_cols == 'two':
        
        plt.figure(figsize = (20, 6.56))
        
    
    #@|+++++++++++++++++++++++++++++++++ 
    #@|+++++Numerical Color coding++++++            
    #@|+++++++++++++++++++++++++++++++++ 
    
    if numerical_color_coding:

    
        plt.scatter(M_catalog, R_catalog, c = df[color_coding].values, cmap = cmap, s = size_catalog_planets,                     vmin = color_min, vmax = color_max, lw = 1.1, ec = ec_catalog_cc)
        


        if n_cols == 'one':
            cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
        if n_cols == 'two':
            cbar = plt.colorbar(location = 'left', anchor=(2.3,0.95), aspect = 8, shrink=0.4)

        
        #@|plt.errorbar(M_catalog, R_catalog, yerr = np.array(R_catalog_ERR).T, xerr = np.array(M_catalog_ERR).T,\
                     #@|linestyle = "None", ecolor = 'grey', zorder = -1, lw = 1.8, capsize = capsize, alpha = 1)
        
        #@|++++++++++++++++++++++++++++++++++++++++++++
        #@|Error bars of the same color of data points
        #@|++++++++++++++++++++++++++++++++++++++++++++
        #convert time to a color tuple using the colormap used for scatter
        import matplotlib
        import matplotlib.cm as cm
        norm = matplotlib.colors.Normalize(vmin=color_min, vmax=color_max, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
        time_color = np.array([(mapper.to_rgba(v)) for v in df[color_coding].values])

        #loop over each data point to plot
        for x, y, e1, e2, color in zip(M_catalog, R_catalog,                                        (abs(R_catalog_err_up) + abs(R_catalog_err_down)) / 2,                                        (abs(M_catalog_err_up) + abs(M_catalog_err_down)) / 2, time_color):
            #plt.scatter(x, y, color=color)
            plt.errorbar(x, y, yerr = e1, xerr=e2, lw = 1.8, capsize = capsize, color = color, zorder = -1)
            
            
        #@|++++Color bar++++#@|    
        cbar.set_label(color_coding_labels[color_coding], fontsize = 12)
        cbar.ax.tick_params(labelsize=10)
        #cbar.set_ticks_position('left')


        #@|My planets
        for i in range(1, 21):
            try:
                plt.scatter(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                c = float(globals()['c_p'+str(i)]), ec = ec_my_planets, cmap = cmap, s = 250,                 vmin = color_min, vmax = color_max, marker = 'h',lw = 1.7, zorder = 1000)
                plt.errorbar(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                 xerr = np.array([[globals()['m_p'+str(i)+'_err_down']],[globals()['m_p'+str(i)+'_err_up']]]),                  yerr = np.array([[globals()['r_p'+str(i)+'_err_down']],[globals()['r_p'+str(i)+'_err_up']]]),                  zorder = 999, lw = 1.7, capsize = capsize, color = ec_my_planets)


                if text_boxes == True:

                    plt.text(globals()['m_p'+str(i)] +  globals()['dis_x_p'+str(i)],                      globals()['r_p'+str(i)] +  globals()['dis_y_p'+str(i)], globals()['name_p'+str(i)], fontsize=12.5,                     verticalalignment = 'bottom', horizontalalignment = 'center',                      bbox = {"boxstyle": "round", 'facecolor': 'k', 'alpha': 0.7, 'pad': 0.4},                      c = 'white', weight='bold', zorder = 10000)

            except:
                pass
            
            
    #@|+++++++++++++++++++++++++++++++++++++ 
    #@|+++++Non numerical Color coding++++++            
    #@|+++++++++++++++++++++++++++++++++++++         
            
    else:  
        
        if n_cols == 'one':
    
            plt.figure(figsize = (8, 7))

        if n_cols == 'two':

            plt.figure(figsize = (16, 7))
            
        
        for i in range(len(groups)):

            idxs_ac = np.where(df[color_coding].values==groups[i])[0] 

            
            #@|change for the labels
            if groups[i] == 'Transiting Exoplanet Survey Satellite (TESS)':
                groups[i] = 'TESS'
            
            
            plt.scatter(M_catalog[idxs_ac], R_catalog[idxs_ac], c = colors_groups[i],                         s = size_catalog_planets, lw = 1.1, ec = ec_catalog_cc, label = groups[i], zorder = i)
            
            plt.errorbar(M_catalog[idxs_ac], R_catalog[idxs_ac], yerr = np.array(R_catalog_ERR)[idxs_ac].T,                         xerr = np.array(M_catalog_ERR)[idxs_ac].T,                     linestyle = "None", ecolor = colors_groups[i], zorder = i-1, lw = 2, capsize = capsize)
                     
            
        if plot_all_planets:
            
            plt.scatter(M_catalog, R_catalog, c = 'lightgrey', s = size_catalog_planets,                         ec = ec_catalog_cc, lw = 0.7, alpha = 0.6, zorder = -5, label  = 'Other')
            plt.errorbar(M_catalog, R_catalog, yerr = np.array(R_catalog_ERR).T,                         xerr = np.array(M_catalog_ERR).T,                          linestyle = "None", ecolor = 'grey',                          zorder = -6, lw = 1.3, capsize = capsize, alpha = 0.6)
            
            
        #@|My planets (no color coding)
    
        for i in range(1, 21):
            try:

                if text_boxes == True:

                    plt.scatter(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                                color = globals()['c_p'+str(i)], ec = ec_my_planets,                                marker = 'h', s = size_my_planets, lw = 1.7, zorder = 1000,)
                    plt.errorbar(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                                 xerr = np.array([[globals()['m_p'+str(i)+'_err_down']],                                                  [globals()['m_p'+str(i)+'_err_up']]]),                                  yerr = np.array([[globals()['r_p'+str(i)+'_err_down']],                                                  [globals()['r_p'+str(i)+'_err_up']]]),                                  zorder = 999, lw = 1.7, capsize = capsize, color = globals()['c_p'+str(i)])


                    plt.text(globals()['m_p'+str(i)] +  globals()['dis_x_p'+str(i)],                              globals()['r_p'+str(i)] +  globals()['dis_y_p'+str(i)],                              globals()['name_p'+str(i)], fontsize = 12.5,                             verticalalignment = 'bottom', horizontalalignment = 'center',                              bbox = {"boxstyle": "round",'facecolor': globals()['c_p'+str(i)],                                      'alpha': 0.8, 'pad': 0.4}, c = 'white', weight='bold', zorder = 10000)

                if text_boxes == False:

                    plt.scatter(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                                color = globals()['c_p'+str(i)], ec = ec_my_planets,                                marker = 'h', s = size_my_planets, lw = 1.7,                                zorder = 1000, label = globals()['name_p'+str(i)])
                    plt.errorbar(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                                 xerr = np.array([[globals()['m_p'+str(i)+'_err_down']],                                                  [globals()['m_p'+str(i)+'_err_up']]]),                                  yerr = np.array([[globals()['r_p'+str(i)+'_err_down']],                                                  [globals()['r_p'+str(i)+'_err_up']]]),                                  zorder = 999, lw = 1.7, capsize = capsize, color = globals()['c_p'+str(i)])   

            except:
            
                pass
            

#@|+++++++++++++++++++++++ 
#@|++++No color coding++++            
#@|+++++++++++++++++++++++ 
    
elif color_coding == 'none':
    if n_cols == 'one':
    
        plt.figure(figsize = (8, 7))
        
    if n_cols == 'two':
        
        plt.figure(figsize = (16, 7))
        
    #@|My planets 
    
    for i in range(1, 21):
        try:
            
            if text_boxes == True:
                
                plt.scatter(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                            color = globals()['c_p'+str(i)], ec = ec_my_planets,                            marker = 'h', s = size_my_planets, lw = 1.7, zorder = 1000,)
                plt.errorbar(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                             xerr = np.array([[globals()['m_p'+str(i)+'_err_down']],                                              [globals()['m_p'+str(i)+'_err_up']]]),                              yerr = np.array([[globals()['r_p'+str(i)+'_err_down']],                                              [globals()['r_p'+str(i)+'_err_up']]]),                              zorder = 999, lw = 1.7, capsize = capsize, color = 'k')
                
                
                plt.text(globals()['m_p'+str(i)] +  globals()['dis_x_p'+str(i)],                          globals()['r_p'+str(i)] +  globals()['dis_y_p'+str(i)],                          globals()['name_p'+str(i)], fontsize = 12.5,                         verticalalignment = 'bottom', horizontalalignment = 'center',                          bbox = {"boxstyle": "round",'facecolor': globals()['c_p'+str(i)],                                  'alpha': 0.8, 'pad': 0.4}, c = 'white', weight='bold', zorder = 10000)
                
            if text_boxes == False:
                
                plt.scatter(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                            color = globals()['c_p'+str(i)], ec = ec_my_planets,                            marker = 'h', s = size_my_planets, lw = 1.7,                            zorder = 1000, label = globals()['name_p'+str(i)])
                plt.errorbar(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                             xerr = np.array([[globals()['m_p'+str(i)+'_err_down']],                                              [globals()['m_p'+str(i)+'_err_up']]]),                              yerr = np.array([[globals()['r_p'+str(i)+'_err_down']],                                              [globals()['r_p'+str(i)+'_err_up']]]),                              zorder = 999, lw = 1.7, capsize = capsize, color = 'k')
                
                
   
 
        except:
            
            pass
        
    #@|Catalog planets
    
    if appearance == 'standard':
    
        plt.scatter(M_catalog, R_catalog, c = 'lightgrey', s = size_catalog_planets, ec = ec_catalog,                     lw = 0.7, alpha = 1, zorder = 0)
        plt.errorbar(M_catalog, R_catalog, yerr = np.array(R_catalog_ERR).T, xerr = np.array(M_catalog_ERR).T,                      linestyle = "None", ecolor = 'grey', zorder = -1, lw = 1.45, capsize = capsize, alpha = 1)
     
    if appearance == 'faint':
        plt.scatter(M_catalog, R_catalog, c = 'lightgrey', s = size_catalog_planets, ec = ec_catalog,                     lw = 0.7, alpha = 0.5, zorder = 0)
        plt.errorbar(M_catalog, R_catalog, yerr = np.array(R_catalog_ERR).T, xerr = np.array(M_catalog_ERR).T,                      linestyle = "None", ecolor = 'grey', zorder = -1, lw = 1.45, capsize = capsize, alpha = 0.2)
        
        
        

elif color_coding not in cols:
    
    raise Exception('The selected color code ('+color_coding+') is not availabe in the '+catalog+' catalog.')
        
#@|##########--Theoretical models--###############

#@|Zeng et al. (2016, 2019)

if zeng:

    for model in models_zeng:
        
        if model == 'zeng_2019_pure_iron':
            
            plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],                 pd.read_csv(path_models+model,  sep = '\t', header = None)[1],                     lw = lw_models, linestyle = "solid" , zorder = -100,                     c = zeng_models_colors[model], label =  zeng_models_labels[model])
            
            
            
        elif model == 'zeng_2019_earth_like' or model == 'zeng_2016_20_Fe' or model == 'zeng_2019_pure_rock':
            
            plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],                 pd.read_csv(path_models+model,  sep = '\t', header = None)[1],                     lw = lw_models, linestyle = "dashdot" , zorder = -100,                     c = zeng_models_colors[model], label =  zeng_models_labels[model])
            
        elif model.find('H2O') != -1:
            
            plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],                 pd.read_csv(path_models+model,  sep = '\t', header = None)[1],                     lw = lw_models, linestyle = "dashed" , zorder = -100,                     c = zeng_models_colors[model], label =  zeng_models_labels[model])
            
           
        else:
        
            plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],                 pd.read_csv(path_models+model,  sep = '\t', header = None)[1],                     lw = lw_models*1.4, linestyle = "dotted" , zorder = -100,                     c = zeng_models_colors[model], label =  zeng_models_labels[model])
        
    
#@|Turbet et al. (2020)
if turb_2020:
    
    for i in range(len(WMFs_turb2020)):

        if Core_turb2020[i] == 'earth':
            label_core = 'Earth'
        elif Core_turb2020[i] == 'rock':
            label_core = 'Rock'
        elif Core_turb2020[i] == 'iron':
            label_core = 'Iron'

        label_wmf = WMFs_turb2020[i]

        plt.plot(M_pl_turb[i], R_pl_turb[i], lw = lw_models*1.2, linestyle = 'dotted',                 zorder = -1000, c=colors_turb2020[i], label = label_core + " + "+ str(label_wmf*100)+"% "+r'$\rm H_{2}O$ steam')

        
#@|Aguichine et al. (2021)
if aguich2021:

    for i in range(len(x_core_aguich2021)):

        plt.plot(M_aguich2021[i], R_aguich2021[i], lw = lw_models*1.2, linestyle = 'dotted', zorder = -1000,                 label = str(int(x_core_aguich2021[i]*100))+'% CMF & '+str(int(x_H2O_aguich2021[i]*100))+                 r'% WMF ('+str(int(Tirr_aguich2021[i]))+'K)', c = colors_aguich2021[i])

#@|Luo et al. (2024)
if luo2024:

    for i in range(len(wmf_luo2024)):
        label_wmf = wmf_luo2024[i]
        plt.plot(M_luo2024[i], R_luo2024[i], lw = lw_models*1.2, linestyle = 'dotted', zorder = -1000,                 label = "Earth + " str(label_wmf*100)+"% "+r'$\rm H_{2}O$ ('+str(int(teq_luo2024[i]))+'K)', c = colors_luo2024[i])


#@|Lopez & Fortney et al. (2014)
if lopez_fortney2014:
    
    for i in range(len(age_lf2014)):
        
        plt.plot(M_lf2014[i], R_lf2014[i], lw = lw_models*1.2, linestyle = 'dotted', zorder = -1000,                 label = H_He[i]+'% H/He, '+age_lf2014[i]+','+f' {Seff_lf2014[i]}'+r'$\rm S_{\oplus}$',                 c = colors_lf2014[i])
        
        
#@|Haldemannet al. (2014) 
if haldemann2024:
    
    for i in range(len(models_haldemann2024)):
        
        #@|solid lines for the 100% core planets
        
        if models_haldemann2024[i] == 'C0' or models_haldemann2024[i] == 'C1':
            
            plt.plot(M_haldemann2024[i], R_haldemann2024[i], lw = lw_models*1.2, linestyle = 'solid', zorder = -1000,                 label = models_haldemann2024[i]+                  r' ($T_{\rm out}$ = ' +str(int(T_out_haldemann2024[i]))+' K)',                 c = colors_haldemann2024[i])
        
        else:
        
            plt.plot(M_haldemann2024[i], R_haldemann2024[i], lw = lw_models, linestyle = 'dashed', zorder = -1000,                     label = models_haldemann2024[i]+                      r' ($T_{\rm out}$ = ' +str(int(T_out_haldemann2024[i]))+' K)',                     c = colors_haldemann2024[i])
            
#@|Seager et al. (2007)            
if seager2007:
    
    for i in range(len(models_seager2007)):
        
        if models_seager2007[i] == 'iron':
            
            plt.plot(M_seager2007[i], R_seager2007[i], lw = lw_models*1.2, linestyle = 'solid', zorder = -1000,                 label = r'100% Fe (0% $\rm MgSiO_{3}$)', c = colors_seager2007[i])
            
        if models_seager2007[i] == 'rock':
            
            plt.plot(M_seager2007[i], R_seager2007[i], lw = lw_models*1.2, linestyle = 'dashdot', zorder = -1000,                 label = r'0% Fe (100% $\rm MgSiO_{3}$)', c = colors_seager2007[i])
            
        if models_seager2007[i] == 'water':
            
            plt.plot(M_seager2007[i], R_seager2007[i], lw = lw_models*1.2, linestyle = 'dashed', zorder = -1000,                 label = r'100% $\rm H_{2}O$', c = colors_seager2007[i])
            
            
            
#@|Marcus et al. (2010)
if marcus:

    for model in models_marcus:
        plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],                 pd.read_csv(path_models+model,  sep = '\t', header = None)[1], lw = lw_models*1.4, linestyle = "dotted" ,                 zorder = -100, c = zeng_models_colors[model], label =  zeng_models_labels[model] )

        
#@|Isodensity lines
if isodensity:

    iso_density()

    #for i in range(len(Masses_iso)):
        #plt.plot(Masses_iso[i], Radii_iso[i], lw = lw_models, linestyle = '-.', zorder = -1000,\
                #label = fr'Isodensity ({density[i]/1000} $\rm g / cm^3$)', c = colors_density[i])   
        
    for i in range(len(Masses_iso)):
        plt.plot(Masses_iso[i], Radii_iso[i], lw = lw_models, linestyle = '-.', zorder = -1000,                label = fr'{density[i]/1000} $\rm g / cm^3$ isodensity', c = colors_density[i]) 

        
#@|Otegi et al. (2020)
if otegi2020:
    
    otegi2020_MR()
    
    
    if 'small' in models_otegi2020:
        
        idx = np.where(np.array(models_otegi2020)=='small')[0][0]
        plt.plot(M_otegi_small, R_otegi_small, lw = 2.5, c = colors_otegi2020[idx],                  linestyle = linestyles_otegi2020[idx])
        
    if 'intermediate' in models_otegi2020:
        
        idx = np.where(np.array(models_otegi2020)=='intermediate')[0][0]
        plt.plot(M_otegi_intermediate, R_otegi_intermediate, lw = 2.5, c = colors_otegi2020[idx],                  linestyle =  linestyles_otegi2020[idx])
        
        
    #@|vertical lines (no! to remove)   
    #plt.vlines(x = [10, 138],  ymin = [1.25, 6], ymax = [4.9, 25], linestyle = 'dotted', color = 'k', lw = 1.7)        
        
        
#@|Parc et al. (2024)
if parc2024:
    
    parc2024_MR()
    
    if 'small' in models_parc2024:
        
        idx = np.where(np.array(models_parc2024)=='small')[0][0]
        plt.plot(M_parc_small, R_parc_small, lw = 2.5, c = colors_parc2024[idx],                  linestyle = linestyles_parc2024[idx])

        if uncertainties_parc2024:
            
            plt.fill_between(M_parc_small, R_parc_small_lower, R_parc_small_upper, c=colors_parc2024[idx], alpha=0.5, linestyle = linestyles_parc2024[idx])
        
    if 'intermediate' in models_parc2024:
        
        idx = np.where(np.array(models_parc2024)=='intermediate')[0][0]
        plt.plot(M_parc_intermediate, R_parc_intermediate, lw = 2.5, c = colors_parc2024[idx],                  linestyle =  linestyles_parc2024[idx])
        
        if uncertainties_parc2024:
            
            plt.fill_between(M_parc_intermediate, R_parc_intermediate_lower, R_parc_intermediate_upper, c=colors_parc2024[idx], alpha=0.5, linestyle = linestyles_parc2024[idx])
        
    if 'giant' in models_parc2024:
        
        idx = np.where(np.array(models_parc2024)=='giant')[0][0]
        plt.plot(M_parc_giant, R_parc_giant, lw = 2.5, c = colors_parc2024[idx],                  linestyle = linestyles_parc2024[idx])

        if uncertainties_parc2024:
            
            plt.fill_between(M_parc_giant, R_parc_giant_lower, R_parc_giant_upper, c=colors_parc2024[idx], alpha=0.5, linestyle = linestyles_parc2024[idx]) 

    if ('small' in models_parc2024) & ('intermediate' in models_parc2024):

        sep_small_inter = pd.read_csv('theoretical_models/MR-Water20_650K_DORN.txt')
        plt.plot(sep_small_inter['x'], sep_small_inter['y'], linestyle = 'dotted', color = 'k', lw= 1.7)
    
        
        
    #@|vertical lines (only between intermediate and giant planets)
    #plt.vlines(x = [10, 138],  ymin = [1.25, 6], ymax = [4.9, 25], linestyle = 'dotted', color = 'k', lw = 1.7)
    plt.vlines(x = [138],  ymin = [6], ymax = [25], linestyle = 'dotted', color = 'k', lw = 1.7)
    
    
#@configuration
import matplotlib.ticker as mticker
ax = plt.gca()
if log_x == True:
    ax.set_xscale('log')
if log_y == True:
    ax.set_yscale('log')
    

ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

from matplotlib.ticker import FormatStrFormatter
ax.yaxis.set_minor_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))


ax.tick_params(which='major', length = 9, color = ec_my_planets, direction = 'in', width = 1.3)
ax.tick_params(which='minor', length = 5, color = ec_my_planets, direction = 'in', width = 0.9)



if color_coding == 'none':

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=14)

    plt.ylabel(r'Planet radius $\rm (R_{\oplus})$', fontsize = 16)
    plt.xlabel(r'Planet mass $\rm (M_{\oplus})$', fontsize = 16)    
    
else:
    
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.tick_params(axis='both', which='minor', labelsize=13)

    plt.ylabel(r'Planet radius $\rm (R_{\oplus})$', fontsize = 15)
    plt.xlabel(r'Planet mass $\rm (M_{\oplus})$', fontsize = 15)   
    
plt.xlim(x_lims)
plt.ylim(y_lims)


if n_cols == 'one':
    plt.legend(loc = loc_legend, fontsize = 10, markerscale = 1, ncol = n_cols_legend)
if n_cols == 'two':
    plt.legend(loc = loc_legend, fontsize = 12.5, ncol = n_cols_legend)

#@|low density super-Earths region

if low_d_sE:
    plot_low_density_SE_region()
    
#@| Region below the 100% iron model by Zeng et al. (2019)
    
if shade_below_pure_iron:
    
    if haldemann2024:
        
        if 'C0' in models_haldemann2024:

            idxs_C0 = np.where(np.array(models_haldemann2024) == 'C0')[0]
            T_out_min = np.min(np.array(T_out_haldemann2024)[idxs_C0])
            
            df_haldemann2024 = pd.read_csv(f'{path_models}/Mass_Radius_C0.dat',                                comment = '#', header = None)
            
        if 'C1' in models_haldemann2024 and 'C0' not in models_haldemann2024:
            
            idxs_C1 = np.where(np.array(models_haldemann2024) == 'C1')[0]
            T_out_min = np.min(np.array(T_out_haldemann2024)[idxs_C1])
            
            df_haldemann2024 = pd.read_csv(f'{path_models}/Mass_Radius_C1.dat',                                comment = '#', header = None)
            
            
        if T_out_min == 50:
            idx_R_haldemann2024 = 1

        if T_out_min == 300:
            idx_R_haldemann2024 = 2

        if T_out_min == 800:
            idx_R_haldemann2024 = 3

        if T_out_min == 1500:
            idx_R_haldemann2024 = 4

        if T_out_min == 2000:
            idx_R_haldemann2024 = 5

        m_pure_iron = df_haldemann2024[0].values
        r_pure_iron = df_haldemann2024[idx_R_haldemann2024].values

        plt.fill_between(m_pure_iron, r_pure_iron, 0,  alpha = 0.6, color = 'grey', zorder = -1000)
            
    
    else:
        
        #@|Zeng et al. (2019)
        r_pure_iron = pd.read_csv(path_models+'zeng_2019_pure_iron',  sep = '\t', header = None)[1].values
        m_pure_iron = pd.read_csv(path_models+'zeng_2019_pure_iron',  sep = '\t', header = None)[0].values
        plt.fill_between(m_pure_iron, r_pure_iron, 0,  alpha = 0.6, color = 'grey', zorder = -1000)
    


plt.savefig(f'output/{config_file[:-4]}.pdf', bbox_inches = 'tight', pad_inches = 0.1)
plt.savefig(f'output/{config_file[:-4]}.png', bbox_inches = 'tight', pad_inches = 0.1, dpi = 400)


print('')
print('\033[1m' + f'Your diagram {config_file[:-4]}.pdf/png has been successfully generated and saved')
print('\033[0m')
print('     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('      Thank you for using Mister plotter :-D We hope to see you again soon!')
print('     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('')


# In[ ]:





# In[ ]:



# In[ ]:





# In[ ]:




