#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 16:00:02 2021

@author: brunocamino
"""

def final_energy(file_name):
    import sys
    import re
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .out file needs to be specified')
        sys.exit(1)
    for i,line in enumerate(data[::-1]):  
        if re.match(r'^ EEEEEEEEEE TERMINATION',line) != None:
            for j,line1 in enumerate(data[len(data)-i::-1]):
                if re.match(r'\s\W OPT END - CONVERGED',line1) != None:
                    return float(line1.split()[7])*27.2114
                elif re.match(r'^ == SCF ENDED',line1) != None:
                    return float(line1.split()[8])*27.2114
                

#print(final_energy('data/BN_4x4.out'))
#print(final_energy('data/Cu.out'))

def fermi_energy(file_name):
    import sys
    import re
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .out file needs to be specified')
        sys.exit(1)
    
    for i,line in enumerate(data[::-1]):        
        if re.match(r'^ EEEEEEEEEE TERMINATION',line) != None:
            #This is in case the .out is from a BAND calculation
            if re.match(r'^ TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT BAND',data[len(data)-(i+4)]) != None:
                for j,line1 in enumerate(data[len(data)-i::-1]):
                    if re.match(r'^ ENERGY RANGE ',line1):
                        return float(line1.split()[7])*27.2114  
            #This is in case the .out is from a DOSS calculation  
            if re.match(r'^ TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT DOSS',data[len(data)-(i+4)]) != None:
                for j,line1 in enumerate(data[len(data)-i::-1]):
                    if re.match(r'^ N. OF SCF CYCLES ',line1):
                        return float(line1.split()[7])*27.2114    
            #This is in case the .out is from a sp/optgeom calculation
            else:      
                for j,line1 in enumerate(data[:i:-1]):
                    if re.match(r'^   FERMI ENERGY:',line1) != None:
                        return float(line1.split()[2])*27.2114
    else:
        return None

#print(fermi_energy('data/es/BN5x5_CuNP2_N.out_SAVE'))

def primitive_lattice(file_name):
    
    import sys
    import re
    import numpy as np
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .out file needs to be specified')
        sys.exit(1)
    
    lattice = []
    for i,line in enumerate(data):
        if re.match(r'^ DIRECT LATTICE VECTORS CARTESIAN',line) != None:
            for j in range(i+2,i+5):
                lattice_line = [float(n) for n in data[j].split()]
                lattice.append(lattice_line)
                
            return np.array(lattice)


def band_gap(file_name,spin_pol=False):
    import sys
    import re
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .out file needs to be specified')
        sys.exit(1)
    
    for i,line in enumerate(data[::-1]): 
        if re.match(r'^ EEEEEEEEEE TERMINATION',line) != None:
            for j,line1 in enumerate(data[len(data)-i::-1]):
                if spin_pol == False:
                    if re.match(r'^   BAND GAP',line1) != None:
                        return float(line1.split()[2])
                    elif re.match(r'^\s\w+ ENERGY BAND GAP',line1) != None:
                        #print(line1,j,len(data)-i+j)
                        return float(line1.split()[4])
                    elif re.match(r'^ POSSIBLY CONDUCTING STATE',line1) != None:
                        return 'Metal'
                else:
                    if re.match(r'^   BETA BAND GAP',line1) != None:
                        return [float(data[len(data)-i-j-1].split()[3]),float(line1.split()[3])]
                    elif re.match(r'^\s\w+ ENERGY BAND GAP',line1) != None:
                        return [float(data[len(data)-i-j-7].split()[4]),float(line1.split()[4])]

#print(band_gap('../results/BN4x4_CuSA_h.out',spin_pol=True))

def reciprocal_lattice(file_name):
    import sys
    import re
    import numpy as np
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .out file needs to be specified')
        sys.exit(1)
    
    lattice = []
    for i,line in enumerate(data):
        if re.match(r'^ DIRECT LATTICE VECTORS COMPON. \(A.U.\)',line) != None:
            for j in range(i+2,i+5):
                lattice_line = [float(n)/0.52917721067121 for n in data[j].split()[3:]]
                lattice.append(lattice_line)
            return np.array(lattice)

                
                
#print(primitive_lattice('data/BN_4x4.out'))
#print(band_gap('data/BN4x4_CuAS_N.out'))