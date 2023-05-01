#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate


# ### M-R diagram

# In[2]:


#@|inputs
color_coding = 'none'  # 'none', 'st_met', 'pl_insol'

#@|my planet(s)
#@|TOI-244
m_toi244_b, merr_toi244_b = 2.66, 0.31
r_toi244_b, rerr_toi244_b = 1.52, 0.11
#@|TOI-4481 b | Still not in the NEA (Palle et al. 2022)
m_toi4481_b, merr_toi4481_b = 1.90, 0.17
r_toi4481_b, rerr_toi4481_b = 1.331, 0.023

#m_toi244_b, merr_toi244_b = 1, 0
#r_toi244_b, rerr_toi244_b = 1, 0

#@|Load data from the Nasa Exoplanet Archive (Confirmed planets)
NEA_table = 'composite' # 'normal' or 'composite'

#@|We remove the planets with a precision in mass and radius lower than 'thres'
thres = 0.2


# In[9]:


#@|Load data from the Nasa Exoplanet Archive (Confirmed planets)
#@|TODO. See if this can be accesed directly
#@|TODO. See how to acces the tepcat database as well
#@|TODO. Give the user the opportunity to use the table from internet or his/her own table

if NEA_table == 'composite':
    df = pd.read_csv('PSCompPars_2023.04.04_11.24.47.csv')

elif NEA_table == 'normal':
    df = pd.read_csv('PS_2023.04.04_11.29.04.csv')
    
n_planets = len(df)


# In[10]:


#@|We remove the planets with a precision in mass and radius lower than 'thres'
#thres = 0.2

#@|mass precision better than thres
M_pl, M_pl_err = df['pl_bmasse'].values, (abs(df['pl_bmasseerr1'].values) + abs(df['pl_bmasseerr1'].values)) / 2
idxs_M_pl_thres = np.where(M_pl_err / M_pl < thres)[0]
#print(str(len(idxs_M_pl_thres))+' of '+str(n_planets)+' planets ('+str(int(len(idxs_M_pl_thres) / n_planets * 100))+'%) have a mass measurement precision below '+str(int(thres*100))+'%.')
df = df.iloc[idxs_M_pl_thres]

#@|radius precision better than thres
R_pl, R_pl_err = df['pl_rade'].values, (abs(df['pl_radeerr1'].values) + abs(df['pl_radeerr2'].values)) / 2
idxs_R_pl_thres = np.where(R_pl_err / R_pl < thres)[0]
#print(str(len(idxs_R_pl_thres))+' of '+str(n_planets)+' planets ('+str(int(len(idxs_R_pl_thres) / n_planets * 100))+'%) have a mass and radius precision below '+str(int(thres*100))+'%.')
df = df.iloc[idxs_R_pl_thres]


# In[ ]:





# In[12]:


#@|We remove the rows from the df that have not 'color_coding'
df_cols = df.columns.values
if color_coding in df_cols:
    idxs_not_nan = np.where(~np.isnan(df[color_coding]))[0]
    df = df.iloc[idxs_not_nan]


# In[13]:


#@|Definition of the Mass and radius arrays
R_NEA, R_NEA_err_up, R_NEA_err_down = df['pl_rade'].values, df['pl_radeerr1'].values, df['pl_radeerr2'].values
M_NEA, M_NEA_err_up, M_NEA_err_down = df['pl_bmasse'].values, df['pl_bmasseerr1'].values, df['pl_bmasseerr2'].values

#@|Mass and radius upper and lower errors in the same array (for the plots)

R_NEA_ERR = [(abs(R_NEA_err_down[i]), R_NEA_err_up[i]) for i in range(len(R_NEA))]
M_NEA_ERR = [(abs(M_NEA_err_down[i]), M_NEA_err_up[i]) for i in range(len(M_NEA))]


# In[14]:


#@|EXTRA
#@|The most up-to-date parameters for TOI-561 b comes from Brinkman et al. (2023)
#@|As of April 2023 those parameters are still not in the NEA
#@|We replace the current ones by those from Brinkman et al. 2023
#@|TO COMMENT THE WHOLE CELL AFTER Brinkman et al. (2023) PARAMS ARE INCLUDED WITHIN THE NEA

idx_toi_561 = np.where(df['pl_name'] == 'TOI-561 b')[0][0]

M_NEA[idx_toi_561], M_NEA_err_up[idx_toi_561], M_NEA_err_down[idx_toi_561] = 2.24, 0.20, 0.20
R_NEA[idx_toi_561], R_NEA_err_up[idx_toi_561], R_NEA_err_down[idx_toi_561] = 1.37, 0.04, 0.04

R_NEA_ERR = [(abs(R_NEA_err_down[i]), R_NEA_err_up[i]) for i in range(len(R_NEA))]
M_NEA_ERR = [(abs(M_NEA_err_down[i]), M_NEA_err_up[i]) for i in range(len(M_NEA))]

#@|TOI-561 b (Brinkman et al. 2023)
m_toi561_b, merr_toi561_b = 2.24, 0.20
r_toi561_b, rerr_toi561_b = 1.37, 0.04
met_toi561_b = -0.41
insol_toi561_b = 4383.42054422045 


# In[15]:


path_models = 'theoretical_models/'


# In[17]:


#@|Models from Zeng et al. (2016)

df_20_fe = pd.read_csv('theoretical_models/zeng_2016/20%_fe', sep = '\t', header = None)
m_20_fe, r_20_fe = df_20_fe[0].values, df_20_fe[1].values

#@|Models from Zeng et al. (2019)

#@|Earth-like, pure iron, and pure rock 
pure_iron_df = pd.read_csv('theoretical_models/zeng_2019/pure_iron', sep = "\t", header = None)
earth_like_df = pd.read_csv('theoretical_models/zeng_2019/earth_like', sep = "\t", header = None)
pure_rock_df = pd.read_csv('theoretical_models/zeng_2019/pure_rock', sep = "\t", header = None)

m_pure_iron, r_pure_iron = pure_iron_df[0].values,  pure_iron_df[1].values
m_earth_like, r_earth_like = earth_like_df[0].values,  earth_like_df[1].values
m_pure_rock, r_pure_rock = pure_rock_df[0].values,  pure_rock_df[1].values


#@|Hydrogen (H2) onto an Earth-like composition (at different temperatures)
h2_01_onto_earth_700K = pd.read_csv('theoretical_models/zeng_2019/0.1%_H2_onto_earth_like_700K', sep = "\t", header = None)
h2_03_onto_earth_700K = pd.read_csv('theoretical_models/zeng_2019/0.3%_H2_onto_earth_like_700K', sep = "\t", header = None)
h2_1_onto_earth_700K = pd.read_csv('theoretical_models/zeng_2019/1%_H2_onto_earth_like_700K', sep = "\t", header = None)
h2_2_onto_earth_700K = pd.read_csv('theoretical_models/zeng_2019/2%_H2_onto_earth_like_700K', sep = "\t", header = None)
h2_5_onto_earth_700K = pd.read_csv('theoretical_models/zeng_2019/5%_H2_onto_earth_like_700K', sep = "\t", header = None)

m_01_h2_onto_earth, r_01_h2_onto_earth = h2_01_onto_earth[0].values, h2_01_onto_earth[1].values
m_03_h2_onto_earth, r_03_h2_onto_earth = h2_03_onto_earth[0].values, h2_03_onto_earth[1].values
m_1_h2_onto_earth, r_1_h2_onto_earth = h2_1_onto_earth[0].values, h2_1_onto_earth[1].values

#@|100% H20 (at different temperatures)
h2o_100_300K = pd.read_csv('theoretical_models/zeng_2019/100%_h2o_300K', sep = "\t", header = None)
h2o_100_500K = pd.read_csv('theoretical_models/zeng_2019/100%_h2o_500K', sep = "\t", header = None)
h2o_100_700K = pd.read_csv('theoretical_models/zeng_2019/100%_h2o_700K', sep = "\t", header = None)
h2o_100_1000K = pd.read_csv('theoretical_models/zeng_2019/100%_h2o_1000K', sep = "\t", header = None)

m_100_h2o_300K, r_100_h2o_300K = h2o_100_300K[0].values, h2o_100_300K[1].values
m_100_h2o_500K, r_100_h2o_500K = h2o_100_500K[0].values, h2o_100_500K[1].values
m_100_h2o_700K, r_100_h2o_700K = h2o_100_700K[0].values, h2o_100_700K[1].values
m_100_h2o_1000K, r_100_h2o_1000K = h2o_100_1000K[0].values, h2o_100_1000K[1].values

#@|50% H20 (at different temperatures)

h2o_50_300K = pd.read_csv('theoretical_models/zeng_2019/50%_h2o_300K', sep = "\t", header = None)
h2o_50_500K = pd.read_csv('theoretical_models/zeng_2019/50%_h2o_500K', sep = "\t", header = None)
h2o_50_700K = pd.read_csv('theoretical_models/zeng_2019/50%_h2o_700K', sep = "\t", header = None)
h2o_50_1000K = pd.read_csv('theoretical_models/zeng_2019/50%_h2o_1000K', sep = "\t", header = None)

m_50_h2o_300K, r_50_h2o_300K = h2o_50_300K[0].values, h2o_50_300K[1].values
m_50_h2o_500K, r_50_h2o_500K = h2o_50_500K[0].values, h2o_50_500K[1].values
m_50_h2o_700K, r_50_h2o_700K = h2o_50_700K[0].values, h2o_50_700K[1].values
m_50_h2o_1000K, r_50_h2o_1000K = h2o_50_1000K[0].values, h2o_50_1000K[1].values


# In[ ]:





# In[18]:


plt.figure(figsize = (8, 6))
#@|plot config
s_my_planet = 200
s_NEA_planets = 120
zorder_lines = -1
lw_models = 2.5

#@|my planet(s)

plt.scatter(m_toi244_b, r_toi244_b,  s = s_my_planet, c = 'cyan', lw = 2, ec = "black", marker = "p")
plt.errorbar(m_toi244_b, r_toi244_b, xerr = merr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi244_b, r_toi244_b, yerr = rerr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

plt.scatter(m_toi4481_b, r_toi4481_b,  s = s_NEA_planets, c = 'grey', lw = 1.5, ec = "black")
plt.errorbar(m_toi4481_b, r_toi4481_b, xerr = merr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi4481_b, r_toi4481_b, yerr = rerr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

#@|NEA planets
plt.scatter(M_NEA, R_NEA, c = 'grey', s = s_NEA_planets, ec = "black", lw = 1.5)
#cbar.set_ticks_position('left')
plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)


#@|Models

#@|Volatiles (Zeng et al. 2019)
plt.plot(m_01_h2_onto_earth, r_01_h2_onto_earth, lw = lw_models, linestyle = "dashed" , zorder = -100, c = "lightblue", label = r'Earth + 0.1% $\rm H_{2}$' )
#plt.plot(m_100_h2o_700K, r_100_h2o_700K, c = "blue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'100% $\rm H_{2}O$')
plt.plot(m_50_h2o_700K, r_50_h2o_700K, c = "dodgerblue", zorder = zorder_lines, lw = lw_models, linestyle = "dashed", label = r'50% $\rm H_{2}O$ (50% $\rm MgSiO_{3})$')

#@|Solid structures (Zeng et al. (2016,2019))
plt.plot(m_pure_rock, r_pure_rock, lw = lw_models, linestyle = "dotted", zorder = zorder_lines, c = "orange", label = r'0% Fe (100% $\rm MgSiO_{3}$)')
plt.plot(m_20_fe, r_20_fe, lw = lw_models, linestyle = "dotted", zorder = -1000, c = "brown", label = r'20% Fe (80% $\rm MgSiO_{3}$)')
plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_models, label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_models, label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")


#@conf

import matplotlib.ticker as mticker
ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

from matplotlib.ticker import FormatStrFormatter
ax.yaxis.set_minor_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

ax.tick_params(axis='both', which='major', labelsize=12)
ax.tick_params(axis='both', which='minor', labelsize=12)

plt.ylabel(r'Planet Radius $\rm (R_{\odot})$', fontsize = 15)
plt.xlabel(r'Planet Mass $\rm (M_{\odot})$', fontsize = 15)


#@|small planets region (Rp < 4RE)
plt.xlim(0.5, 50)
plt.ylim(0.9,4)

#plt.ylim(4,15)

plt.legend(loc = "upper left", fontsize = 12)


# ### M-R diagram ([Fe/H] color coding)

# In[11]:


#@|metallicity limits for the color coding
met_min = -0.4
met_max = 0.0
#@|metallicity of my planet(s)
met_toi244 = -0.39
met_toi4481_b = -0.28 # Still not in the NEA (Palle et al. 2022)


# In[12]:


#@|metallicity from the NEA
met_NEA = df['st_met']


# In[13]:


#plt.figure(figsize = (8, 6))
plt.figure(figsize = (10, 6.5))
#@|plot config
s_my_planet = 200
s_NEA_planets = 120
zorder_lines = -100
lw_models = 2.5

#@|my planet(s)
#TOI-244
plt.scatter(m_toi244_b, r_toi244_b,  s = s_my_planet, c = 'white', cmap = 'rainbow', vmin = met_min, vmax = met_max, lw = 2, ec = "black", marker = "p")
plt.errorbar(m_toi244_b, r_toi244_b, xerr = merr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi244_b, r_toi244_b, yerr = rerr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

plt.scatter(m_toi4481_b, r_toi4481_b,  s = s_NEA_planets, c = met_toi4481_b, cmap = 'rainbow', vmin = met_min, vmax = met_max, lw = 1.5, ec = "black")
plt.errorbar(m_toi4481_b, r_toi4481_b, xerr = merr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi4481_b, r_toi4481_b, yerr = rerr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)



#@|NEA planets
plt.scatter(M_NEA, R_NEA, c = met_NEA, cmap = 'rainbow', s = s_NEA_planets, vmin = met_min, vmax = met_max, ec = "black", lw = 1.5)
cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
cbar.set_label(r'Star metallicity (dex)', fontsize = 12)
cbar.ax.tick_params(labelsize=10)
#cbar.set_ticks_position('left')
plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)


#@|Models
#@|Solid structures (Zeng et al. (2016,2019))
plt.plot(m_pure_rock, r_pure_rock, lw = lw_models, linestyle = "dotted", zorder = zorder_lines, c = "orange", label = r'0% Fe (100% $\rm MgSiO_{3}$)')
plt.plot(m_20_fe, r_20_fe, lw = lw_models, linestyle = "dotted", zorder = -1000, c = "brown", label = r'20% Fe (80% $\rm MgSiO_{3}$)')
plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_models, label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_models, label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")

#plt.plot(m_01_onto_earth, r_01_onto_earth, lw = lw_models, linestyle = "dashed" , zorder = -100, c = "lightblue", label = r'Earth + 0.1% $\rm H_{2}$' )
#plt.plot(m_100_h2o_700K, r_100_h2o_700K, c = "blue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'100% $\rm H_{2}O$')
#plt.plot(m_50_h2o_700K, r_50_h2o_700K, c = "dodgerblue", zorder = zorder_lines, lw = lw_models, linestyle = "dashed", label = r'50% $\rm H_{2}O$ (50% $\rm MgSiO_{3})$')



#@conf

import matplotlib.ticker as mticker
ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

from matplotlib.ticker import FormatStrFormatter
ax.yaxis.set_minor_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

ax.tick_params(axis='both', which='major', labelsize=14)
ax.tick_params(axis='both', which='minor', labelsize=14)

plt.ylabel(r'Planet Radius $\rm (R_{\odot})$', fontsize = 16)
plt.xlabel(r'Planet Mass $\rm (M_{\odot})$', fontsize = 16)



#plt.ylim(4,15)


#@|EXTRA
#@|Figure around the low-density super-Earths

x = [1.55, 1.58,  2., 2.5, 3.5, 2.6, 1.9]
y = [1.35, 1.5, 1.67, 1.68, 1.6, 1.38, 1.30]
#ax.scatter(x, y, zorder=3)

tck, u = interpolate.splprep([x + x[:1], y + y[:1]], s=0, per=True)
unew = np.linspace(0, 1, 100)
basic_form = interpolate.splev(unew, tck)
ax.plot(basic_form[0], basic_form[1], color='blue', lw=2,alpha = 0.7)
ax.fill(basic_form[0], basic_form[1], color='dodgerblue', alpha=0.2)

#@|Highlighting the names of the low-density super-Earths

#@| Planet names and arrows
lw_arrows = 1.5
#@|TOI-244
props = dict(boxstyle='round', facecolor='lavender', alpha=1, ec = "black" )
props_244 = dict(boxstyle='round', facecolor='lightgreen', alpha=1, lw = lw_arrows , ec = 'black')

plt.text(1.4, 1.75, "TOI-244 b", fontsize = 12,  weight='bold', bbox = props_244)
plt.arrow(2.1, 1.76, 0.35, -0.17, head_width = 0.04, head_length = 0.1, lw = lw_arrows , color = 'black')

plt.text(0.80, 1.58, "L 98-59 d", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.6, 0.35, -0.045, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.80, 1.43, "L 98-59 c", fontsize = 12,   bbox = props)
plt.arrow(1.38, 1.45, 0.65, -0.038, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.765, 1.30, "TOI-4481 b", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.315, 0.20, 0.008, head_width = 0.02, head_length = 0.07, lw = lw_arrows, color = 'k')

plt.text(2.2, 1.1, "TOI-561 b", fontsize = 12,   bbox = props)
plt.arrow(2.85, 1.13, -0.5, 0.195, head_width = 0.06, head_length = 0.04, lw = lw_arrows, color = 'k')

plt.text(2, 1.91, "HD 260655 c", fontsize = 12,   bbox = props)
plt.arrow(3.1, 1.87, 0, -0.23, head_width = 0.12, head_length = 0.04, lw = lw_arrows, color = 'k')


#@|small planets region (Rp < 4RE)
plt.xlim(0.5, 50)
plt.ylim(0.9,4)

plt.xlim(0.5, 21)
plt.ylim(0.9,2.8)



plt.legend(loc = "lower right", fontsize = 12)

plt.savefig('M-R_diagram_metallicity.pdf', bbox_inches = 'tight', pad_inches = 0.2)


# In[ ]:





# ### M-R diagram (Insolation color coding)

# In[14]:


#@|metallicity limits for the color coding
S_min = 0.0
S_max = 25.0
#@|metallicity of my planet(s)
insol_toi244 = 7.1
insol_toi4481_b = 130 # Still not in the NEA (Palle et al. 2022)


# In[15]:


S_NEA = df['pl_insol'].values


# In[16]:


#idxs_not_nan_S = np.where(~np.isnan(S_NEA))


# In[17]:


ii = np.where(df['pl_name']=='TOI-561 b')[0]
S_NEA[ii] = np.nan


# In[ ]:





# In[18]:


#@|inputs
M, R = 2.66, 1.5
WMFs = [0.003, 0.04, 0.08]
Core = ['earth', 'earth', 'earth']
colors_turbet = ['purple', 'magenta', 'plum']


# In[19]:


Cores_db = np.array(['earth', 'rock', 'iron'])            #@|Cores database
R_db = np.array([r_earth_like, r_pure_rock, r_pure_iron], dtype=object) #@|Corresponding radius database
M_db = np.array([m_earth_like, m_pure_rock, m_pure_iron], dtype=object) #@|Corresponding masses database


# In[20]:


R_Core, M_Core = [], []
for core in Core:
    idx = np.where(core==Cores_db)[0]
    R_Core.extend(R_db[idx])
    M_Core.extend(M_db[idx])


# In[21]:


for i,frac in enumerate(WMFs):
    frac


# In[ ]:





# In[22]:


#|Turbet et al. (2020) theoretical M-R models
from astropy.constants import G
import astropy.constants as const

R_pl_turb, M_pl_turb = [], []

for i,frac in enumerate(WMFs):
    
    r_core = R_Core[i]
    m_core = M_Core[i]
    

    #frac = 0.09
    #1 / (1/frac +1)


    R_cons,M_h20, Pt = 8.314, 1.8e-2, 0.1 # fixed
    g_core = G.value * m_core * const.M_earth.value / (r_core*const.R_earth.value)**2
    g = G.value * M * const.M_earth.value / (R*const.R_earth.value)**2

    alpha_1, alpha_2, alpha_3, alpha_4, alpha_5, alpha_6 = -3.550, 1.310, 1.099, 4.683e-1, 7.664e-1, 4.224e-1
    beta_1, beta_2, beta_3, beta_4, beta_5 = 2.846, 1.555e-1, 8.777e-2, 6.045e-2, 1.143e-2
    beta_6, beta_7, beta_8, beta_9, beta_10 = 1.736e-2, 1.859e-2, 4.314e-2, 3.393e-2, -1.034e-2

    R_s = 0.428
    Seff =  0.02277292940122454 * (28*R_s*const.R_sun.value / const.au.value )**-2

    X = (np.log10(frac)-alpha_1) / alpha_2
    Y = (np.log10(g)-alpha_3) / alpha_4
    Z = (np.log10(Seff)-alpha_5)/alpha_6

    X = (np.log10(frac)-alpha_1) / alpha_2
    Y = (np.log10(g)-alpha_3) / alpha_4
    Z = (np.log10(Seff)-alpha_5)/alpha_6

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
    
    R_pl_turb.append(r_pl)
    M_pl_turb.append(m_pl)


# In[ ]:





# In[76]:


#plt.figure(figsize = (8, 6))
plt.figure(figsize = (10, 6.5))
#@|plot config
s_my_planet = 200
s_NEA_planets = 120
zorder_lines = -100
lw_models = 2.5

#@|my planet(s)
#TOI-244
plt.scatter(m_toi244_b, r_toi244_b,  s = s_my_planet, c = insol_toi244, cmap = 'rainbow', vmin = S_min, vmax = S_max, lw = 2, ec = "black", marker = "p")
plt.errorbar(m_toi244_b, r_toi244_b, xerr = merr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi244_b, r_toi244_b, yerr = rerr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

plt.scatter(m_toi4481_b, r_toi4481_b,  s = s_NEA_planets, c = insol_toi4481_b, cmap = 'rainbow', vmin = S_min, vmax = S_max, lw = 1.5, ec = "black")
plt.errorbar(m_toi4481_b, r_toi4481_b, xerr = merr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi4481_b, r_toi4481_b, yerr = rerr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

plt.scatter(m_toi561_b, r_toi561_b,  s = s_NEA_planets, c = insol_toi561_b, cmap = 'rainbow', lw = 2,  vmin = S_min, vmax = S_max, ec = "black", zorder = -1000)
plt.errorbar(m_toi561_b, r_toi561_b, xerr = merr_toi561_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi561_b, r_toi561_b, yerr = rerr_toi561_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

#@|NEA planets
plt.scatter(M_NEA, R_NEA, c = S_NEA, cmap = 'rainbow', s = s_NEA_planets, vmin = S_min, vmax = S_max, ec = "black", lw = 1.5)
cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
#cbar.set_label(r'Star metallicity [dex]', fontsize = 12)
cbar.set_label(r'Insolation Flux $\rm (S_{\oplus})$', fontsize = 12)
cbar.ax.tick_params(labelsize=10)
#cbar.set_ticks_position('left')
plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)


#@|Models
#@|
plt.plot(m_01_h2_onto_earth, r_01_h2_onto_earth, lw = lw_models, linestyle = "dashed" , zorder = -100, c = "lightblue", label = r'Earth + 0.1% $\rm H_{2}$' )
#plt.plot(m_100_h2o_700K, r_100_h2o_700K, c = "blue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'100% $\rm H_{2}O$')
plt.plot(m_50_h2o_700K, r_50_h2o_700K, c = "dodgerblue", zorder = zorder_lines, lw = lw_models, linestyle = "dashed", label = r'50% $\rm H_{2}O$ (50% $\rm MgSiO_{3})$')

#@|Turbet et al. (2019)

for i in range(len(WMFs)):
    
    if Core[i] == 'earth':
        label_core = 'Earth'
    elif Core[i] == 'rock':
        label_core = 'Rock'
    elif Core[i] == 'iron':
        label_core = 'Iron'
        
    label_wmf = WMFs[i]
    
    plt.plot(M_pl_turb[i], R_pl_turb[i], lw = 3, linestyle = 'dotted',             zorder = -1000, c=colors_turbet[i], label = label_core + " + "+ str(label_wmf*100)+"% "+r'$\rm H_{2}O$ steam')

#@|Solid structures (Zeng et al. (2016,2019))
#plt.plot(m_pure_rock, r_pure_rock, lw = lw_models, linestyle = "dotted", zorder = zorder_lines, c = "orange", label = r'0% Fe (100% $\rm MgSiO_{3}$)')
#plt.plot(m_20_fe, r_20_fe, lw = lw_models, linestyle = "dotted", zorder = -1000, c = "brown", label = r'20% Fe (80% $\rm MgSiO_{3}$)')
plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_models, label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_models, label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")




#@conf

import matplotlib.ticker as mticker
ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

from matplotlib.ticker import FormatStrFormatter
ax.yaxis.set_minor_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

ax.tick_params(axis='both', which='major', labelsize=14)
ax.tick_params(axis='both', which='minor', labelsize=14)

plt.ylabel(r'Planet Radius $\rm (R_{\odot})$', fontsize = 16)
plt.xlabel(r'Planet Mass $\rm (M_{\odot})$', fontsize = 16)




#plt.ylim(4,15)


#@|EXTRA
#@|Figure around the low-density super-Earths

x = [1.55, 1.58,  2., 2.5, 3.5, 2.6, 1.9]
y = [1.35, 1.5, 1.67, 1.68, 1.6, 1.38, 1.30]
#ax.scatter(x, y, zorder=3)

tck, u = interpolate.splprep([x + x[:1], y + y[:1]], s=0, per=True)
unew = np.linspace(0, 1, 100)
basic_form = interpolate.splev(unew, tck)
ax.plot(basic_form[0], basic_form[1], color='blue', lw=2,alpha = 0.7)
ax.fill(basic_form[0], basic_form[1], color='dodgerblue', alpha=0.2)

#@|Highlighting the names of the low-density super-Earths

#@| Planet names and arrows
lw_arrows = 1.5
#@|TOI-244
props = dict(boxstyle='round', facecolor='lavender', alpha=1, ec = "black" )
props_244 = dict(boxstyle='round', facecolor='lightgreen', alpha=1, lw = lw_arrows , ec = 'black')

plt.text(1.4, 1.75, "TOI-244 b", fontsize = 12,  weight='bold', bbox = props_244)
plt.arrow(2.1, 1.76, 0.35, -0.17, head_width = 0.04, head_length = 0.1, lw = lw_arrows , color = 'black')

plt.text(0.80, 1.58, "L 98-59 d", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.6, 0.35, -0.045, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.80, 1.43, "L 98-59 c", fontsize = 12,   bbox = props)
plt.arrow(1.38, 1.45, 0.65, -0.038, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.765, 1.30, "TOI-4481 b", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.315, 0.20, 0.008, head_width = 0.02, head_length = 0.07, lw = lw_arrows, color = 'k')

plt.text(2.2, 1.1, "TOI-561 b", fontsize = 12,   bbox = props)
plt.arrow(2.85, 1.13, -0.5, 0.195, head_width = 0.06, head_length = 0.04, lw = lw_arrows, color = 'k')

plt.text(2, 1.91, "HD 260655 c", fontsize = 12,   bbox = props)
plt.arrow(3.1, 1.87, 0, -0.23, head_width = 0.12, head_length = 0.04, lw = lw_arrows, color = 'k')




plt.legend(loc = "lower right", fontsize = 11)

#@|small planets region (Rp < 4RE)
plt.xlim(0.5, 50)
plt.ylim(0.9,4)

plt.xlim(0.5, 21)
plt.ylim(0.9,2.8)


plt.savefig('M-R_diagram_insolation.pdf', bbox_inches = 'tight', pad_inches = 0.2)


# In[77]:


#@|ALL ----------------------------


# In[162]:


models = ['zeng_2019_standard']
models = ['zeng_2019_earth_like', 'zeng_2019_pure_rock', 'zeng_2019_pure_iron',           'zeng_2019_0.1%_H2_onto_earth_like_700K','zeng_2019_0.1%_H2_onto_earth_like_300K',          'zeng_2019_0.1%_H2_onto_earth_like_500K',  'zeng_2019_0.1%_H2_onto_earth_like_1000K',           'zeng_2019_0.1%_H2_onto_earth_like_2000K']
color_coding = 'none'
color_min = -0.4
color_max = 0.0
log_x = True
log_y = True


# In[163]:


models_dic_colors = {'zeng_2019_pure_iron':'black', 'zeng_2019_earth_like': 'red', 'zeng_2019_pure_rock': 'orange',                    'zeng_2019_0.1%_H2_onto_earth_like_300K': 'darkslateblue',                    'zeng_2019_0.3%_H2_onto_earth_like_300K':'mediumslateblue',                    'zeng_2019_1%_H2_onto_earth_like_300K': 'mediumpurple',                    'zeng_2019_2%_H2_onto_earth_like_300K': 'rebeccapurple',                    'zeng_2019_5%_H2_onto_earth_like_300K': 'blueviolet',                    'zeng_2019_0.1%_H2_onto_earth_like_500K': 'indigo',                    'zeng_2019_0.3%_H2_onto_earth_like_500K': 'darkorchid',                    'zeng_2019_1%_H2_onto_earth_like_500K': 'darkviolet',                    'zeng_2019_2%_H2_onto_earth_like_500K': 'mediumorchid',                    'zeng_2019_5%_H2_onto_earth_like_500K': 'thistle',                    'zeng_2019_0.1%_H2_onto_earth_like_700K': 'plum',                    'zeng_2019_0.3%_H2_onto_earth_like_700K': 'violet',                    'zeng_2019_1%_H2_onto_earth_like_700K': 'purple',                    'zeng_2019_2%_H2_onto_earth_like_700K': 'darkmagenta',                    'zeng_2019_5%_H2_onto_earth_like_700K': 'fuchsia',                    'zeng_2019_0.1%_H2_onto_earth_like_1000K': 'magenta',                    'zeng_2019_0.3%_H2_onto_earth_like_1000K': 'orchid',                    'zeng_2019_1%_H2_onto_earth_like_1000K': 'mediumvioletred',                    'zeng_2019_2%_H2_onto_earth_like_1000K': 'deepping',                    'zeng_2019_5%_H2_onto_earth_like_1000K': 'hotpink',                    'zeng_2019_0.1%_H2_onto_earth_like_2000K': 'lavenderblush',                    'zeng_2019_0.3%_H2_onto_earth_like_2000K': 'palevioletred',                    'zeng_2019_1%_H2_onto_earth_like_2000K': 'crimson',                    'zeng_2019_2%_H2_onto_earth_like_2000K': 'pink',                    'zeng_2019_5%_H2_onto_earth_like_2000K': 'lightpink'
                    }
models_dic_labels = {'zeng_2019_pure_iron':r'100% Fe (0% $\rm MgSiO_{3}$)',                    'zeng_2019_earth_like': r'33% Fe (66% $\rm MgSiO_{3}$)',                    'zeng_2019_pure_rock': r'0% Fe (100% $\rm MgSiO_{3}$)',                    'zeng_2019_0.1%_H2_onto_earth_like_300K': r'Earth + 0.1% $\rm H_{2}$ (300K)',                    'zeng_2019_0.3%_H2_onto_earth_like_300K': r'Earth + 0.1% $\rm H_{2}$ (300K)',                    'zeng_2019_1%_H2_onto_earth_like_300K': r'Earth + 0.1% $\rm H_{2}$ (300K)',                    'zeng_2019_2%_H2_onto_earth_like_300K': r'Earth + 0.1% $\rm H_{2}$ (300K)',                    'zeng_2019_5%_H2_onto_earth_like_300K': r'Earth + 0.1% $\rm H_{2}$ (300K)',                    'zeng_2019_0.1%_H2_onto_earth_like_500K': r'Earth + 0.1% $\rm H_{2}$ (500K)',                    'zeng_2019_0.3%_H2_onto_earth_like_500K': r'Earth + 0.1% $\rm H_{2}$ (500K)',                    'zeng_2019_1%_H2_onto_earth_like_500K': r'Earth + 0.1% $\rm H_{2}$ (500K)',                    'zeng_2019_2%_H2_onto_earth_like_500K': r'Earth + 0.1% $\rm H_{2}$ (500K)',                    'zeng_2019_5%_H2_onto_earth_like_500K': r'Earth + 0.1% $\rm H_{2}$ (500K)',                    'zeng_2019_0.1%_H2_onto_earth_like_700K': r'Earth + 0.1% $\rm H_{2}$ (700K)',                    'zeng_2019_0.3%_H2_onto_earth_like_700K': r'Earth + 0.1% $\rm H_{2}$ (700K)',                    'zeng_2019_1%_H2_onto_earth_like_700K': r'Earth + 0.1% $\rm H_{2}$ (700K)',                    'zeng_2019_2%_H2_onto_earth_like_700K': r'Earth + 0.1% $\rm H_{2}$ (700K)',                    'zeng_2019_5%_H2_onto_earth_like_700K': r'Earth + 0.1% $\rm H_{2}$ (700K)',                    'zeng_2019_0.1%_H2_onto_earth_like_1000K': r'Earth + 0.1% $\rm H_{2}$ (1000K)',                    'zeng_2019_0.3%_H2_onto_earth_like_1000K': r'Earth + 0.1% $\rm H_{2}$ (1000K)',                    'zeng_2019_1%_H2_onto_earth_like_1000K': r'Earth + 0.1% $\rm H_{2}$ (1000K)',                    'zeng_2019_2%_H2_onto_earth_like_1000K': r'Earth + 0.1% $\rm H_{2}$ (1000K)',                    'zeng_2019_5%_H2_onto_earth_like_1000K': r'Earth + 0.1% $\rm H_{2}$ (1000K)',                    'zeng_2019_0.1%_H2_onto_earth_like_2000K': r'Earth + 0.1% $\rm H_{2}$ (2000K)',                    'zeng_2019_0.3%_H2_onto_earth_like_2000K': r'Earth + 0.1% $\rm H_{2}$ (2000K)',                    'zeng_2019_1%_H2_onto_earth_like_2000K': r'Earth + 0.1% $\rm H_{2}$ (2000K)',                    'zeng_2019_2%_H2_onto_earth_like_2000K': r'Earth + 0.1% $\rm H_{2}$ (2000K)',                    'zeng_2019_5%_H2_onto_earth_like_2000K': r'Earth + 0.1% $\rm H_{2}$ (2000K)',                    }


# In[164]:


color_codings = np.array(['pl_insol', 'st_met'])
color_codings_label = np.array([r'Insolation Flux $\rm (S_{\oplus})$', r'Star metallicity (dex)'])


# In[165]:


color_codings


# In[ ]:





# if color_coding == 'st_met':
#     plt.figure(figsize = (10, 6.56))
#     #@|NEA planets
#     plt.scatter(M_NEA, R_NEA, c = met_NEA, cmap = 'rainbow', s = s_NEA_planets, vmin = met_min, vmax = met_max, ec = "black", lw = 1.5)
#     cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
#     cbar.set_label(r'Star metallicity [dex]', fontsize = 12)
#     cbar.ax.tick_params(labelsize=10)
#     #cbar.set_ticks_position('left')
#     plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)
#     
# 
# if color_coding == 'pl_insol':
#     plt.figure(figsize = (10, 6.56))
#     #@|NEA planets
#     plt.scatter(M_NEA, R_NEA, c = S_NEA, cmap = 'rainbow', s = s_NEA_planets, vmin = S_min, vmax = S_max, ec = "black", lw = 1.5)
#     cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
#     #cbar.set_label(r'Star metallicity [dex]', fontsize = 12)
#     cbar.set_label(r'Insolation Flux $\rm (S_{\oplus})$', fontsize = 12)
#     cbar.ax.tick_params(labelsize=10)
#     #cbar.set_ticks_position('left')
#     plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)
# 

# In[168]:


#plt.figure(figsize = (8, 6))
#@|plot config
s_my_planet = 200
s_NEA_planets = 120
zorder_lines = -100
lw_models = 2.5


if color_coding in df_cols:
    plt.figure(figsize = (10, 6.56))
    #idx_color = np.where(df_cols==color_coding)[0]
    #@|NEA planets
    plt.scatter(M_NEA, R_NEA, c = df[color_coding].values, cmap = 'rainbow', s = s_NEA_planets, vmin = color_min, vmax = color_max, ec = "black", lw = 1.5)
    cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
    cbar.set_label(color_codings_label[np.where(color_codings == color_coding)[0]][0], fontsize = 12)
    cbar.ax.tick_params(labelsize=10)
    #cbar.set_ticks_position('left')
    plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)
    



if color_coding == 'none':
    plt.figure(figsize = (8, 7))
    #f plot_size = 'twocols':
        
    #@|NEA planets
    plt.scatter(M_NEA, R_NEA, c = 'grey', s = s_NEA_planets, ec = "black", lw = 1.5)
    plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)


    

#@|theoretical models
for model in models:
    plt.plot(pd.read_csv(path_models+model,  sep = '\t', header = None)[0],             pd.read_csv(path_models+model,  sep = '\t', header = None)[1], lw = lw_models, linestyle = "dashed" ,             zorder = -100, c = models_dic_colors[model], label =  models_dic_labels[model] )
    
    
    


    
    
#@conf

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

    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=16)

    plt.ylabel(r'Planet Radius $\rm (R_{\odot})$', fontsize = 18)
    plt.xlabel(r'Planet Mass $\rm (M_{\odot})$', fontsize = 18)    
    
else:
    
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=14)

    plt.ylabel(r'Planet Radius $\rm (R_{\odot})$', fontsize = 16)
    plt.xlabel(r'Planet Mass $\rm (M_{\odot})$', fontsize = 16)   
    
    

    
#@|small planets region (Rp < 4RE)
plt.xlim(0.5, 50)
plt.ylim(0.9,4)

plt.xlim(0.5, 21)
plt.ylim(0.9,2.8)


plt.legend(loc = "lower right", fontsize = 11)

plt.savefig('M-R_met.pdf', bbox_inches = 'tight', pad_inches = 0.2)


# In[ ]:


if 'zeng_2019_standard' in models:
    
    plt.plot(m_01_h2_onto_earth, r_01_h2_onto_earth, lw = lw_models, linestyle = "dashed" ,             zorder = -100, c = "lightblue", label = r'Earth + 0.1% $\rm H_{2}$' )
    #plt.plot(m_100_h2o_700K, r_100_h2o_700K, c = "blue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'100% $\rm H_{2}O$')
    plt.plot(m_50_h2o_700K, r_50_h2o_700K, c = "dodgerblue", zorder = zorder_lines, lw = lw_models,              linestyle = "dashed", label = r'50% $\rm H_{2}O$ (50% $\rm MgSiO_{3})$')

    plt.plot(m_pure_rock, r_pure_rock, lw = lw_models, linestyle = "dashed", zorder = zorder_lines,              c = "orange", label = r'0% Fe (100% $\rm MgSiO_{3}$)')
    plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_models,             label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
    plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_models,              label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")


    
    
if '0.3%_H2_onto_earth_like' in models:
    print("AF")
    plt.plot(m_03_h2_onto_earth, r_03_h2_onto_earth, lw = lw_models, linestyle = "dashed" ,             zorder = -100, c = "blue", label = r'Earth + 0.3% $\rm H_{2}$' )
if '0.1%_H2_onto_earth_like' in models:
    plt.plot(m_01_h2_onto_earth, r_01_h2_onto_earth, lw = lw_models, linestyle = "dashed" ,             zorder = -100, c = "lightblue", label = r'Earth + 0.1% $\rm H_{2}$' )
    
    
    
if 'pure_iron_zeng_2019' in models:
    plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_models,             label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")
if 'earth_like_zeng_2019' in models:
    plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_models,             label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
if 'pure_rock_zeng_2019' in models:
    plt.plot(m_pure_rock, r_pure_rock, lw = lw_models, linestyle = "dashed", zorder = zorder_lines,              c = "orange", label = r'0% Fe (100% $\rm MgSiO_{3}$)')
    


# In[35]:


###############
#END
###############


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:







#plt.figure(figsize = (8, 6))
plt.figure(figsize = (10, 6))
#@|plot config
s_my_planet = 200
s_NEA_planets = 120
zorder_lines = -100
lw_models = 2.5

#@|my planet(s)
#TOI-244
plt.scatter(m_toi244_b, r_toi244_b,  s = s_my_planet, c = insol_toi244, cmap = 'rainbow', vmin = S_min, vmax = S_max, lw = 2, ec = "black", marker = "p")
plt.errorbar(m_toi244_b, r_toi244_b, xerr = merr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi244_b, r_toi244_b, yerr = rerr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

plt.scatter(m_toi4481_b, r_toi4481_b,  s = s_NEA_planets, c = insol_toi4481_b, cmap = 'rainbow', vmin = S_min, vmax = S_max, lw = 1.5, ec = "black")
plt.errorbar(m_toi4481_b, r_toi4481_b, xerr = merr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi4481_b, r_toi4481_b, yerr = rerr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

plt.scatter(m_toi561_b, r_toi561_b,  s = s_NEA_planets, c = insol_toi561_b, cmap = 'rainbow', lw = 2,  vmin = S_min, vmax = S_max, ec = "black", zorder = -1000)
plt.errorbar(m_toi561_b, r_toi561_b, xerr = merr_toi561_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
plt.errorbar(m_toi561_b, r_toi561_b, yerr = rerr_toi561_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)

#@|NEA planets
plt.scatter(M_NEA, R_NEA, c = S_NEA, cmap = 'rainbow', s = s_NEA_planets, vmin = S_min, vmax = S_max, ec = "black", lw = 1.5)
cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
#cbar.set_label(r'Star metallicity [dex]', fontsize = 12)
cbar.set_label(r'Insolation Flux $\rm [S_{\oplus}]$', fontsize = 12)
cbar.ax.tick_params(labelsize=10)
#cbar.set_ticks_position('left')
plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)


#@|Models
#@|
plt.plot(m_01_h2_onto_earth, r_01_h2_onto_earth, lw = lw_models, linestyle = "dashed" , zorder = -100, c = "lightblue", label = r'Earth + 0.1% $\rm H_{2}$' )
#plt.plot(m_100_h2o_700K, r_100_h2o_700K, c = "blue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'100% $\rm H_{2}O$')
plt.plot(m_50_h2o_700K, r_50_h2o_700K, c = "dodgerblue", zorder = zorder_lines, lw = lw_models, linestyle = "dashed", label = r'50% $\rm H_{2}O$ (50% $\rm MgSiO_{3})$')

#@|Turbet et al. (2019)

for i in range(len(WMFs)):
    
    if Core[i] == 'earth':
        label_core = 'Earth'
    elif Core[i] == 'rock':
        label_core = 'Rock'
    elif Core[i] == 'iron':
        label_core = 'Iron'
        
    label_wmf = WMFs[i]
    
    plt.plot(M_pl_turb[i], R_pl_turb[i], lw = 3, linestyle = 'dotted',             zorder = -1000, c=colors_turbet[i], label = label_core + " + "+ str(label_wmf*100)+"% "+r'$\rm H_{2}O$ steam')

#@|Solid structures (Zeng et al. (2016,2019))
#plt.plot(m_pure_rock, r_pure_rock, lw = lw_models, linestyle = "dotted", zorder = zorder_lines, c = "orange", label = r'0% Fe (100% $\rm MgSiO_{3}$)')
#plt.plot(m_20_fe, r_20_fe, lw = lw_models, linestyle = "dotted", zorder = -1000, c = "brown", label = r'20% Fe (80% $\rm MgSiO_{3}$)')
plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_models, label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_models, label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")




#@conf

import matplotlib.ticker as mticker
ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

from matplotlib.ticker import FormatStrFormatter
ax.yaxis.set_minor_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

ax.tick_params(axis='both', which='major', labelsize=12)
ax.tick_params(axis='both', which='minor', labelsize=12)

plt.ylabel(r'Planet Radius $\rm [R_{\odot}]$', fontsize = 15)
plt.xlabel(r'Planet Mass $\rm [M_{\odot}]$', fontsize = 15)




#plt.ylim(4,15)


#@|EXTRA
#@|Figure around the low-density super-Earths

x = [1.55, 1.58,  2., 2.5, 3.5, 2.6, 1.9]
y = [1.35, 1.5, 1.67, 1.68, 1.6, 1.38, 1.30]
#ax.scatter(x, y, zorder=3)

tck, u = interpolate.splprep([x + x[:1], y + y[:1]], s=0, per=True)
unew = np.linspace(0, 1, 100)
basic_form = interpolate.splev(unew, tck)
ax.plot(basic_form[0], basic_form[1], color='blue', lw=2,alpha = 0.7)
ax.fill(basic_form[0], basic_form[1], color='dodgerblue', alpha=0.2)

#@|Highlighting the names of the low-density super-Earths

#@| Planet names and arrows
lw_arrows = 1.5
#@|TOI-244
props = dict(boxstyle='round', facecolor='lavender', alpha=1, ec = "black" )
props_244 = dict(boxstyle='round', facecolor='lightgreen', alpha=1, lw = lw_arrows , ec = 'black')

plt.text(1.4, 1.75, "TOI-244 b", fontsize = 12,  weight='bold', bbox = props_244)
plt.arrow(2.1, 1.76, 0.35, -0.17, head_width = 0.04, head_length = 0.1, lw = lw_arrows , color = 'black')

plt.text(0.80, 1.58, "L 98-59 d", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.6, 0.35, -0.045, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.80, 1.43, "L 98-59 c", fontsize = 12,   bbox = props)
plt.arrow(1.38, 1.45, 0.65, -0.038, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.765, 1.30, "TOI-4481 b", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.315, 0.20, 0.008, head_width = 0.02, head_length = 0.07, lw = lw_arrows, color = 'k')

plt.text(2.2, 1.1, "TOI-561 b", fontsize = 12,   bbox = props)
plt.arrow(2.85, 1.13, -0.5, 0.195, head_width = 0.06, head_length = 0.04, lw = lw_arrows, color = 'k')

plt.text(2, 1.91, "HD 260655 c", fontsize = 12,   bbox = props)
plt.arrow(3.1, 1.87, 0, -0.23, head_width = 0.12, head_length = 0.04, lw = lw_arrows, color = 'k')




plt.legend(loc = "lower right", fontsize = 11)

#@|small planets region (Rp < 4RE)
plt.xlim(0.5, 50)
plt.ylim(0.9,4)

plt.xlim(0.5, 21)
plt.ylim(0.9,2.8)

plt.savefig('M-R_diagram_insolation.pdf', bbox_inches = 'tight')


# In[ ]:


###############################33


# In[ ]:


R_NEA = df['pl_rade'].values[idxs_e]
M_NEA = df['pl_bmasse'].values[idxs_e]
Teff_NEA = df['st_teff'].values[idxs_e]

R_NEA_UP = df['pl_radeerr1'].values[idxs_e]
R_NEA_DOWN = df['pl_radeerr2'].values[idxs_e]

M_NEA_UP = df['pl_bmasseerr1'].values[idxs_e]
M_NEA_DOWN = df['pl_bmasseerr2'].values[idxs_e]

Teq = df['pl_insol'].values[idxs_e]
Teq_err_up = df['pl_insolerr1'].values[idxs_e]
Teq_err_down = df['pl_insolerr2'].values[idxs_e]

met = df['st_met'].values[idxs_e]
met_err_up = df['st_meterr1'].values[idxs_e]
met_err_down = df['st_meterr2'].values[idxs_e]

names = df['pl_name'].values[idxs_e]

RS_NEA = df['st_rad'].values[idxs_e]
Teff_NEA = df['st_teff'].values[idxs_e]
a_NEA = df['pl_orbsmax'].values[idxs_e]

RS_NEA_ERR = df['st_raderr1'].values[idxs_e]
Teff_NEA_ERR = df['st_tefferr1'].values[idxs_e]
a_NEA_ERR = df['pl_orbsmaxerr1'].values[idxs_e]


#@|#@|#|
idxs_not_nan_teff = np.where(~np.isnan(met))
idxs_not_nan_met = np.where(~np.isnan(met))



if color_scale == 'met':
    R_NEA = R_NEA[idxs_not_nan_met]
    M_NEA = M_NEA[idxs_not_nan_met]
    R_NEA_UP = R_NEA_UP[idxs_not_nan_met]
    R_NEA_DOWN = R_NEA_DOWN[idxs_not_nan_met]
    M_NEA_UP = M_NEA_UP[idxs_not_nan_met]
    M_NEA_DOWN = M_NEA_DOWN[idxs_not_nan_met]
    Teff_NEA = Teff_NEA[idxs_not_nan_met]
    df = df.iloc[idxs_not_nan_met]
    
    names = names[idxs_not_nan_met]
    
if color_scale == 'Teq':
    
    R_NEA = R_NEA[idxs_not_nan_teff]
    M_NEA = M_NEA[idxs_not_nan_teff]
    R_NEA_UP = R_NEA_UP[idxs_not_nan_teff]
    R_NEA_DOWN = R_NEA_DOWN[idxs_not_nan_teff]
    M_NEA_UP = M_NEA_UP[idxs_not_nan_teff]
    M_NEA_DOWN = M_NEA_DOWN[idxs_not_nan_teff]
    Teff_NEA = Teff_NEA[idxs_not_nan_teff]
    
    names = names[idxs_not_nan_teff]
    
    RS_NEA = RS_NEA[idxs_not_nan_teff]
    a_NEA = a_NEA[idxs_not_nan_teff]
    
    RS_NEA_ERR = RS_NEA_ERR[idxs_not_nan_teff]
    Teff_NEA_ERR = Teff_NEA_ERR[idxs_not_nan_teff]
    a_NEA_ERR = a_NEA_ERR[idxs_not_nan_teff]
    

Teq = Teq[idxs_not_nan_teff]
Teq_err_up= Teq_err_up[idxs_not_nan_met]
Teq_err_down= Teq_err_down[idxs_not_nan_met]

met = met[idxs_not_nan_met]
met_err_up= met_err_up[idxs_not_nan_met]
met_err_down= met_err_down[idxs_not_nan_met]


R_NEA_ERR = [(abs(R_NEA_DOWN[i]), R_NEA_UP[i]) for i in range(len(R_NEA_UP))]
M_NEA_ERR = [(abs(M_NEA_DOWN[i]), M_NEA_UP[i]) for i in range(len(M_NEA_UP))]
#met_err = [(abs(met_err_up[i]), met_err_down[i]) for i in range(len(met_err_up))]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#!pip install branca


# In[ ]:


#@|extra planets (not in the NEA)

#@|TOI-244 b
m_toi244_b, merr_toi244_b = 2.66, 0.31
r_toi244_b, rerr_toi244_b = 1.52, 0.11
met_toi244_b, insol_toi244_b = -0.39, 7.1

#@|TOI-561 b (Brinkman et al. 2023)
m_toi561_b, merr_toi561_b = 2.24, 0.20
r_toi561_b, rerr_toi561_b = 1.37, 0.04
met_toi561_b = -0.41
insol_toi561_b = 4383.42054422045 

#@|TOI-4481 b (Palle et al. 2022)
m_toi4481_b, merr_toi4481_b = 1.90, 0.17
r_toi4481_b, rerr_toi4481_b = 1.331, 0.023
met_toi4481_b = -0.28
insol_toi4481_b = 130


# In[ ]:





# In[ ]:


zorder_lines = -100
lw_lines = 2.5
fig = plt.figure(figsize = (10, 6))



#@|H2 atmosphere onto earth-like

#plt.plot(m_01_onto_earth, r_01_onto_earth, lw = lw_lines, linestyle = "dashed" , zorder = -100, c = "lightblue", label = r'0.1% $\rm H_{2}$' )

#@|100% H2O
#plt.plot(m_100_h2o_700K, r_100_h2o_700K, c = "blue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'100% $\rm H_{2}O$')

#@|50% H2O
#plt.plot(m_50_h2o_700K, r_50_h2o_700K, c = "dodgerblue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'50% $\rm H_{2}O$')

#plt.plot(m_pure_rock, r_pure_rock, c = "red")
#plt.xscale('log')
#plt.yscale('log')
#plt.xlim(0.6, 50)
#plt.ylim(0.8, 4.5)

#color_scale = 'Teq'

if color_scale == 'Teq':
    values = Teq
    vmin, vmax = 0, 25
    
    plt.plot(m_01_onto_earth, r_01_onto_earth, lw = lw_lines, linestyle = "dashed" , zorder = -100, c = "lightblue", label = r'Earth + 0.1% $\rm H_{2}$' )
    #plt.plot(m_100_h2o_700K, r_100_h2o_700K, c = "blue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'100% $\rm H_{2}O$')
    plt.plot(m_50_h2o_700K, r_50_h2o_700K, c = "dodgerblue", zorder = zorder_lines, lw = lw_lines, linestyle = "dashed", label = r'50% $\rm H_{2}O$ (50% $\rm MgSiO_{3})$')

    plt.plot(m_new_90, r_new_90, c = "purple", lw = 3, linestyle = 'dotted', zorder = -1000, label = r'Earth + 9% $\rm H_{2}O$ steam')
    plt.plot(m_new_40, r_new_40, c = "magenta", lw = 3, linestyle = 'dotted', zorder = -1000, label = r'Earth + 4% $\rm H_{2}O$ steam')
    plt.plot(m_new_3, r_new_3, c = "plum", lw = 3, linestyle = 'dotted', zorder = -1000, label = r'Earth + 0.3% $\rm H_{2}O$ steam')
    
    
    plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_lines, label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
    plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_lines, label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")
    
    
    #@|extra planets
    #@|TOI-244 b 
    points = plt.scatter(m_toi244_b, r_toi244_b,  s = 140, c = insol_toi244_b, cmap = 'rainbow', lw = 2,  vmin = vmin, vmax = vmax, ec = "black", marker = "p")
    plt.errorbar(m_toi244_b, r_toi244_b, xerr = merr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    plt.errorbar(m_toi244_b, r_toi244_b, yerr = rerr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    #@|TOI-561 b
    points = plt.scatter(m_toi561_b, r_toi561_b,  s = 60, c = insol_toi561_b, cmap = 'rainbow', lw = 2,  vmin = vmin, vmax = vmax, ec = "black")
    plt.errorbar(m_toi561_b, r_toi561_b, xerr = merr_toi561_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    plt.errorbar(m_toi561_b, r_toi561_b, yerr = rerr_toi561_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    #@|TOI-4481 b
    points = plt.scatter(m_toi4481_b, r_toi4481_b,  s = 60, c = insol_toi4481_b, cmap = 'rainbow', lw = 2,  vmin = vmin, vmax = vmax, ec = "black")
    plt.errorbar(m_toi4481_b, r_toi4481_b, xerr = merr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    plt.errorbar(m_toi4481_b, r_toi4481_b, yerr = rerr_toi4481_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    
    
    
    
if color_scale == 'met':
    values = met
    #@-----------------
    vmin, vmax= -0.4, 0
    
    plt.plot(m_0_fe, r_0_fe, lw = lw_lines, linestyle = "dotted", zorder = -1000, c = "orange", label = r'0% Fe (100% $\rm MgSiO_{3}$)')
    plt.plot(m_20_fe, r_20_fe, lw = lw_lines, linestyle = "dotted", zorder = -1000, c = "brown", label = r'20% Fe (80% $\rm MgSiO_{3}$)')
    plt.plot(m_earth_like, r_earth_like, c = "red", zorder = zorder_lines, lw = lw_lines, label = r'33% Fe (66% $\rm MgSiO_{3}$)', linestyle = "dashed")
    plt.plot(m_pure_iron, r_pure_iron, c = "black", zorder = zorder_lines, lw = lw_lines, label = r'100% Fe (0% $\rm MgSiO_{3}$)', linestyle = "dashed")
    
    #@|extra planets
    #@|TOI-244 b 
    #points = plt.scatter(m_toi244_b, r_toi244_b,  s = 160, c = met_toi244_b, cmap = 'rainbow', lw = 2,  vmin = vmin, vmax = vmax, ec = "black", marker = "p")
    points = plt.scatter(m_toi244_b, r_toi244_b,  s = 140, c = 'white', lw = 2, ec = "black", marker = "p")
    plt.errorbar(m_toi244_b, r_toi244_b, xerr = merr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    plt.errorbar(m_toi244_b, r_toi244_b, yerr = rerr_toi244_b, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    #@|TOI-561 b
    points = plt.scatter(m_toi561_b, r_toi561_b,  s = 60, c = met_toi561_b, cmap = 'rainbow', lw = 2,  vmin = vmin, vmax = vmax, ec = "black")
    plt.errorbar(m_toi561_b, r_toi561_b, xerr = merr_toi561_b*3, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    plt.errorbar(m_toi561_b, r_toi561_b, yerr = rerr_toi561_b*3, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    #@|TOI-4481 b
    points = plt.scatter(m_toi4481_b, r_toi4481_b,  s = 60, c = met_toi4481_b, cmap = 'rainbow', lw = 2,  vmin = vmin, vmax = vmax, ec = "black")
    plt.errorbar(m_toi4481_b, r_toi4481_b, xerr = merr_toi4481_b*3, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    plt.errorbar(m_toi4481_b, r_toi4481_b, yerr = rerr_toi4481_b*3, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
    

    
    
#@|my planet
#points = plt.scatter(M, R,  s = 160, c = value_244, cmap = 'rainbow', lw = 2,  vmin = vmin, vmax = vmax, ec = "black", marker = "p")
#plt.errorbar(M, R, xerr = M_err, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
#plt.errorbar(M, R, yerr = R_err, c = 'black', zorder = -0.5, lw = 2, capsize = 2)
#@|other planets not NEA



#@|NEA planets
plt.scatter(M_NEA, R_NEA, c = values, cmap = 'rainbow', s = 60, vmin = vmin, vmax = vmax, ec = "black", lw = 1.5)
cbar = plt.colorbar(location = 'left', anchor=(2.95,0.95), aspect = 8, shrink=0.4)
if color_scale == 'met':
    cbar.set_label(r'Star metallicity [Fe/H]', fontsize = 12)
if color_scale == 'Teq':
    cbar.set_label(r'Insolation Flux $\rm (S_{\oplus})$', fontsize = 12)
cbar.ax.tick_params(labelsize=10)
#cbar.set_ticks_position('left')
plt.errorbar(M_NEA, R_NEA, yerr = np.array(R_NEA_ERR).T, xerr = np.array(M_NEA_ERR).T, linestyle = "None", ecolor = 'black', zorder = -1, lw = 2, capsize = 2)


#plt.ticklabel_format(style='plain')


#convert time to a color tuple using the 'rainbow' used for scatter
#import matplotlib
#import matplotlib.cm as cm
#norm = matplotlib.colors.Normalize(vmin=np.nanmin(300), vmax=np.nanmax(1000), clip=True)
#mapper = cm.ScalarMappable(norm=norm, cmap='magma')
#time_color = np.array([(mapper.to_rgba(v)) for v in Teq])

#for x, y, e, color in zip(M_NEA, R_NEA, R_NEA_UP, time_color):
    #plt.scatter(x, y, color=color, s = 160,  cmap = 'magma', vmin=np.nanmin(300), vmax=np.nanmax(1000))
    #plt.errorbar(x, y, e, lw=3, capsize=2, color=color)




#plt.xscale('log')
#plt.yscale('log')



#plt.xlim(1.5, 2.6)
#plt.ylim(1.3, 2)

#plt.xticks(np.array([1, 2, 10]))

#ax.xaxis.set_minor_formatter(mticker.ScalarFormatter())
#ax.ticklabel_format(style='plain', axis='x')
import matplotlib.ticker as mticker
ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

from matplotlib.ticker import FormatStrFormatter
ax.yaxis.set_minor_formatter(FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

ax.tick_params(axis='both', which='major', labelsize=12)
ax.tick_params(axis='both', which='minor', labelsize=12)




#plt.axhspan(1.7, 1.9, alpha = 0.5, zorder = -100, rasterized = True)


#@| Planet names and arrows
lw_arrows = 1.5
#@|TOI-244
props = dict(boxstyle='round', facecolor='wheat', alpha=1, ec = "black" )
props_244 = dict(boxstyle='round', facecolor='lightgreen', alpha=1, lw = lw_arrows , ec = 'black')

plt.text(1.4, 1.75, "TOI-244 b", fontsize = 12,  weight='bold', bbox = props_244)
plt.arrow(2.1, 1.76, 0.35, -0.17, head_width = 0.04, head_length = 0.1, lw = lw_arrows , color = 'black')

plt.text(0.80, 1.58, "L 98-59 d", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.6, 0.35, -0.045, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.80, 1.43, "L 98-59 c", fontsize = 12,   bbox = props)
plt.arrow(1.38, 1.45, 0.65, -0.038, head_width = 0.03, head_length = 0.1, lw = lw_arrows , color = 'k')

plt.text(0.765, 1.30, "TOI-4481 b", fontsize = 12,   bbox = props)
plt.arrow(1.4, 1.315, 0.20, 0.008, head_width = 0.02, head_length = 0.07, lw = lw_arrows, color = 'k')

plt.text(2.2, 1.1, "TOI-561 b", fontsize = 12,   bbox = props)
plt.arrow(2.85, 1.13, -0.5, 0.195, head_width = 0.06, head_length = 0.04, lw = lw_arrows, color = 'k')

plt.text(2, 1.91, "HD 260655 c", fontsize = 12,   bbox = props)
plt.arrow(3.1, 1.87, 0, -0.23, head_width = 0.12, head_length = 0.04, lw = lw_arrows, color = 'k')


plt.Circle((2, 2), 5, color='blue')



#plt.axhline(1.35)
#plt.axhline(1.9)



plt.legend(loc = "lower right", fontsize = 11)

plt.ylabel(r'Planet Radius $\rm [R_{\odot}]$', fontsize = 15)
plt.xlabel(r'Planet Mass $\rm [M_{\odot}]$', fontsize = 15)

plt.xlim(0.5, 32)
plt.ylim(0.9, 2.8)

plt.xlim(0.5, 22)
plt.ylim(0.9, 2.9)

#plt.xlim(1, 3.3)
#plt.ylim(1.5, 1.62)



#@|TOI-561

#plt.scatter(1.59, 1.423)
#plt.scatter(3.2, 1.45)

#plt.savefig('M-R_diagram_'+color_scale+'.pdf', bbox_inches = 'tight')

x = [1.55, 1.58,  2., 2.5, 3.5, 2.6, 1.9]
y = [1.35, 1.5, 1.67, 1.68, 1.6, 1.38, 1.30]
#ax.scatter(x, y, zorder=3)

tck, u = interpolate.splprep([x + x[:1], y + y[:1]], s=0, per=True)
unew = np.linspace(0, 1, 100)
basic_form = interpolate.splev(unew, tck)
ax.plot(basic_form[0], basic_form[1], color='blue', lw=2,alpha = 0.7)
ax.fill(basic_form[0], basic_form[1], color='dodgerblue', alpha=0.2)

plt.savefig('M-R_diagram_'+color_scale+'.pdf', bbox_inches = 'tight')

#plt.scatter(2.66, 1.315, s = 100)


# In[ ]:


idxs_insol = np.where((M_NEA<3.5) & (R_NEA<2))[0]
len(idxs_insol)


# In[ ]:


met_err_up = met_err_up[idxs_insol]
met_err_down = met_err_down[idxs_insol]

Teq_err_up = Teq_err_up[idxs_insol]
Teq_err_down = Teq_err_down[idxs_insol]


# In[ ]:


met_err = [(abs(met_err_up[i]), abs(met_err_down[i])) for i in range(len(met_err_up))]
Teq_err = [(abs(Teq_err_up[i]), abs(Teq_err_down[i])) for i in range(len(Teq_err_up))]
#met_err_low = [(abs(met_err_up_low[i]), abs(met_err_down_low[i])) for i in range(len(met_err_up_low))]


# In[ ]:





# In[ ]:


pure_rock_int = interpolate.interp1d(m_pure_rock, r_pure_rock)
earth_like_int = interpolate.interp1d(m_earth_like, r_earth_like)


# In[ ]:


x  = np.linspace(0.5,5, 1000)


# In[ ]:





# In[ ]:


norm_dens = (M_NEA[idxs_insol] / R_NEA[idxs_insol]**3) / (M_NEA[idxs_insol] / pure_rock_int(M_NEA[idxs_insol])**3)
norm_dens_earth = (M_NEA[idxs_insol] / R_NEA[idxs_insol]**3) / (M_NEA[idxs_insol] / earth_like_int(M_NEA[idxs_insol])**3)
#norm_dens_low = (M_NEA[idxs_insol_low] / R_NEA[idxs_insol_low]**3) / (M_NEA[idxs_insol_low] / pure_rock_int(M_NEA[idxs_insol_low])**3)


# In[ ]:


r_d,m_d = 1.521, 1.94
r_c,m_c = 1.385, 2.22
r_hd, m_hd = 1.533, 3.09


# In[ ]:


norm_dens_toi244 = (m_toi244_b / r_toi244_b**3) / (m_toi244_b / pure_rock_int(m_toi244_b)**3)
norm_dens_earth_toi244 = (m_toi244_b / r_toi244_b**3) / (m_toi244_b / earth_like_int(m_toi244_b)**3)
norm_dens_toi4481 = (m_toi4481_b / r_toi4481_b**3) / (m_toi4481_b / pure_rock_int(m_toi4481_b)**3)
norm_dens_earth_toi4481 = (m_toi4481_b / r_toi4481_b**3) / (m_toi4481_b / earth_like_int(m_toi4481_b)**3) ###
norm_dens_toi561 = (m_toi561_b/ r_toi561_b**3) / (m_toi561_b / pure_rock_int(m_toi561_b)**3)
norm_dens_c = (m_c/ r_c**3) / (m_c / pure_rock_int(m_c)**3)
norm_dens_d = (m_d/ r_d**3) / (m_d / pure_rock_int(m_d)**3)
norm_dens_hd = (m_hd/ r_hd**3) / (m_hd / pure_rock_int(m_hd)**3)


# In[ ]:


def err_dens(m,r,err_m, err_r):
    a = err_m / r**3
    b = 3*m*err_r / r**4
    return np.sqrt(a**2+b**2)


# In[ ]:





# In[ ]:


norm_dens_err = err_dens(M_NEA[idxs_insol],  R_NEA[idxs_insol], np.array(M_NEA_ERR).T[1][idxs_insol], np.array(R_NEA_ERR).T[1][idxs_insol])
#@|watch out above (to change with the proper upper and lowe limits)


# In[ ]:


from uncertainties import ufloat
from uncertainties.umath import *  # sin(), etc.
#@|Insolations calculations
S = np.zeros(len(RS_NEA))
S_err = np.zeros(len(RS_NEA))
for i in range(len(RS_NEA)):
    #RS_NEA_C = ufloat()
    
    a=ufloat(RS_NEA[i], RS_NEA_ERR[i])**2 * (ufloat(Teff_NEA[i], Teff_NEA_ERR[i]) / 5780)**4 * (1/ufloat(a_NEA[i], a_NEA_ERR[i]))**2
    
    S[i] = a.n
    S_err[i] = a.s


# In[ ]:


norm_dens_err = err_dens(M_NEA[idxs_insol],  R_NEA[idxs_insol], np.array(M_NEA_ERR).T[1][idxs_insol], np.array(R_NEA_ERR).T[1][idxs_insol])


# In[ ]:





# In[ ]:


Teq_new = Teq[idxs_insol]

for i in range(len(Teq[idxs_insol])):
    if Teq[idxs_insol][i] < 1.34:
        Teq_new[i] = np.nan
    
# In[ ]:


Teq_new


# In[ ]:


plt.figure(figsize = (8, 6))
line_w = 2
size = 180
#vmin =3200,vmax = 5000,
plt.scatter(Teq_new, norm_dens,  cmap ='Spectral', s = size, ec = "black",c = Teff_NEA[idxs_insol],vmin =3200,vmax = 5000, lw = line_w, zorder = 1)
plt.errorbar(Teq_new, norm_dens, xerr=np.array(S_err[idxs_insol]).T, linestyle  = "None", c = "k",  capsize = 4, lw = 3, zorder = 0)
plt.errorbar(Teq_new, norm_dens, yerr=norm_dens_err, linestyle  = "None", c = "k",  capsize = 3, lw = 3, zorder = 0)
cbar_2 = plt.colorbar(location = 'right')
cbar_2.set_label(r'Stellar effective temperature (K)', fontsize = 13)
cbar_2.ax.tick_params(labelsize=10)


plt.scatter(insol_toi244_b, norm_dens_toi244, c = 3433 ,cmap ='Spectral' , s = size, ec = "blue", vmin =3200,vmax = 5000, lw = line_w, zorder = 1, label = 'TOI-244 b')
plt.errorbar(insol_toi244_b, norm_dens_toi244, xerr=0.07, linestyle  = "None", c = "blue",  capsize = 2, zorder = 0, lw = 3)
plt.errorbar(insol_toi244_b, norm_dens_toi244, yerr=err_dens(m_toi244_b, r_toi244_b, merr_toi244_b, rerr_toi244_b), linestyle  = "None", c = "blue",  capsize = 2, zorder = 0, lw = 3)

plt.scatter(insol_toi4481_b, norm_dens_toi4481, c = 3600 ,cmap ='Spectral' , s = size, ec = "black", vmin =3200,vmax = 5000, lw = line_w, zorder = 1)
plt.errorbar(insol_toi4481_b, norm_dens_toi4481, xerr=0.07, linestyle  = "None", c = "black",  capsize = 2, zorder = 0)
plt.errorbar(insol_toi4481_b, norm_dens_toi4481, yerr=0.12, linestyle  = "None", c = 'black',  capsize = 4, lw = 3, zorder = 0)

#plt.scatter(insol_toi561_b, norm_dens_toi561, c =5455, cmap ='Spectral', s = size, ec = "black", vmin =3200,vmax = 5000, lw = line_w, zorder = 1)
#plt.errorbar(insol_toi561_b, norm_dens_toi561, xerr=0.04, linestyle  = "None", c = "black",  capsize = 2, zorder = 0)
#plt.errorbar(insol_toi561_b, norm_dens_toi561, yerr=0.10, linestyle  = "None", c = "black",  capsize = 4, lw = 3, zorder = 0)
#r'Insolation Flux $\rm (S_{\oplus})$'
plt.xlabel(r'Insolation Flux $\rm (S_{\oplus})$', fontsize = 17)
plt.ylabel(r'$\rho$ / $\rho_{rock}$', fontsize = 17)

plt.tick_params(axis='x', labelsize=13)
plt.tick_params(axis='y', labelsize=13)

plt.xscale('log')
plt.yscale('log')
plt.xlim(1.34,80)
plt.ylim(0.34,2)

plt.axhspan(0., 1.0,alpha = 0.1, color = "cyan")
plt.axhspan(1.0, 2.0,alpha = 0.1, color = 'brown')
#plt.ylim(0.6, 1.2)
#plt.xlim(-1, 0)

legend = plt.legend(loc = 'upper left', fontsize = 12, edgecolor = "black")
legend.get_frame().set_alpha(1)
legend.get_frame().set_facecolor('white')

#plt.scatter(np.log(Teq_new_notnans_down), y_pred_notnans_down, s =400)

plt.plot(np.exp(thin_x), y)

plt.savefig('dens_vs_Teq.pdf', bbox_inches = 'tight')

plt.scatter(2, 0)


# In[ ]:


met[idxs_insol]


# In[ ]:


plt.scatter(Teq_new_notnans_down, norm_dens_notnans_down)
plt.xlim(0,100)


# In[ ]:


Teq_new_notnans_down.tolist()


# In[ ]:


plt.plot(Teq_new_notnans_down, y_pred_notnans_down)


# In[ ]:





# In[ ]:


from sklearn.linear_model import LinearRegression


# In[ ]:


notnan = np.where(~np.isnan(Teq_new))[0]


# In[ ]:


Teq_new_notnans = Teq_new[notnan]
norm_dens_notnans = norm_dens[notnan]


# In[ ]:


Teq_new_notnans  = np.log(Teq_new_notnans)
#norm_dens_notnans  = np.log(norm_dens_notnans)


# In[ ]:


down_idxs = np.where(norm_dens_notnans<1)[0]


# In[ ]:


Teq_new_notnans_down = Teq_new_notnans[down_idxs]


# In[ ]:


norm_dens_notnans_down = norm_dens_notnans[down_idxs]


# In[ ]:


Teq_new_notnans_down = np.append(Teq_new_notnans_down,insol_toi4481_b)
norm_dens_notnans_down = np.append(norm_dens_notnans_down, norm_dens_toi4481)


# In[ ]:


Teq_new_notnans_down = np.delete(Teq_new_notnans_down, 9)
norm_dens_notnans_down = np.delete(norm_dens_notnans_down, 9)


# In[ ]:


model_down = LinearRegression().fit(Teq_new_notnans_down.reshape((-1, 1)), norm_dens_notnans_down)


# In[ ]:


r_sq = model_down.score(Teq_new_notnans_down.reshape((-1, 1)), norm_dens_notnans_down)
print(f"coefficient of determination: {r_sq}")


# In[ ]:


print(f"intercept: {model_down.intercept_}")
print(f"slope: {model_down.coef_}")


# In[ ]:


a = 10**(0.00150168)
b = 10**(0.6994443753861932)


# In[ ]:


np.exp(0.00150168)


# In[ ]:


thin_x = np.linspace(0.1, 10000, 10000)


# In[ ]:


y = a*thin_x + b


# In[ ]:


y_pred_notnans_down = model_down.predict(Teq_new_notnans_down.reshape((-1, 1)))


# In[ ]:


##############################333


# In[ ]:


norm_dens_err = err_dens(M_NEA[idxs_insol],  R_NEA[idxs_insol], np.array(M_NEA_ERR).T[1][idxs_insol], np.array(R_NEA_ERR).T[1][idxs_insol])
#norm_dens_err_low = err_dens(M_NEA[idxs_insol_low],  R_NEA[idxs_insol_low], np.array(M_NEA_ERR).T[1][idxs_insol_low], np.array(R_NEA_ERR).T[1][idxs_insol_low])
#@|watch out above (to change with the proper upper and lowe limits)


# In[ ]:


met[np.where(names=='Kepler-114 c')] = -0.20


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


plt.figure(figsize = (8, 6))
size = 180
c_new = "blue"
c_low = 'orange'
line_w = 2

#@|NEA planets
plt.scatter(met[idxs_insol], norm_dens,  cmap ='Spectral', s = size, ec = "black", c = Teff_NEA[idxs_insol],vmin =3200,vmax = 5000, lw = line_w, zorder = 1)
plt.errorbar(met[idxs_insol], norm_dens, xerr=np.array(met_err).T, linestyle  = "None", c = "k",  capsize = 4, lw = 3, zorder = 0)
plt.errorbar(met[idxs_insol], norm_dens, yerr=norm_dens_err, linestyle  = "None", c = "k",  capsize = 3, lw = 3, zorder = 0)

cbar_1 = plt.colorbar(location = 'right')
cbar_1.set_label(r'Stellar effective temperature (K)', fontsize = 13)
cbar_1.ax.tick_params(labelsize=10)

#plt.scatter(met[idxs_insol_low], norm_dens_low, s = size, ec = "black", c = c_low, lw = line_w, zorder = 1)
#plt.errorbar(met[idxs_insol_low], norm_dens_low, xerr=np.array(met_err_low).T, linestyle  = "None", c = c_low,  capsize = 4, lw = 3, zorder = 0)
#plt.errorbar(met[idxs_insol_low], norm_dens_low, yerr=norm_dens_err_low, linestyle  = "None", c = c_low,  capsize = 3, lw = 3, zorder = 0)


#plt.scatter(met[idxs_insol_low], norm_dens_low, s = size, ec = "black", c = 'orange')

#@|Extra planets
plt.scatter(met_toi244_b, norm_dens_toi244, c = 3433, cmap ='Spectral',s = size, vmin =3200,vmax = 5000, ec = "blue", zorder = 10, lw = line_w, label = 'TOI-244 b (SteParSyn)')
plt.errorbar(met_toi244_b, norm_dens_toi244, xerr=0.07, linestyle  = "None", c = 'blue',  capsize = 4, lw = 3)
plt.errorbar(met_toi244_b, norm_dens_toi244, yerr=err_dens(m_toi244_b, r_toi244_b, merr_toi244_b, rerr_toi244_b), linestyle  = "None", c = 'blue',  capsize = 4, lw = line_w)
plt.scatter(-0.03, norm_dens_toi244, c = c_new , marker = 'x', s = size, ec = 'dodgerblue', lw = line_w,  label = 'TOI-244 b (ODUSSEAS)')
eb1 = plt.errorbar(-0.03, norm_dens_toi244, xerr=0.11, linestyle  = "None", c = 'dodgerblue',  capsize = 2,)
eb1[-1][0].set_linestyle('--')
eb2=plt.errorbar(-0.03, norm_dens_toi244, yerr=err_dens(m_toi244_b, r_toi244_b, merr_toi244_b, rerr_toi244_b), linestyle  = "None", c = 'dodgerblue',  capsize = 2)
eb2[-1][0].set_linestyle('--')

plt.scatter(met_toi4481_b, norm_dens_toi4481, c = 3600 , s = size, ec = "black", lw = line_w, zorder = 1, cmap ='Spectral',vmin =3200,vmax = 5000,)
plt.errorbar(met_toi4481_b, norm_dens_toi4481, xerr=0.07, linestyle  = "None", c = 'black',  capsize = 4, lw = 3, zorder = 0)
plt.errorbar(met_toi4481_b, norm_dens_toi4481, yerr=0.12, linestyle  = "None", c = 'black',  capsize = 4, lw = 3, zorder = 0)

#plt.scatter(met_toi561_b, norm_dens_toi561, c = 5455, s = size, ec = "black", lw = line_w, zorder = 1, cmap ='Spectral',vmin =3200,vmax = 5000,)
#plt.errorbar(met_toi561_b, norm_dens_toi561, xerr=0.04, linestyle  = "None", c = "black",  capsize = 4, lw = 3, zorder = 0)
#plt.errorbar(met_toi561_b, norm_dens_toi561, yerr=0.10, linestyle  = "None", c = "black",  capsize = 4, lw = 3, zorder = 0)

#plt.scatter(-0.43, norm_dens_hd, c = c_new, s = size, ec = "black", zorder = 1, lw = line_w)
#plt.scatter(-0.46, norm_dens_c, c = c_new, s = size, ec = "black", zorder = 1, lw = line_w)
#plt.scatter(-0.46, norm_dens_d, c = c_new, s = size, ec = "black", zorder = 1, lw = line_w)



plt.axhspan(0., 1.0,alpha = 0.1, color = "cyan")
plt.axhspan(1.0, 2.0,alpha = 0.1, color = 'brown')


#plt.axhline(1.2,c = 'black', linestyle = "dashed")

plt.xlabel('[Fe/H] (dex)', fontsize = 17)
plt.ylabel(r'$\rho$ / $\rho_{rock}$', fontsize = 17)

plt.tick_params(axis='x', labelsize=13)
plt.tick_params(axis='y', labelsize=13)

#plt.
#plt.yscale('log')
#plt.xlim(0, 100)
#plt.ylim(0.6, 1.2)
#plt.xlim(-1, 0)

#plt.ylim(0.34,1.6)
#plt.xlim(-0.55, 0.43)



legend = plt.legend(loc = 'upper left', fontsize = 12, edgecolor = "black")
legend.get_frame().set_alpha(1)
legend.get_frame().set_facecolor('white')


plt.savefig('dens_vs_met.pdf', bbox_inches = 'tight')


# In[ ]:


norm_dens


# In[ ]:


norm_dens_toi244


# In[ ]:


err_dens(m_toi244_b, r_toi244_b, merr_toi244_b, rerr_toi244_b)


# In[ ]:


#@|TABLE


# In[ ]:


M_NEA[idxs_insol][idxs_below_1]


# In[ ]:


norm_dens_earth[idxs_below_1]
norm_dens_err[idxs_below_1]


# In[ ]:


1 = norm_dens + sigma * err


# In[ ]:


#@|SIGMA to earth
sigma_earth = np.zeros(len(norm_dens_earth[idxs_below_1]))
for i in range(len(norm_dens_earth[idxs_below_1])):
    sigma_earth[i] = (1-norm_dens_earth[idxs_below_1][i]) / norm_dens_err[idxs_below_1][i]
    
sigma_earth


# In[ ]:


err_dens(1.90, 1.331, 0.17, 0.023)
err_dens(2.68, 1.52, 0.30, 0.12)


# In[ ]:


(1- norm_dens_earth_toi4481) / 0.083323830933821


# In[ ]:


(1- norm_dens_earth_toi244) / 0.1999146486549182


# In[ ]:


0.023 / 1.331


# In[ ]:


#@|MASS relative precission 
M_NEA_ERR_MAX = np.zeros(len(M_NEA_ERR))
for i in range(len(M_NEA_ERR)):
    M_NEA_ERR_MAX[i] = np.mean(M_NEA_ERR[i])
    
#M_NEA_ERR_MAX[idxs_insol][idxs_below_1]

relative_errors_M = np.zeros(len(M_NEA))
for i  in range(len(M_NEA)):
    relative_errors_M[i] = (M_NEA_ERR_MAX[i] / M_NEA[i]) * 100
relative_errors_M[idxs_insol][idxs_below_1]


# In[ ]:


#@|Radius relative precission 
R_NEA_ERR_MAX = np.zeros(len(R_NEA_ERR))
for i in range(len(R_NEA_ERR)):
    R_NEA_ERR_MAX[i] = np.mean(R_NEA_ERR[i])
    
#M_NEA_ERR_MAX[idxs_insol][idxs_below_1]

relative_errors_R = np.zeros(len(R_NEA))
for i  in range(len(R_NEA)):
    relative_errors_R[i] = (R_NEA_ERR_MAX[i] / R_NEA[i]) * 100
relative_errors_R[idxs_insol][idxs_below_1]


# In[ ]:


idxs_below_1 = np.where(norm_dens<1)[0]


# In[ ]:


names[idxs_insol][idxs_below_1]


# In[ ]:


#@|rho_norm
norm_dens[idxs_below_1]


# In[ ]:


#@|rho_norm_err
norm_dens_err[idxs_below_1]


# In[ ]:


met[idxs_insol][idxs_below_1]


# In[ ]:


#@|Insolation
S[idxs_insol][idxs_below_1].tolist()


# In[ ]:


names[idxs_insol][idxs_below_1]


# In[ ]:


S_err[idxs_insol][idxs_below_1].tolist()


# In[ ]:


names[idxs_insol]


# In[ ]:


names[idxs_insol]


# In[ ]:


a = np.array(np.array(['GJ 1132 b', 'GJ 1252 b', 'GJ 3473 b', 'GJ 357 b', 'GJ 367 b',
       'GJ 3929 b', 'GJ 486 b', 'HD 23472 c', 'HD 260655 b',
       'HD 260655 c', 'K2-229 b', 'KOI-1831 d', 'Kepler-114 c',
       'Kepler-138 b', 'Kepler-138 c', 'Kepler-138 d', 'Kepler-1972 b',
       'Kepler-1972 c', 'Kepler-78 b', 'L 98-59 c', 'L 98-59 d',
       'LHS 1140 c', 'LHS 1478 b', 'LTT 1445 A b', 'LTT 1445 A c',
       'LTT 3780 b', 'TOI-1468 b', 'TOI-178 b', 'TOI-1807 b', 'TOI-270 b',
       'TOI-431 b', 'TOI-500 b', 'TOI-561 b', 'TRAPPIST-1 b',
       'TRAPPIST-1 c', 'TRAPPIST-1 d', 'TRAPPIST-1 e', 'TRAPPIST-1 f',
       'TRAPPIST-1 g', 'TRAPPIST-1 h'], dtype=object).tolist() + np.array(['GJ 1132 b', 'GJ 1252 b', 'GJ 3473 b', 'GJ 357 b', 'GJ 367 b',
       'GJ 3929 b', 'GJ 486 b', 'HD 23472 c', 'HD 260655 b',
       'HD 260655 c', 'K2-229 b', 'KOI-1831 d', 'Kepler-114 c',
       'Kepler-138 b', 'Kepler-138 c', 'Kepler-138 d', 'Kepler-1972 b',
       'Kepler-1972 c', 'Kepler-78 b', 'L 98-59 c', 'L 98-59 d',
       'LHS 1140 c', 'LHS 1478 b', 'LTT 1445 A b', 'LTT 1445 A c',
       'LTT 3780 b', 'TOI-1468 b', 'TOI-178 b', 'TOI-1807 b', 'TOI-270 b',
       'TOI-431 b', 'TOI-500 b', 'TOI-561 b', 'TRAPPIST-1 b',
       'TRAPPIST-1 c', 'TRAPPIST-1 d', 'TRAPPIST-1 e', 'TRAPPIST-1 f',
       'TRAPPIST-1 g', 'TRAPPIST-1 h'], dtype=object).tolist())


# In[ ]:





# In[ ]:


len(np.unique(names[idxs_insol].tolist().extend(names[idxs_insol].tolist())


# In[ ]:


names[idxs_insol]+names[idxs_insol]


# In[ ]:


#@|Ks test


# In[ ]:


idxs_sub_solar = np.where(met[idxs_insol]<0.0)[0]
idxs_super_solar = np.where(met[idxs_insol]>0.0)[0]


# In[ ]:





# In[ ]:


sub_solar_sample = norm_dens[idxs_sub_solar]
sub_solar_sample_err = norm_dens_err[idxs_sub_solar]

sub_solar_sample = np.append(sub_solar_sample, norm_dens_toi4481)
sub_solar_sample_err = np.append(sub_solar_sample, 0.12)

sub_solar_sample = np.append(sub_solar_sample, norm_dens_toi561)
sub_solar_sample_err = np.append(sub_solar_sample, 0.10)


#sub_solar_sample = np.append(sub_solar_sample, met_toi4481_b)
#sub_solar_sample = np.append(sub_solar_sample, met_toi561_b)
#sub_solar_sample = np.append(sub_solar_sample, met_toi244_b)
super_solar_sample = norm_dens[idxs_super_solar]
super_solar_sample_err = norm_dens_err[idxs_super_solar]


# In[ ]:


from scipy.stats import ks_2samp

#perform Kolmogorov-Smirnov test
ks_2samp(sub_solar_sample , super_solar_sample)


# In[ ]:


np.random.seed(9001)
siz = 100000

p_values = np.zeros(siz)
for i in range(siz):
    sub_solar_ac = np.zeros(len(norm_dens))
    super_solar_ac = np.zeros(len(norm_dens))
    for j in range(len(sub_solar_sample)):
        sub_solar_ac[j] = np.random.normal(sub_solar_sample[j], sub_solar_sample_err[j])
        
    for j in range(len(super_solar_sample)):
        super_solar_ac[j] = np.random.normal(super_solar_sample_err[j], super_solar_sample_err[j])
        
        
    p_values[i] = ks_2samp(sub_solar_ac, super_solar_ac).statistic
    #p_values[i] =  sub_solar_ac[0]
    
    #print(sample_ac)
        


# In[ ]:


np.percentile(p_values, [50]), np.percentile(p_values, [15.87]), np.percentile(p_values, [84.13])


# In[ ]:


np.percentile(p_values, [50]), np.percentile(p_values, [50]) - np.percentile(p_values, [15.87]), np.percentile(p_values, [84.13]) - np.percentile(p_values, [50])


# In[ ]:


np.percentile(p_values, [84.13]) - np.percentile(p_values, [50])


# In[ ]:


np.percentile(p_values, [50]) - np.percentile(p_values, [15.87])


# In[ ]:


(1- np.percentile(p_values, [50])) * 100


# In[ ]:


(1-np.percentile(p_values, [84.13])) * 100, (1-np.percentile(p_values, [15.87])) * 100


# In[ ]:


plt.hist(p_values, bins = 50)
#plt.xlim(0, 0.15)


# In[ ]:


p_values


# In[ ]:


names[idxs_insol][1]


# In[ ]:


np.where((norm_dens<1) & (met[idxs_insol]>-0) )


# In[ ]:





# In[ ]:


np.where((norm_dens<0.8) & (met[idxs_insol]>0.2))


# In[ ]:





# In[ ]:


R_NEA_DOWN[idxs_insol][17]


# In[ ]:


0.18 / 1.6


# In[ ]:


0.6 / 2.8


# In[ ]:


R_NEA[idxs_insol][17]


# In[ ]:


plt.scatter(-0.43, norm_dens_hd, c = c_new, s = size, ec = "black", zorder = 1, lw = line_w)
plt.scatter(-0.46, norm_dens_c, c = c_new, s = size, ec = "black", zorder = 1, lw = line_w)
plt.scatter(-0.46, norm_dens_d, c = c_new, s = size, ec = "black", zorder = 1, lw = line_w)


# In[ ]:


A = (m_pure_rock.values / r_pure_rock.values**3)
B = (m_earth_like.values / r_earth_like.values**3)


# In[ ]:





# In[ ]:


plt.errorbar(x = met[idxs_insol], y  = norm_dens, xerr=np.array(met_err).T, linestyle  = "None", c = "blue")


# In[ ]:


met_err


#   #### norm_dens_toi244

# In[ ]:


34.3 +- 6.5  #NEW


# In[ ]:


norm_dens_toi244


# In[ ]:


plt.scatter(m_pure_iron.values, r_pure_iron)
plt.xlim(0, 6)
plt.xlim(0.5, 22)
plt.ylim(0.9, 2.9)


# In[ ]:





# In[ ]:


(2.66 / 1.72**3) / (2.66/1.30**3)


# In[ ]:


df_20_fe = pd.read_csv('20%_fe', sep = '\t', header = None)
m_20_fe, r_20_fe = df_20_fe[0].values, df_20_fe[1].values


# In[ ]:


df_0_fe = pd.read_csv('0%_fe', sep = '\t', header = None)
m_0_fe, r_0_fe = df_0_fe[0].values, df_0_fe[1].values


# In[ ]:


#@|M-R relations from turbet et al. (2020)


# In[ ]:


M, R = 2.66, 1.5


# In[ ]:


from astropy.constants import G
import astropy.constants as const

frac = 0.004
1 / (1/frac +1)



R_cons,M_h20, Pt = 8.314, 1.8e-2, 0.1 # fixed
g_core = G.value * m_earth_like * const.M_earth.value / (r_earth_like*const.R_earth.value)**2
g = G.value * M * const.M_earth.value / (R*const.R_earth.value)**2

alpha_1, alpha_2, alpha_3, alpha_4, alpha_5, alpha_6 = -3.550, 1.310, 1.099, 4.683e-1, 7.664e-1, 4.224e-1
beta_1, beta_2, beta_3, beta_4, beta_5 = 2.846, 1.555e-1, 8.777e-2, 6.045e-2, 1.143e-2
beta_6, beta_7, beta_8, beta_9, beta_10 = 1.736e-2, 1.859e-2, 4.314e-2, 3.393e-2, -1.034e-2

R_s= 0.428
Seff =  0.02277292940122454 * (28*R_s*const.R_sun.value / const.au.value )**-2

X = (np.log10(frac)-alpha_1) / alpha_2
Y = (np.log10(g)-alpha_3) / alpha_4
Z = (np.log10(Seff)-alpha_5)/alpha_6

X = (np.log10(frac)-alpha_1) / alpha_2
Y = (np.log10(g)-alpha_3) / alpha_4
Z = (np.log10(Seff)-alpha_5)/alpha_6

Teff = 10**(beta_1+beta_2*X+beta_3*Y+beta_4*Z+beta_5*X*Y+beta_6*Y**2+beta_7*X**3+beta_8*X**2*Y+beta_9*X*Y**2+beta_10*Y**4)

#@|z_atm 
a = np.log(frac / (1-frac) * g_core**2 / 4 / np.pi / G.value / Pt) 
b = R_cons * Teff / M_h20 / g_core
c = 1 / (r_earth_like*const.R_earth.value)
z_atm = (1 / a / b - c)**(-1)

#r_new = (r_earth_like.values*const.R_earth.value + z_atm) / const.R_earth.value 
#m_new = m_earth_like.values / (1-frac)

globals()['r_new_'+str(int(frac*1000))] = (r_earth_like*const.R_earth.value + z_atm) / const.R_earth.value 
globals()['m_new_'+str(int(frac*1000))] = m_earth_like / (1-frac)


# In[ ]:


r_new_4


# In[ ]:


########################


# In[ ]:





# In[ ]:


#@|How to plot error bars of the same color of data points
#convert time to a color tuple using the colormap used for scatter
#import matplotlib
#import matplotlib.cm as cm
#norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
#mapper = cm.ScalarMappable(norm=norm, cmap='rainbow')
#time_color = np.array([(mapper.to_rgba(v)) for v in met])

#loop over each data point to plot
#plt.xscale('log')
#plt.xlim(0.6, 50)
#plt.ylim(0, 3.5)
#for x, y, e, color in zip(M_NEA, R_NEA, R_NEA_UP, time_color):
    #plt.scatter(x, y, color=color)
    #plt.errorbar(x, y, e, lw=1, capsize=3, color=color)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


earth_like_int(1.90)


# In[ ]:




