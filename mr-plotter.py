#!/usr/bin/env python
# coding: utf-8

# In[ ]:


###########################
#@|-----mr-plotter------#@|
###########################


# In[ ]:


import os
import pyvo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
from configparser import ConfigParser
from astropy.constants import G
import astropy.constants as const
import argparse


# In[ ]:


#@|Uncomment this for the mr-plotter.py version
#parser = argparse.ArgumentParser()
#parser.add_argument('config_file')
#args = parser.parse_args()
#config_file = args.config_file


# In[ ]:


#@|Uncomment this for the mr.plotter.ipynb version
#@|#####--Configuration file--#########
config_file = 'example4.ini'
#@|####################################


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


#@|Read the configuration file 'config.ini' into a config_object
config_object = ConfigParser()
config_object.read(f"config/{config_file}")

#@|Sections
try:
    NEA_DATA = config_object['NEA_DATA']
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


#@|Load data from the NASA Exoplanet Archive (Confirmed planets)
web_or_local = NEA_DATA['web_or_local']
ps_or_composite = NEA_DATA['ps_or_composite']

if web_or_local == 'web':
    
    if ps_or_composite == 'ps':
        print('Downloading the "Planetary Systems" table from the NASA Exoplanet Archive ... (this might take a while)')
    
    if ps_or_composite == 'composite':
        print('Downloading the "Planetary Systems Composite Data" table from the NASA Exoplanet Archive ... (this might take a while)')   
        
    request = pyvo.dal.TAPQuery('https://exoplanetarchive.ipac.caltech.edu/TAP', 'SELECT * FROM '+ps_or_composite)
    table = pyvo.dal.TAPQuery.execute(request)
    
    df = pd.DataFrame(table)
    
if web_or_local == 'local':
    
    list_complete = sorted(os.listdir('NEA_data/'))
    #list_complete

    list_ps = []
    list_composite = []
    for item in list_complete:
        if item[0:10] == 'PSCompPars':
            list_composite.append(item)

        else:
            list_ps.append(item)
            
    if ps_or_composite == 'ps':
        
        df = pd.read_csv('NEA_data/'+list_ps[-1], comment = "#")
        
    if ps_or_composite == 'composite':
        
        df = pd.read_csv('NEA_data/'+list_composite[-1], comment = "#")


# In[ ]:


#@|We remove the planets with a precision in mass and radius lower than precision_radius and precision_mass

precision_radius = float(NEA_DATA['precision_radius'])
precision_mass = float(NEA_DATA['precision_mass'])

#@|mass precision better than thres
M_pl, M_pl_err = df['pl_bmasse'].values, (abs(df['pl_bmasseerr1'].values) + abs(df['pl_bmasseerr1'].values)) / 2
idxs_M_pl_thres = np.where(M_pl_err / M_pl < (precision_mass / 100))[0]
#print(str(len(idxs_M_pl_thres))+' of '+str(n_planets)+' planets ('+str(int(len(idxs_M_pl_thres) / n_planets * 100))+'%) have a mass measurement precision below '+str(int(thres*100))+'%.')
df = df.iloc[idxs_M_pl_thres]

#@|radius precision better than thres
R_pl, R_pl_err = df['pl_rade'].values, (abs(df['pl_radeerr1'].values) + abs(df['pl_radeerr2'].values)) / 2
idxs_R_pl_thres = np.where(R_pl_err / R_pl < (precision_radius / 100))[0]
#print(str(len(idxs_R_pl_thres))+' of '+str(n_planets)+' planets ('+str(int(len(idxs_R_pl_thres) / n_planets * 100))+'%) have a mass and radius precision below '+str(int(thres*100))+'%.')
df = df.iloc[idxs_R_pl_thres]


# In[ ]:


#@|We remove the rows from the df that have not 'color_coding'
color_coding = NEA_DATA['color_coding']

df_cols = df.columns.values
if color_coding in df_cols:
    idxs_not_nan = np.where(~np.isnan(df[color_coding]))[0]
    df = df.iloc[idxs_not_nan]
    
print('Your sample contains '+str(len(df))+' planets')


# In[ ]:


#@|Definition of the Mass and radius arrays
R_NEA, R_NEA_err_up, R_NEA_err_down = df['pl_rade'].values, df['pl_radeerr1'].values, df['pl_radeerr2'].values
M_NEA, M_NEA_err_up, M_NEA_err_down = df['pl_bmasse'].values, df['pl_bmasseerr1'].values, df['pl_bmasseerr2'].values

#@|Mass and radius upper and lower errors in the same array (for the plots)

R_NEA_ERR = [(abs(R_NEA_err_down[i]), R_NEA_err_up[i]) for i in range(len(R_NEA))]
M_NEA_ERR = [(abs(M_NEA_err_down[i]), M_NEA_err_up[i]) for i in range(len(M_NEA))]


# In[ ]:


#@|zeng et al. (2016,2019) and marcus et al. (2010) colors and labels
#@|data from https://lweb.cfa.harvard.edu/~lzeng/planetmodels.html

models_dic_colors = {'zeng_2019_pure_iron':'black', 'zeng_2019_earth_like': 'red', 'zeng_2019_pure_rock': 'orange',                    'zeng_2019_0.1_H2_onto_earth_like_300K': 'darkslateblue',                    'zeng_2019_0.3_H2_onto_earth_like_300K':'mediumslateblue',                    'zeng_2019_1_H2_onto_earth_like_300K': 'mediumpurple',                    'zeng_2019_2_H2_onto_earth_like_300K': 'rebeccapurple',                    'zeng_2019_5_H2_onto_earth_like_300K': 'blueviolet',                    'zeng_2019_0.1_H2_onto_earth_like_500K': 'indigo',                    'zeng_2019_0.3_H2_onto_earth_like_500K': 'darkorchid',                    'zeng_2019_1_H2_onto_earth_like_500K': 'darkviolet',                    'zeng_2019_2_H2_onto_earth_like_500K': 'mediumorchid',                    'zeng_2019_5_H2_onto_earth_like_500K': 'thistle',                    'zeng_2019_0.1_H2_onto_earth_like_700K': 'plum',                    'zeng_2019_0.3_H2_onto_earth_like_700K': 'violet',                    'zeng_2019_1_H2_onto_earth_like_700K': 'purple',                    'zeng_2019_2_H2_onto_earth_like_700K': 'darkmagenta',                    'zeng_2019_5_H2_onto_earth_like_700K': 'fuchsia',                    'zeng_2019_0.1_H2_onto_earth_like_1000K': 'magenta',                    'zeng_2019_0.3_H2_onto_earth_like_1000K': 'orchid',                    'zeng_2019_1_H2_onto_earth_like_1000K': 'mediumvioletred',                    'zeng_2019_2_H2_onto_earth_like_1000K': 'deepping',                    'zeng_2019_5_H2_onto_earth_like_1000K': 'hotpink',                    'zeng_2019_0.1_H2_onto_earth_like_2000K': 'lavenderblush',                    'zeng_2019_0.3_H2_onto_earth_like_2000K': 'palevioletred',                    'zeng_2019_1_H2_onto_earth_like_2000K': 'crimson',                    'zeng_2019_2_H2_onto_earth_like_2000K': 'pink',                    'zeng_2019_5_H2_onto_earth_like_2000K': 'lightpink',                    'zeng_2019_50_H2O_300K': 'navy',                    'zeng_2019_50_H2O_500K': 'blue',                    'zeng_2019_50_H2O_700K': 'royalblue',                    'zeng_2019_50_H2O_1000K': 'deepskyblue',                    'zeng_2019_100_H2O_300K': 'darkcyan',                    'zeng_2019_100_H2O_500K': 'darkturquoise',                    'zeng_2019_100_H2O_700K': 'dodgerblue',                    'zeng_2019_100_H2O_1000K': 'cyan',                    'zeng_2016_20_Fe': 'brown',                    'marcus_2010_maximum_collision_stripping': 'green'
                    }

models_dic_labels = {'zeng_2019_pure_iron':r'100% Fe (0% $\rm MgSiO_{3}$)',                    'zeng_2019_earth_like': r'33% Fe (66% $\rm MgSiO_{3}$)',                    'zeng_2019_pure_rock': r'0% Fe (100% $\rm MgSiO_{3}$)',                    'zeng_2019_0.1_H2_onto_earth_like_300K': r'Earth + 0.1% $\rm H_{2}$ (300K)',                    'zeng_2019_0.3_H2_onto_earth_like_300K': r'Earth + 0.3% $\rm H_{2}$ (300K)',                    'zeng_2019_1_H2_onto_earth_like_300K': r'Earth + 1% $\rm H_{2}$ (300K)',                    'zeng_2019_2_H2_onto_earth_like_300K': r'Earth + 2% $\rm H_{2}$ (300K)',                    'zeng_2019_5_H2_onto_earth_like_300K': r'Earth + 5% $\rm H_{2}$ (300K)',                    'zeng_2019_0.1_H2_onto_earth_like_500K': r'Earth + 0.1% $\rm H_{2}$ (500K)',                    'zeng_2019_0.3_H2_onto_earth_like_500K': r'Earth + 0.3% $\rm H_{2}$ (500K)',                    'zeng_2019_1_H2_onto_earth_like_500K': r'Earth + 1% $\rm H_{2}$ (500K)',                    'zeng_2019_2_H2_onto_earth_like_500K': r'Earth + 2% $\rm H_{2}$ (500K)',                    'zeng_2019_5_H2_onto_earth_like_500K': r'Earth + 5% $\rm H_{2}$ (500K)',                    'zeng_2019_0.1_H2_onto_earth_like_700K': r'Earth + 0.1% $\rm H_{2}$ (700K)',                    'zeng_2019_0.3_H2_onto_earth_like_700K': r'Earth + 0.3% $\rm H_{2}$ (700K)',                    'zeng_2019_1_H2_onto_earth_like_700K': r'Earth + 1% $\rm H_{2}$ (700K)',                    'zeng_2019_2_H2_onto_earth_like_700K': r'Earth + 2% $\rm H_{2}$ (700K)',                    'zeng_2019_5_H2_onto_earth_like_700K': r'Earth + 5% $\rm H_{2}$ (700K)',                    'zeng_2019_0.1_H2_onto_earth_like_1000K': r'Earth + 0.1% $\rm H_{2}$ (1000K)',                    'zeng_2019_0.3_H2_onto_earth_like_1000K': r'Earth + 0.3% $\rm H_{2}$ (1000K)',                    'zeng_2019_1_H2_onto_earth_like_1000K': r'Earth + 1% $\rm H_{2}$ (1000K)',                    'zeng_2019_2_H2_onto_earth_like_1000K': r'Earth + 2% $\rm H_{2}$ (1000K)',                    'zeng_2019_5_H2_onto_earth_like_1000K': r'Earth + 5% $\rm H_{2}$ (1000K)',                    'zeng_2019_0.1_H2_onto_earth_like_2000K': r'Earth + 0.1% $\rm H_{2}$ (2000K)',                    'zeng_2019_0.3_H2_onto_earth_like_2000K': r'Earth + 0.3% $\rm H_{2}$ (2000K)',                    'zeng_2019_1_H2_onto_earth_like_2000K': r'Earth + 1% $\rm H_{2}$ (2000K)',                    'zeng_2019_2_H2_onto_earth_like_2000K': r'Earth + 2% $\rm H_{2}$ (2000K)',                    'zeng_2019_5_H2_onto_earth_like_2000K': r'Earth + 5% $\rm H_{2}$ (2000K)',                    'zeng_2016_20_Fe': r'20% Fe (80% $\rm MgSiO_{3}$)',                    'zeng_2019_50_H2O_300K': r'50% $\rm H_{2}O$',                    'zeng_2019_50_H2O_500K': r'50% $\rm H_{2}O$ (500K)',                    'zeng_2019_50_H2O_700K': r'50% $\rm H_{2}O$ (700K)',                    'zeng_2019_50_H2O_1000K': r'50% $\rm H_{2}O$ (1000K)',                    'zeng_2019_100_H2O_300K': r'100% $\rm H_{2}O$ (300K)',                    'zeng_2019_100_H2O_500K': r'100% $\rm H_{2}O$ (500K)',                    'zeng_2019_100_H2O_700K': r'100% $\rm H_{2}O$ (700K)',                    'zeng_2019_100_H2O_1000K': r'100% $\rm H_{2}O$ (1000K)',                    'marcus_2010_maximum_collision_stripping': 'Max. collisional stripping'
                    }


# In[ ]:


color_codings_label_dic = {'disc_year': 'Discovery year',                            'pl_orbper': 'Orbital period (days)',                           'pl_orbsmax': 'Semi-major axis (AU)',                           'pl_orbeccen': 'Eccentricity',                           'pl_insol': r'Insolation Flux $\rm (S_{\oplus})$',                            'pl_eqt': 'Equilibrium temperature (K)',                           'st_teff': 'Stellar effective temperature (K)',                           'st_rad': r'Stellar radius $\rm (R_{\odot})$' ,                           'st_mass':r'Stellar mass $\rm (M_{\odot})$' ,                           'st_met': r'Star metallicity (dex)',                           'st_logg': 'Stellar surface gravity (dex)',                           'sy_dist': 'Distance (pc)',                           'sy_vmag': r'$V$ (Johnson) magnitude',                           'sy_kmag': r'$K_{\rm s}$ (2MASS) magnitude',                           'sy_gaiamag': r'$Gaia$ magnitude' }


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


#@|optional configuration

#@|number of columns to make the plot (one or two)

try:
    n_cols = OPTIONAL_CONFIG['n_cols']
except:
    n_cols = 'one'

#@|#####--color_max and color_min--###########

if color_coding != 'none':
    
    try: 
        color_max = float(OPTIONAL_CONFIG['color_max'])
    except:
        five_per_cent = int(len(df[color_coding].values)*0.05)
        color_min = np.median(np.sort(df[color_coding].values)[:five_per_cent])

    try:
        color_min = float(OPTIONAL_CONFIG['color_min'])
    except:
        five_per_cent = int(len(df[color_coding].values)*0.05)
        color_max= np.median(np.sort(df[color_coding].values)[-five_per_cent:])
    
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
    loc_legend = 'lower right'
    
#@|############--plot the low-density super-Earths region--###############

try:
    low_d_sE = OPTIONAL_CONFIG['low_density_superEarths'] == 'True'
except:
    low_d_sE = False
    
    
#@|############--Markersize of the NEA and my planets--###############  
    
try:
    size_NEA_planets = float(OPTIONAL_CONFIG['size_NEA_planets'])
    size_my_planets = float(OPTIONAL_CONFIG['size_my_planets'])
except:
    size_my_planets = 200
    size_NEA_planets = 120
    
    
#@|############--Grey shade below the 100% iron model by Zeng et al. (2019)--###############

try:
    shade_below_pure_iron = OPTIONAL_CONFIG['shade_below_pure_iron'] == 'True'
except:
    shade_below_pure_iron = True

    
    
#@|###########--My planets--###############   
    
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
    except:
        pass
    
    #@|text boxes
    
    try:
        globals()['name_p'+str(i)] = MY_DATA['name_p'+str(i)]
        globals()['dis_x_p'+str(i)] = float(MY_DATA['dis_x_p'+str(i)])
        globals()['dis_y_p'+str(i)] = float(MY_DATA['dis_y_p'+str(i)])
        text_boxes = True  
    except:
        pass
    


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


###########################
#@|--------Main---------#@|
###########################

#@|plot config_object
zorder_lines = -100
lw_models = 1.8

try:
    cmap = OPTIONAL_CONFIG['cmap']
except:
    cmap = 'rainbow'


#@|##########--NEA and my planets--###############

if color_coding in df_cols:
    if n_cols == 'one':
    
        plt.figure(figsize = (10, 6.56))
        
    if n_cols == 'two':
        
        plt.figure(figsize = (20, 6.56))
        
    
    
    #idx_color = np.where(df_cols==color_coding)[0]
    #@|NEA planets
    plt.scatter(M_NEA, R_NEA, c = df[color_coding].values, cmap = cmap, s = size_NEA_planets,                 vmin = color_min, vmax = color_max, lw = 1.5, ec = 'grey')
    
    if n_cols == 'one':
        cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
    if n_cols == 'two':
        cbar = plt.colorbar(location = 'left', anchor=(2.3,0.95), aspect = 8, shrink=0.4)
        
    cbar.set_label(color_codings_label_dic[color_coding], fontsize = 12)
    cbar.ax.tick_params(labelsize=10)
    
    #cbar.set_ticks_position('left')
    plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T,                 linestyle = "None", ecolor = 'grey', zorder = -1, lw = 2, capsize = 2)
    
    #@|My planets
    for i in range(1, 21):
        try:
            plt.scatter(globals()['m_p'+str(i)], globals()['r_p'+str(i)],            c = float(globals()['c_p'+str(i)]), ec = 'black', cmap = cmap, s = 250,             vmin = color_min, vmax = color_max, marker = 'p',lw = 2.5, zorder = 1000)
            plt.errorbar(globals()['m_p'+str(i)], globals()['r_p'+str(i)],             xerr = np.array([[globals()['m_p'+str(i)+'_err_down']],[globals()['m_p'+str(i)+'_err_up']]]),              yerr = np.array([[globals()['r_p'+str(i)+'_err_down']],[globals()['r_p'+str(i)+'_err_up']]]),              zorder = 999, lw = 2.5, capsize = 4, color = 'black')


            if text_boxes == True:

                plt.text(globals()['m_p'+str(i)] +  globals()['dis_x_p'+str(i)],                  globals()['r_p'+str(i)] +  globals()['dis_y_p'+str(i)], globals()['name_p'+str(i)], fontsize=14,                 verticalalignment = 'bottom', horizontalalignment = 'center',                  bbox = {"boxstyle": "round", 'facecolor': 'magenta', 'alpha': 0.7, 'pad': 0.4},                  c = 'white', weight='bold', zorder = 10000)
                
        except:
            pass
    

if color_coding == 'none':
    if n_cols == 'one':
    
        plt.figure(figsize = (8, 7))
        
    if n_cols == 'two':
        
        plt.figure(figsize = (16, 7))
        
        
    #@|NEA planets
    plt.scatter(M_NEA, R_NEA, c = 'lightgrey', s = size_NEA_planets, ec = "grey", lw = 1.5)
    plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T,                  linestyle = "None", ecolor = 'grey', zorder = -1, lw = 2, capsize = 2)

    #@|My planets
    for i in range(1, 21):
        try:
            plt.scatter(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                        color = globals()['c_p'+str(i)], ec = 'black', marker = 'p', s = 250, lw = 2, zorder = 1000)
            plt.errorbar(globals()['m_p'+str(i)], globals()['r_p'+str(i)],                         xerr = np.array([[globals()['m_p'+str(i)+'_err_down']],[globals()['m_p'+str(i)+'_err_up']]]),                          yerr = np.array([[globals()['r_p'+str(i)+'_err_down']],[globals()['r_p'+str(i)+'_err_up']]]),                          zorder = 999, lw = 2, capsize = 4, color = 'black')
           
            
            if text_boxes == True:
                
                
                plt.text(globals()['m_p'+str(i)] +  globals()['dis_x_p'+str(i)],                          globals()['r_p'+str(i)] +  globals()['dis_y_p'+str(i)], globals()['name_p'+str(i)], fontsize=14,                         verticalalignment = 'bottom', horizontalalignment = 'center',                          bbox = {"boxstyle": "round",'facecolor': globals()['c_p'+str(i)], 'alpha': 0.7, 'pad': 0.4},                          c = 'white', weight='bold', zorder = 10000)
 
        except:
            
            pass
        
#@|##########--Theoretical models--###############

#@|Zeng et al. (2016, 2019)

if zeng:

    for model in models_zeng:
        plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],                 pd.read_csv(path_models+model,  sep = '\t', header = None)[1], lw = lw_models, linestyle = "dashed" ,                 zorder = -100, c = models_dic_colors[model], label =  models_dic_labels[model] )
        
#@|Marcus et al. (2010)

if marcus:

    for model in models_marcus:
        plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],                 pd.read_csv(path_models+model,  sep = '\t', header = None)[1], lw = lw_models*1.2, linestyle = "dotted" ,                 zorder = -100, c = models_dic_colors[model], label =  models_dic_labels[model] )
    
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
        
#@|Lopez & Fortney et al. (2014)

if lopez_fortney2014:
    
    for i in range(len(age_lf2014)):
        
        plt.plot(M_lf2014[i], R_lf2014[i], lw = lw_models*1.2, linestyle = 'dotted', zorder = -1000,                 label = H_He[i]+'% H/He, '+age_lf2014[i]+','+f' {Seff_lf2014[i]}'+r'$\rm S_{\oplus}$',                 c = colors_lf2014[i])
        
#@|Isodensity lines

if isodensity:

    iso_density()

    for i in range(len(Masses_iso)):
        plt.plot(Masses_iso[i], Radii_iso[i], lw = lw_models, linestyle = '-.', zorder = -1000,                label = fr'Isodensity ({density[i]/1000} $\rm g/cm^3$)', c = colors_density[i])     
    
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

if color_coding == 'none':

    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.tick_params(axis='both', which='minor', labelsize=15)

    plt.ylabel(r'Planet Radius $\rm (R_{\oplus})$', fontsize = 17)
    plt.xlabel(r'Planet Mass $\rm (M_{\oplus})$', fontsize = 17)    
    
else:
    
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.tick_params(axis='both', which='minor', labelsize=13)

    plt.ylabel(r'Planet Radius $\rm (R_{\oplus})$', fontsize = 15)
    plt.xlabel(r'Planet Mass $\rm (M_{\oplus})$', fontsize = 15)   
    
plt.xlim(x_lims)
plt.ylim(y_lims)

if n_cols == 'one':
    plt.legend(loc = loc_legend, fontsize = 11)
if n_cols == 'two':
    plt.legend(loc = loc_legend, fontsize = 13)

#@|low density super-Earths region

if low_d_sE:
    plot_low_density_SE_region()
    
#@| Region below the 100% iron model by Zeng et al. (2019)
    
if shade_below_pure_iron:
    r_pure_iron = pd.read_csv(path_models+'zeng_2019_pure_iron',  sep = '\t', header = None)[1].values
    m_pure_iron = pd.read_csv(path_models+'zeng_2019_pure_iron',  sep = '\t', header = None)[0].values
    plt.fill_between(m_pure_iron, r_pure_iron, 0,  alpha = 0.3, color = 'grey', zorder = -1000)
    
    

#plt.axhline(1.5)
#plt.axhline(2.0)

#x = [0,1000]
#plt.fill_between(x, 1.9, 1.6, alpha = 0.1, color = 'green', zorder = -1000, )

#plt.plot(x, 2*[1.6], linestyle = "dashdot", c = 'green')
#plt.plot(x, 2*[1.9], linestyle = "dashdot", c = 'green')

plt.savefig(f'output/{config_file[:-4]}.pdf', bbox_inches = 'tight', pad_inches = 0.2)
plt.savefig(f'output/{config_file[:-4]}.png', bbox_inches = 'tight', pad_inches = 0.2, dpi = 400)

print('Your mass-radius diagram has been saved successfully!')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




