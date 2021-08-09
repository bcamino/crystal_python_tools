#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:23:28 2021

@author: brunocamino
"""
import numpy as np
import re

def plot_bands(file_name,not_scaled=False):
    #plot from .BAND file
    import sys
    #from extract_info import fermi_energy
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .BAND file needs to be specified')
        sys.exit(1)
    
    n_kpoints = int(data[0].split()[2])
    n_bands = int(data[0].split()[4])
    
    if int(data[0].split()[6]) == 2:
        spin_pol = True
        bands = np.zeros((n_kpoints,n_bands+1,2),dtype=float)
    else:
        spin_pol = False
        bands = np.zeros((n_kpoints,n_bands+1,1),dtype=float)
    

    index = -1
    k_points = []
        
    for i,line in enumerate(data):
        m = re.match(r'^@ XAXIS TICK SPEC',line)
        if m:
            n_k = int(data[i].split()[4])
            #k points labels
            for n in range(i+1,i+n_k*2+1,2):
                k_points.append(float(data[n].split()[4]))
            #read band energy
            for j in range(i+n_k*2+3,n_kpoints+i+n_k*2+3):
                index += 1
                #dos[i-4,0:n_proj+1,0] = np.array([float(n) for n in data[i].split()])
                #bands[index] = np.array([float(n) for n in data[j].split()])
                #print(j,np.array([float(n) for n in data[j].split()]))
                bands[index,0:n_bands+1,0] = np.array([float(n) for n in data[j].split()])
            if spin_pol == True:
                index = -1
                for j in range(n_kpoints+i+n_k*2+28,n_kpoints*2+i+n_k*2+28):
                    index += 1
                    #print(j,np.array([float(n) for n in data[j].split()]))
                    bands[index,0:n_bands+1,1] = np.array([float(n) for n in data[j].split()])
            #print(bands[0:10,0,:])
            bands[:,1:,:] = bands[:,1:,:]*27.2114
            
            efermi = float(data[-1].split()[3])*27.2114
            if not_scaled == True:
                bands[:,1:,:] = bands[:,1:,:] + efermi
            #print(bands.shape)
            #print(bands[0:10,0,:])
            return bands, k_points, efermi

#plot_bands('data/es/BN4x4_CuAS_N_BAND.BAND',not_scaled=True)

def plot_dos(file_name,energy_range,not_scaled=False):
    import sys
    #from extract_info import fermi_energy
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .DOSS file needs to be specified')
        sys.exit(1)
    #plot from .DOSS file
    
    
        
    n_proj = int(data[0].split()[4])
    n_energy = int(data[0].split()[2])
    if int(data[0].split()[6]) == 2:
        spin_pol = True
        spin = 1
        dos = np.zeros((n_energy,n_proj+1,2),dtype=float)
    else:
        spin_pol = False
        spin = 0
        dos = np.zeros((n_energy,n_proj+1,1),dtype=float)
    #return(dos.shape)
    
    #for s in range(spin):
    for i in range(4,n_energy+4):
        dos[i-4,0:n_proj+1,0] = np.array([float(n) for n in data[i].split()])
    
    if spin_pol == True:
        index = -1 
        for i in range(n_energy+6,n_energy*2+6):
            index += 1
            dos[index,0:n_proj+1,1] = np.array([float(n) for n in data[i].split()])
            #print(index)
            #print(np.array([float(n) for n in data[i].split()]))

    dos[:,0,:] = dos[:,0,:]*27.2114
    
    efermi = float(data[n_energy+4].split()[3])*27.2114
    if not_scaled == True:
        dos[:,0,:] = dos[:,0,:]+efermi
    
    min_energy = next(x for x, val in enumerate(dos[:,0,0]) if val > energy_range[0])
    max_energy = next(x for x, val in enumerate(dos[:,0,0]) if val > energy_range[1])  

    max_dos = np.amax(dos[min_energy:max_energy,1:,:])  
    
    """
    # This part was to have all the pdos normalised to 1, but it doesn't make much sense
    
    max_dos = np.zeros((len(dos[0])-1))
    min_dos = np.zeros((len(dos[0])-1))
    for i in range(0,len(dos[0])-1):
        max_dos[i] = np.max(dos[min_energy:max_energy,i+1:])
        min_dos[i] = np.min(dos[min_energy:max_energy,i+1:])
    print('max_dos',max_dos)
    print('min_dos',min_dos)
    #print(dos[min_energy:max_energy,:1])
    for i in range(1,len(dos[0])):        
        dos[:,i] = ((dos[:,i]-min_dos[i-1])/(max_dos[i-1]-min_dos[i-1]))+(i-1)

    #dos[:,1] = (dos[:,1]/max_dos[0])
    #print(dos[0:10,1],max_dos[0])

    
    for i in range(0,len(dos[0])-1):
        max_dos[i] = np.amax(dos[min_energy:max_energy,:i+1])
        print(i,max_dos[i])
    
    print(max_dos)
    for i in range(1,len(dos[0])):
        dos[:,i] = (dos[:,i]/max_dos[i-1])+(i-1)
    """
    

    for i in range(1,len(dos[0])):
        if spin_pol == True:
            dos[:,i,0] = (dos[:,i,0]/max_dos)+(2*i-1)
            dos[:,i,1] = (dos[:,i,1]/max_dos)+(2*i-1)
        else:
            dos[:,i,0] = (dos[:,i,0]/max_dos)+(i-1)
        
        #change this to include both spins

    return dos, efermi   

#print(plot_dos('data/es/BN4x4_CuAS_N_DOSS.DOSS',energy_range=[-5,10]))

def plot_es(band_file_name,dos_file_name,k_labels,energy_range,dos_labels=False,title=False,not_scaled=False,spin_display='single'):   
    
    import matplotlib.pyplot as plt
    from plotting import plot_bands
    from plotting import plot_dos
    import matplotlib.lines as mlines
    
    CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
    bands, kpoints, efermi_band = plot_bands(band_file_name,not_scaled);
 
    if type(dos_file_name) == list:
        dos = plot_dos(dos_file_name[0],energy_range)
        dos_ao = plot_dos(dos_file_name[1],energy_range)
        x3 = dos_ao[:,0,:]
        y3 = dos_ao[:,1:-1,:]        
    else:
        dos, efermi = plot_dos(dos_file_name,energy_range,not_scaled)
                
    x1 = bands[:,0,:]
    y1 = bands[:,1:,:]
    #print(bands[0:10,0:5,0])

    x2 = dos[:,0,:]
    y2 = dos[:,1:,:]

    
    if spin_display == 'single':
        
        if type(dos_file_name) == list:
            fig, (ax1, ax2, ax3) = plt.subplots(1,3,gridspec_kw={'width_ratios': [2, 1, 1]})
        else:
            fig, (ax1, ax2) = plt.subplots(1,2,gridspec_kw={'width_ratios': [2, 1]})
        
            
        if len(dos[0,0,:]) > 1:  
            
            ax1.plot(x1[:,1], y1[:,:,1],'-',  c='red' )
            ax1.plot(x1[:,0], y1[:,:,0],'-' , c='black')   
            spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                         mlines.Line2D([], [], color='red', label='Beta')]
            ax1.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
        
        else:
            ax1.plot(x1[:,0], y1[:,:,0],'-', c='black' )
        
        
        if type(dos_file_name) == list:
            if dos_labels != False:
                labels = dos_labels
                for m in range(len(dos[0,0,:])):
                    for i in range(len(dos[0,1:-1])):
                        ax2.plot(y2[:,i,m],x2[:,m],'-', label=labels[0][i], color=CB_color_cycle[i])
                    ax2.plot(y2[:,i+1,m],x2[:,m],'-', label=labels[0][i], color='black')
                    ax2.legend(labels[0],bbox_to_anchor=(0.5, 1.0))
                for m in range(len(dos_ao[0,0,:])):
                    for j in range(len(dos_ao[0,1:-1])):
                        ax3.plot(y3[:,j,m],x3[:,m],'-', label=labels[1][j], color=CB_color_cycle[j+i+1])
                    ax3.legend(labels[1],bbox_to_anchor=(1, 1.0))
            else:
                for m in range(len(dos[0,0,:])):
                    for i in range(len(dos[0,1:])):
                        ax2.plot(y2[:,i,m],x2[:,m],'-', color=CB_color_cycle[i])
                for m in range(len(dos_ao[0,0,:])):
                    for j in range(len(dos_ao[0,1:-1])):
                        ax3.plot(y3[:,j,m],x3[:,m],'-', color=CB_color_cycle[j+i+1])
         #THIS IS THE PART I TESTED   
        else:
            if dos_labels != False:
                labels = dos_labels
                for m in range(len(dos[0,0,:])):
                    for i in range(len(dos[0,1:-1])):
                        ax2.plot(y2[:,i,m],x2[:,m],'-', label=labels[i], color=CB_color_cycle[i])
                    ax2.plot(y2[:,i+1,m],x2[:,m],'-', label=labels[-1], color='black')
                    ax2.legend(labels,bbox_to_anchor=(.99,.99))
            else:
                for m in range(len(dos[0,0,:])):
                    for i in range(len(dos[0,1:-1])):
                        ax2.plot(y2[:,i,m],x2[:,m],'-', color=CB_color_cycle[i])
                    ax2.plot(y2[:,i+1,m],x2[:,m],'-', color='black')
        
        #Display E Fermi on DOS
        if not_scaled == True:
            fermi_line = [[0, np.amax(dos[:,1:])+1],[efermi,efermi]] 
        else:
            fermi_line = [[0, np.amax(dos[:,1:])+1],[0,0]] 
    
        ax2.plot(fermi_line[0],fermi_line[1], '--',color='grey')
        
        #Display E Fermi on band structure
        if not_scaled == True:
            fermi_line = [[0, np.amax(bands[:,1:,0])+1],[efermi_band,efermi_band]] 
        else:
            fermi_line = [[0, np.amax(bands[:,1:,0])+1],[0,0]] 
        ax1.plot(fermi_line[0],fermi_line[1], '--',color='grey')
    
    ax1.set_title('Band structure', size = 18)
    ax1.set_xlabel('k point', size =12)
    if not_scaled == True:
        ax1.set_ylabel('E (eV)', size =12)
    else:
        ax1.set_ylabel('E-E Fermi (eV)', size =12)
    ax1.set_xticks(kpoints)
    ax1.set_xticklabels(k_labels, size=12)
    ax1.set_xlim([0, bands[-1,0,0]])
    ax1.set_ylim(energy_range)
    ax1.grid()

    ax2.set_title('Density of States \n(Atom proj)', size =18)
    ax2.set_xlabel('DOS (States/eV)', size = 12)
    ax2.set_xlim([0, np.amax(dos[:,1:]+1)])
    ax2.set_ylim(energy_range)
    ax2.yaxis.set_ticklabels([])
    ax2.grid()
    
    if type(dos_file_name) == list:
        ax3.set_title('Density of States \n(AO proj)', size =18)
        ax3.set_xlabel('DOS (States/eV)', size = 12)
        ax3.set_xlim([0, np.amax(dos[:,1:])])
        ax3.set_ylim(energy_range)
        ax3.yaxis.set_ticklabels([])
        ax3.grid()
        
    fig.set_size_inches(15, 8)
    if title != False:
        fig.suptitle(title, size=22)
        plt.subplots_adjust(wspace=0.2, top=0.88)

def plot_bs(band_file_name,k_labels,energy_range,title=False,not_scaled=False):
    
    import matplotlib.pyplot as plt
    from plotting import plot_bands
    import matplotlib.lines as mlines
    
    bands, kpoints, efermi_band = plot_bands(band_file_name,not_scaled);
    #print(efermi_band)
    
                
    x1 = bands[:,0,:]
    y1 = bands[:,1:,:]
    
    fig, ax1 = plt.subplots(1,1)
    
    if len(bands[0,0,:]) > 1:  
        
        ax1.plot(x1[:,1], y1[:,:,1],'-',  c='red' )
        ax1.plot(x1[:,0], y1[:,:,0],'-' , c='black')        
        #ax1.legend( bbox_to_anchor=(0.9, .75))
        spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                     mlines.Line2D([], [], color='red', label='Beta')]
        ax1.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
    
    else:
        ax1.plot(x1[:,0], y1[:,:,0],'-', c='black' )  
    
    #Display E Fermi on band structure
    if not_scaled == True:
        fermi_line = [[0, np.amax(bands[:,1:,0])+1],[efermi_band,efermi_band]] 
    else:
        fermi_line = [[0, np.amax(bands[:,1:,0])+1],[0,0]] 
        
    ax1.plot(fermi_line[0],fermi_line[1], '--',color='grey')
    ax1.set_title('Band structure', size = 18)
    ax1.set_xlabel('k point', size =12)
    ax1.set_ylabel('E-E Fermi (eV)', size =12)
    ax1.set_xticks(kpoints)
    ax1.set_xticklabels(k_labels, size=12)
    ax1.set_xlim([0, bands[-1,0,0]])
    ax1.set_ylim(energy_range)
    ax1.grid()
    
        
    fig.set_size_inches(8, 8)
    if title != False:
        fig.suptitle(title, size=22)
        plt.subplots_adjust(wspace=0.2, top=0.88)
        
def plot_doss(dos_file_name,energy_range,dos_labels=False,title=False,not_scaled=False):   
    
    import matplotlib.pyplot as plt
    from plotting import plot_bands
    from plotting import plot_dos
    import matplotlib.lines as mlines
    
    CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
 
    if type(dos_file_name) == list:
        dos = plot_dos(dos_file_name[0],energy_range)
        dos_ao = plot_dos(dos_file_name[1],energy_range)
        x3 = dos_ao[:,0,:]
        y3 = dos_ao[:,1:-1,:]        
    else:
        dos, efermi = plot_dos(dos_file_name,energy_range,not_scaled)
                
    x2 = dos[:,0,:]
    y2 = dos[:,1:,:]
   
    
        
    if type(dos_file_name) == list:
        fig, (ax2, ax3) = plt.subplots(2,1,gridspec_kw={'width_ratios': [1, 1]})
    else:
        fig, (ax2) = plt.subplots(1)
        
    if type(dos_file_name) == list:
        if dos_labels != False:
            labels = dos_labels
            for m in range(len(dos[0,0,:])):
                for i in range(len(dos[0,1:-1])):
                    ax2.plot(x2[:,m],y2[:,i,m],'-', label=labels[0][i], color=CB_color_cycle[i])
                ax2.plot(x2[:,m],y2[:,i+1,m],'-', label=labels[0][i], color='black')
                ax2.legend(labels[0],bbox_to_anchor=(0.5, 1.0))
            for m in range(len(dos_ao[0,0,:])):
                for j in range(len(dos_ao[0,1:-1])):
                    ax3.plot(x3[:,m],y3[:,j,m],'-', label=labels[1][j], color=CB_color_cycle[j+i+1])
                ax3.legend(labels[1],bbox_to_anchor=(1, 1.0))
        else:
            for m in range(len(dos[0,0,:])):
                for i in range(len(dos[0,1:])):
                    ax2.plot(x2[:,m],y2[:,i,m],'-', color=CB_color_cycle[i])
            for m in range(len(dos_ao[0,0,:])):
                for j in range(len(dos_ao[0,1:-1])):
                    ax3.plot(x3[:,m],y3[:,j,m],'-', color=CB_color_cycle[j+i+1])
     #THIS IS THE PART I TESTED   
    else:
        if dos_labels != False:
            labels = dos_labels
            for m in range(len(dos[0,0,:])):
                for i in range(len(dos[0,1:-1])):
                    ax2.plot(x2[:,m],y2[:,i,m],'-', label=labels[i], color=CB_color_cycle[i])
                ax2.plot(x2[:,m],y2[:,i+1,m],'-', label=labels[-1], color='black')
                ax2.legend(labels,bbox_to_anchor=(.99,.99))
        else:
            for m in range(len(dos[0,0,:])):
                for i in range(len(dos[0,1:-1])):
                    ax2.plot(x2[:,m],y2[:,i,m],'-', color=CB_color_cycle[i])
                ax2.plot(x2[:,m],y2[:,i+1,m],'-', color='black')
    
    
    #Display E Fermi on DOS
    if not_scaled == True:
        fermi_line = [[efermi,efermi],[0, np.amax(dos[:,1:])+1]] 
    else:
        fermi_line = [[0,0],[0, np.amax(dos[:,1:])+1]] 

    ax2.plot(fermi_line[0],fermi_line[1], '--',color='grey')
    
    
    '''ax1.set_title('Band structure', size = 18)
    ax1.set_xlabel('k point', size =12)
    if not_scaled == True:
        ax1.set_ylabel('E (eV)', size =12)
    else:
        ax1.set_ylabel('E-E Fermi (eV)', size =12)
    ax1.set_xticks(kpoints)
    ax1.set_xticklabels(k_labels, size=12)
    ax1.set_xlim([0, bands[-1,0,0]])
    ax1.set_ylim(energy_range)
    ax1.grid()'''

    ax2.set_title('Density of States \n(Atom proj)', size =18)
    ax2.set_xlabel('DOS (States/eV)', size = 12)
    ax2.set_ylim([0, np.amax(dos[:,1:]+1)])
    ax2.set_xlim(energy_range)
    ax2.xaxis.set_ticklabels([])
    ax2.yaxis.set_ticklabels([])
    ax2.grid()
    
    if type(dos_file_name) == list:
        ax3.set_title('Density of States \n(AO proj)', size =18)
        ax3.set_xlabel('DOS (States/eV)', size = 12)
        ax3.set_ylim([0, np.amax(dos[:,1:])])
        ax3.set_xlim(energy_range)
        ax3.xaxis.set_ticklabels([])
        ax3.grid()
        
    fig.set_size_inches(15, 8)
    if title != False:
        fig.suptitle(title, size=22)
        plt.subplots_adjust(wspace=0.2, top=0.88)
    
def compare_bs(band1_file_name,band2_file_name,k_labels,energy_range,title=False,not_scaled=False):
    import matplotlib.pyplot as plt
    from plotting import plot_bands
    import matplotlib.lines as mlines

    bands1, kpoints1, efermi1_band = plot_bands(band1_file_name,not_scaled)
    bands2, kpoints2, efermi2_band = plot_bands(band2_file_name,not_scaled)
 
 
    x1 = bands1[:,0,:]
    y1 = bands1[:,1:,:]

    x2 = bands2[:,0,:]
    y2 = bands2[:,1:,:]
     
    
    fig, (ax1, ax2) = plt.subplots(1,2,gridspec_kw={'width_ratios': [1, 1]})
    
    if len(bands1[0,0,:]) > 1:  
        
        ax1.plot(x1[:,1], y1[:,:,1],'-',  c='red' )
        ax1.plot(x1[:,0], y1[:,:,0],'-' , c='black')        
        spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                     mlines.Line2D([], [], color='red', label='Beta')]
        ax1.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
    else:
        ax1.plot(x1[:,0], y1[:,:,0],'-', c='black' )
        
    if len(bands2[0,0,:]) > 1:  
        
        ax2.plot(x2[:,1], y2[:,:,1],'-',  c='red' )
        ax2.plot(x2[:,0], y2[:,:,0],'-' , c='black')        
        spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                     mlines.Line2D([], [], color='red', label='Beta')]
        ax2.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
    else:
        ax2.plot(x2[:,0], y2[:,:,0],'-', c='black' )

    #Display E Fermi on band structure
    if not_scaled == True:
        fermi_line1 = [[0, np.amax(bands1[:,1:,0])+1],[efermi1_band,efermi1_band]] 
        fermi_line2 = [[0, np.amax(bands2[:,1:,0])+1],[efermi2_band,efermi2_band]] 
    else:
        fermi_line1 = [[0, np.amax(bands1[:,1:,0])+1],[0,0]] 
        fermi_line2 = [[0, np.amax(bands2[:,1:,0])+1],[0,0]] 
    ax1.plot(fermi_line1[0],fermi_line1[1], '--',color='grey')
    ax2.plot(fermi_line2[0],fermi_line2[1], '--',color='grey')
    
        
    ax1.set_title(str(band1_file_name), size = 18)
    ax1.set_xlabel('k point', size =12)
    if not_scaled == True:
        ax1.set_ylabel('E (eV)', size =12)
    else:
        ax1.set_ylabel('E-E Fermi (eV)', size =12)
    ax1.set_xticks(kpoints1)
    ax1.set_xticklabels(k_labels, size=12)
    ax1.set_xlim([0, bands1[-1,0,0]])
    ax1.set_ylim(energy_range)
    ax1.grid()
    
    ax2.set_title(str(band2_file_name), size = 18)
    ax2.set_xlabel('k point', size =12)
    if not_scaled == True:
        ax2.set_ylabel('E (eV)', size =12)
    else:
        ax2.set_ylabel('E-E Fermi (eV)', size =12)
    ax2.set_xticks(kpoints2)
    ax2.set_xticklabels(k_labels, size=12)
    ax2.set_xlim([0, bands1[-1,0,0]])
    ax2.set_ylim(energy_range)
    ax2.grid()
   
    fig.set_size_inches(15, 8)
    if title != False:
        fig.suptitle(title, size=22)
        plt.subplots_adjust(wspace=0.2, top=0.88)
    
    
def compare_es(band1_file_name,band2_file_name,dos1_file_name,dos2_file_name,k_labels,energy_range,dos_labels=False,title=False, not_scaled=False):   
    
    import matplotlib.pyplot as plt
    from plotting import plot_bands
    from plotting import plot_dos
    import matplotlib.lines as mlines
    
    CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
    
    bands1, kpoints1, efermi1_band = plot_bands(band1_file_name,not_scaled)
    bands2, kpoints2, efermi2_band = plot_bands(band2_file_name,not_scaled)
    
    dos1, efermi1 = plot_dos(dos1_file_name,energy_range,not_scaled)
    dos2, efermi2 = plot_dos(dos2_file_name,energy_range,not_scaled)
    
    x1 = bands1[:,0,:]
    y1 = bands1[:,1:,:]

    x2 = bands2[:,0,:]
    y2 = bands2[:,1:,:]
    
    x3 = dos1[:,0,:]
    y3 = dos1[:,1:,:]
    
    x4 = dos2[:,0,:]
    y4 = dos2[:,1:,:]
    
     
    fig, (ax1, ax3, ax2, ax4) = plt.subplots(1,4,gridspec_kw={'width_ratios': [2, 1,2, 1]})
    
    if len(bands1[0,0,:]) > 1:  
        
        ax1.plot(x1[:,1], y1[:,:,1],'-',  c='red' )
        ax1.plot(x1[:,0], y1[:,:,0],'-' , c='black')        
        spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                     mlines.Line2D([], [], color='red', label='Beta')]
        ax1.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
    else:
        ax1.plot(x1[:,0], y1[:,:,0],'-', c='black' )
        
    if len(bands2[0,0,:]) > 1:  
        
        ax2.plot(x2[:,1], y2[:,:,1],'-',  c='red' )
        ax2.plot(x2[:,0], y2[:,:,0],'-' , c='black')        
        spin_band = [mlines.Line2D([], [], color='black', label='Alpha'),
                     mlines.Line2D([], [], color='red', label='Beta')]
        ax2.legend(spin_band,['Alpha electrons', 'Beta electrons'],facecolor='white', framealpha=1,bbox_to_anchor=(.83,.90))
    else:
        ax2.plot(x2[:,0], y2[:,:,0],'-', c='black' )


    if dos_labels != False:
        labels = dos_labels
        for m in range(len(dos1[0,0,:])):
            for i in range(len(dos1[0,1:-1])):
                ax3.plot(y3[:,i,m],x3[:,m],'-', label=labels[i], color=CB_color_cycle[i])
            ax3.plot(y3[:,i+1,m],x3[:,m],'-', label=labels[-1], color='black')
            ax3.legend(labels,bbox_to_anchor=(.99,.99))
        for m in range(len(dos2[0,0,:])):
            for i in range(len(dos2[0,1:-1])):
                ax4.plot(y4[:,i,m],x4[:,m],'-', label=labels[i], color=CB_color_cycle[i])
            ax4.plot(y4[:,i+1,m],x4[:,m],'-', label=labels[-1], color='black')
            ax4.legend(labels,bbox_to_anchor=(.99,.99))
    else:
        for m in range(len(dos1[0,0,:])):
            for i in range(len(dos1[0,1:-1])):
                ax3.plot(y3[:,i,m],x3[:,m],'-', color=CB_color_cycle[i])
            ax3.plot(y3[:,i+1,m],x3[:,m],'-', color='black')
        for m in range(len(dos2[0,0,:])):
            for i in range(len(dos2[0,1:-1])):
                ax4.plot(y4[:,i,m],x4[:,m],'-', color=CB_color_cycle[i])
            ax4.plot(y4[:,i+1,m],x4[:,m],'-', color='black')
    
    #Display E Fermi on DOS
    if not_scaled == True:
        fermi_line1 = [[0, np.amax(dos1[:,1:])+1],[efermi1,efermi1]] 
        fermi_line2 = [[0, np.amax(dos2[:,1:])+1],[efermi2,efermi2]]
    else:
        fermi_line1 = [[0, np.amax(dos1[:,1:])+1],[0,0]] 
        fermi_line2 = [[0, np.amax(dos2[:,1:])+1],[0,0]] 

    ax3.plot(fermi_line1[0],fermi_line1[1], '--',color='grey')  
    ax4.plot(fermi_line2[0],fermi_line2[1], '--',color='grey') 
    
    #Display E Fermi on band structure
    if not_scaled == True:
        fermi_line1 = [[0, np.amax(bands1[:,1:,0])+1],[efermi1_band,efermi1_band]] 
        fermi_line2 = [[0, np.amax(bands2[:,1:,0])+1],[efermi2_band,efermi2_band]] 
    else:
        fermi_line1 = [[0, np.amax(bands1[:,1:,0])+1],[0,0]] 
        fermi_line2 = [[0, np.amax(bands2[:,1:,0])+1],[0,0]] 
    ax1.plot(fermi_line1[0],fermi_line1[1], '--',color='grey')
    ax2.plot(fermi_line2[0],fermi_line2[1], '--',color='grey')
            
    ax1.set_title('Band structure', size = 18)
    ax1.set_xlabel('k point', size =12)
    if not_scaled == True:
        ax1.set_ylabel('E (eV)', size =12)
    else:
        ax1.set_ylabel('E-E Fermi (eV)', size =12)
    ax1.set_xticks(kpoints1)
    ax1.set_xticklabels(k_labels, size=12)
    ax1.set_xlim([0, bands1[-1,0,0]])
    ax1.set_ylim(energy_range)
    ax1.grid()

    ax2.set_title('Band structure', size = 18)
    ax2.set_xlabel('k point', size =12)
    if not_scaled == True:
        ax2.set_ylabel('E (eV)', size =12)
    else:
        ax2.set_ylabel('E-E Fermi (eV)', size =12)
    ax2.set_xticks(kpoints2)
    ax2.set_xticklabels(k_labels, size=12)
    ax2.set_xlim([0, bands2[-1,0,0]])
    ax2.set_ylim(energy_range)
    ax2.grid()
    
    ax3.set_title('Density of States', size =18)
    ax3.set_xlabel('DOS (States/eV)', size = 12)
    ax3.set_xlim([0, np.amax(dos1[:,1:])+1])
    ax3.set_ylim(energy_range)
    ax3.yaxis.set_ticklabels([])
    ax3.grid()
    
    ax4.set_title('Density of States', size =18)
    ax4.set_xlabel('DOS (States/eV)', size = 12)
    ax4.set_xlim([0, np.amax(dos2[:,1:])+1])
    ax4.set_ylim(energy_range)
    ax4.yaxis.set_ticklabels([])
    ax4.grid()
    
    fig.set_size_inches(15, 8)
    
    if title != False:
        fig.suptitle(title, size=22)
        plt.subplots_adjust(wspace=0.2, top=0.88)
