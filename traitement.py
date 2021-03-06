# -*- coding: utf-8 -*-

""" 
Auteur : Marc-Antoine BUCHET
Date : 28/06/2019

Lycée Marceau - Chartres

Test du capteur de pression.
"""

import numpy as np
import matplotlib.pyplot as plt
import fonctions_utiles as fu

import os

################################################################################
# Paramétrage des graphs :
################################################################################   
font = {'family' : 'sans',
        'weight' : 'bold',
        'size'   : 12}
plt.rc('font', **font)
lines = {'linewidth' : 2.0,
         'markeredgewidth' : 2.0,
         'markersize' : 10.0}
plt.rc('lines', **lines)

plt.ion() # activation du mode interactif

plt.close('all') # fermeture des figures éventuellement ouvertes
    
##############################################################################
# Paramètres :
############################################################################## 
############
# Dossiers :
############
data_folder='donnees/'
figure_folder='figures/'

########################
# Paramètres physiques :
########################

###################
# Modèle linéaire :
###################
def model(x,a,b):
    return a*x+b

##############################################################################
# Données  : 
##############################################################################
T = 273.15 + 30 # K

diametre_interieur_tube = 3.5e-3 # m
ddiametre_interieur_tube = 0.25e-3 # m

longueur_tube = 1. # m
dlongueur_tube = 5.e-3 # m
#volume_tube = pi*(diametre_interieur_tube/2)**2*longueur_tube
volume_tube = 12.e-6 # m^3
print("Volume du tube :",volume_tube)
dvolume_tube = volume_tube*np.sqrt(
                       2*(ddiametre_interieur_tube/diametre_interieur_tube)**2
                       + (dlongueur_tube/longueur_tube)**2)

# Données : volume en mL , Signal mesuré UA (de 0 à 1023)
data = np.array([ [60.,295.] ,
                  [55.,307.] ,
                  [50.,321.] ,
                  [45.,333.] ,
                  [40.,351.] ,
                  [35.,372.] ,
                  [30.,398.] ,
                  [25.,428.] ,
                  [20.,465.] ,
                ])

V = data[:,0]*1.e-6 # m^3
dV=1.e-6*np.ones(len(V)) # m^3

Signal = data[:,1] 
dSignal = 1.*np.ones(len(Signal))


##############################################################################
# Graph 1 : Pression en fonction du volume 
##############################################################################
figname,fig,ax=fu.start_fig('P_vs_V')
ax.errorbar(V,Signal,xerr=dV,yerr=dSignal,fmt='+',capsize=3,
            label=u'Signal vs V')
ax.errorbar(V+volume_tube,Signal,xerr=dV,yerr=dSignal,fmt='+',capsize=3,
            label=u'Signal vs V + V_tube')
#fu.add_fit(ax,m_min,m_max,model,[a,b],[da,db],position=(0.11,0.6),N_points=2,
#        chisq=chisq,chisq_red=chisq_red,description=description)
ax.set_xlabel(u'volume ($m^3$)',fontweight='bold') # nom de l'axe x
ax.set_ylabel(u'Signal arduino UA',fontweight='bold') # nom de l'axe y
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#ax.set_xlim(0.9*m_min,1.05*m_max)
plt.legend()
fu.save_fig(figname,fig,figure_folder)

inverseVolume = 1/V
dinverseVolume = inverseVolume*dV/V

##############################################################################
# Graph : Pression en fonction de l'inverse du volume
##############################################################################
figname,fig,ax=fu.start_fig('P_vs_inverse_du_volume')
ax.errorbar(inverseVolume,Signal,xerr=dinverseVolume,yerr=dSignal,fmt='+',
            capsize=3, label=u'mesures')


inverseVolume = 1/(V+volume_tube)
dinverseVolume = inverseVolume*dV/(V+volume_tube)

a,da,b,db,chisq,chisq_red = fu.reg_lin(inverseVolume,Signal,dSignal)
description = ['Signal=a/V+b','a','b']

i_min=min(inverseVolume)
i_max = max(inverseVolume)

ax.errorbar(inverseVolume,Signal,xerr=dinverseVolume,yerr=dSignal,fmt='+',
            capsize=3, label=u'mesures')
fu.add_fit(ax,i_min,i_max,model,[a,b],[da,db],position=(25500,280),N_points=2,
           chisq=chisq,chisq_red=chisq_red,description=description)
ax.set_xlabel(u'inverse du volume ($m^{-3}$)',fontweight='bold') # nom de l'axe x
ax.set_ylabel(u'Signal arduino UA',fontweight='bold') # nom de l'axe y
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#ax.set_xlim(0.9*m_min,1.05*m_max)
#legend(loc='lower right')
fu.save_fig(figname,fig,figure_folder)
