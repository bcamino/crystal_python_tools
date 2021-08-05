#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 10:37:18 2021

@author: brunocamino
"""

def ads_energy(E_system,E_substrate,E_adsorbate,n_adsorbates=1):
    
    from extract_info import final_energy
    
    if type(E_system) == str:
        E_system = final_energy(E_system)
    if type(E_substrate) == str:
        E_substrate = final_energy(E_substrate)
    if type(E_adsorbate) == str:
        E_adsorbate = final_energy(E_adsorbate)
    
    return (E_system-(E_substrate+E_adsorbate))*96/n_adsorbates

def plot_E_ads(E_adsorption,sites):
    
    from matplotlib import pyplot as plt
    
    xticks = []
    fig, ax = plt.subplots()
    for i,energy in enumerate(E_adsorption):
        ax.hlines(y = energy, xmin = i+0.1, xmax = i+0.9, color='black')
        xticks.append(i+0.5)

    ax.set_xticks(xticks)
    ax.set_xticklabels(sites, size=12)
    ax.set_title('Adsorption Energy', size=15)
    ax.set_ylabel('E Ads (kJ/mol)')
    ax.set_xlabel('Adsorption site');