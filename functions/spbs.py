#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 09:36:04 2021

@author: brunocamino
"""
import numpy as np

import matplotlib.pyplot as plt
from plotting import plot_bands
from extract_info import reciprocal_lattice
import matplotlib.lines as mlines
from settings import runprop
from settings import runcry
import time
import os.path


def plot_spbs(file_name,k_path_s,k_labels,energy_range,run,title,n_bands=10,newk=0,
              n_k_points=200,first_band=1,last_band=26,not_scaled=False,slab_bs=None):
    
    """run_calc = runcry(file_name) 
    process = subprocess.Popen(run_calc.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()"""
    
    #Bulk scf calculation
    runcry(file_name)
    
    #Slab scf calculation
    if slab_bs != None:
        runcry(slab_bs)
        runprop(slab_bs+'_BAND', slab_bs)
    
    B =  reciprocal_lattice(file_name+'.out')


    S = np.copy(B)
    S[0][2] = 0.0
    S[1][2] = 0.0
    S[2][2] = 2*np.pi    
    
        
    B_t = np.matrix.transpose(B)
    
    B_t_inv = np.linalg.inv(B_t)
    
    S_t = np.matrix.transpose(S)
       
    fs = np.array(k_path_s)

    
    fs = np.matrix.transpose(fs) 
    
    rs = np.matmul(S_t, fs)

    
    fig, ax1 = plt.subplots(1,1)
    
    index = -1
    
    files_not_found = []
    
    #for i in np.arange(-0.5,0.6,0.05):
    for i in [i for i in np.round(np.arange(-0.5,0.6,1/n_bands),2)]:
        index += 1
        #Convert the coordinates to fractional of the redefined cell
        fb = np.matmul(B_t_inv, rs)
        #Scan a range of z coordinate
        fb[2,:] = fb[2,:]+i
        
        #Find the shrinking factor
        fb = np.around(fb,3)*1000
        a = np.array(fb.ravel()[np.flatnonzero(np.around(fb,3))],dtype=int)
        gcd = np.gcd.reduce(a)    
        fb = (fb/gcd).astype(int)
        shrink = int(1000/gcd)
        
        #Write the first part of the properties input
        data = ['NEWK\n', '%s %s\n'% (str(newk),str(newk*2)), '1 0\n', 'BAND\n', 'BN\n' ]
        
        input_name = file_name+'_spbs_%s.d3' % (str(index))
        cry_input_name = input_name[:-3]
        
        file = open(input_name, 'w')
        for line in data:
            file.writelines(line)
       
        file.writelines('%s %s %s %s %s 1 0\n' % (str(len(fb[0,:])-1),str(shrink),str(n_k_points),str(first_band),str(last_band)))
        
        #Write the k point paths
        for i in range(len(fb[0,:])-1):
            file.writelines(' '.join(str(n) for n in fb[:,i])+' '+' '.join(str(n) for n in fb[:,i+1])+'\n')
        file.writelines('END')
        file.close()
        
        """run_calc = runprop()+ "%s %s" % (cry_input_name, input_name)
        process = subprocess.Popen(run_calc.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()"""
        runprop(cry_input_name,file_name)
        time.sleep(0.1)
        
        band_file_name = input_name[:-3]+'_dat.BAND'
        if os.path.isfile(band_file_name):
           
            bands, kpoints, efermi = plot_bands(band_file_name,not_scaled);
            
            if index > 0:
                x0 = np.copy(x1)
                y0 = np.copy(y1)
                len_x0 = x0.shape[0]
                len_y0 = y0.shape[1]
            
                       
            x1 = bands[:,0,:]
            y1 = bands[:,1:,:]
            len_x1 = x1.shape[0]
            len_y1 = y1.shape[1]
            #This is to account for a +/- 1 difference in the number of k points that can happen in some cases
        
                  
            if len(bands[0,0,:]) > 1:  
                
                ax1.plot(x1[:,1], y1[:,:,1],'-',  c='red' )
                ax1.plot(x1[:,0], y1[:,:,0],'-' , c='black')        
                spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                             mlines.Line2D([], [], color='red', label='Beta')]
                ax1.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
            
            else:
                if slab_bs == None:
                    ax1.plot(x1[:,0], y1[:,:,0],'-', c='black' )  
                else:
                    #ax1.plot(x1[:,0], y1[:,:,0],'-', c='grey' )
                    #print('Plotting the %s-th line' % (index))
                    ax1.plot(x1[:,0], y1[:,:,0],'-', c='black' ) 
            if index > 0:
                min_lenx = min(len_x0,len_x1)                   
                min_leny = min(len_y0,len_y1)
                #print('Filling the gaps, x=',min_lenx,' y=',min_leny)
                for i in range(min_leny):
                    ax1.fill_between(x1[:min_lenx].flatten(),y0[:min_lenx,i,0].flatten(),y1[:min_lenx,i,0].flatten(),color='grey')
        else:
            files_not_found.append(band_file_name)
    
    '''if slab_bs != None:
        band_file_name = slab_bs+'_BAND_dat.BAND'
        print('surface_band_file_name',band_file_name)
        bands, kpoints_surface, efermi = plot_bands(band_file_name,not_scaled);
        x1 = bands[:,0,:]
        y1 = bands[:,1:,:]
        if len(bands[0,0,:]) > 1:     
            ax1.plot(x1[:,1], y1[:,:,1],'-',  c='red' )
            ax1.plot(x1[:,0], y1[:,:,0],'-' , c='black')        
            spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                         mlines.Line2D([], [], color='red', label='Beta')]
            ax1.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
        
        else:
            ax1.plot(x1[:,0], y1[:,:,0],'-', c='black' )  '''


    if not_scaled == True:
        fermi_line = [[0, np.amax(bands[:,1:,0])+1],[efermi,efermi]] 
    else:
        fermi_line = [[0, np.amax(bands[:,1:,0])+1],[0,0]] 
    ax1.plot(fermi_line[0],fermi_line[1], '--',color='grey')
        
    if len(files_not_found) > 0:
        print('The following band file(s) were not found: '+ ','.join(files_not_found))
        
    ax1.set_title('Surface projected band structure', size = 18)
    ax1.set_xlabel('k point', size =12)
    if not_scaled == False:
        ax1.set_ylabel('E-E Fermi (eV)', size =12)
    else:
        ax1.set_ylabel('E (eV)', size =12)
    ax1.set_xticks(kpoints)
    ax1.set_xticklabels(k_labels, size=12)
    ax1.set_xlim([0, bands[-1,0,0]])
    ax1.set_ylim(energy_range)
    ax1.grid()
    
        
    fig.set_size_inches(8, 8)
    if title != False:
        fig.suptitle(title, size=22)
        plt.subplots_adjust(wspace=0.2, top=0.88)

"""file_name = 'data/spbs/cu'
k_path_s = [[0.0, 0.0, 0.0],[0.5, 0.5, 0.25],[0.5, 0.5, 0.5],[0.0, 0.5, 0.25],[0.0, 0.0, 0.0],[0.5,0.5,0.5]]
k_labels = ['G','X\'','M','X\'\'','G','M']
energy_range = [-10,10]
title = 'Cu SPBS'

plot_spbs(file_name,k_path_s,k_labels,energy_range,title)"""