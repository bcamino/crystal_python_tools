#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:18:00 2021

@author: brunocamino
"""
def read_input(file_name):
    import sys
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .d12 file needs to be specified')
        sys.exit(1)
    end_index = [i for i, s in enumerate(data) if "END" in s]
    

    if len(end_index) == 4:
        geom_block = data[:end_index[0]+1]
        optgeom_block = []
        bs_block = data[end_index[0]+1:end_index[1]+1]
        func_block = data[end_index[1]+1:end_index[2]+1]
        scf_block = data[end_index[2]+1:]
    elif len(end_index) == 5:
        geom_block = data[:end_index[0]+1]
        optgeom_block = data[end_index[0]+1:end_index[1]+1]
        bs_block = data[end_index[1]+1:end_index[2]+1]
        func_block = data[end_index[2]+1:end_index[3]+1]
        scf_block = data[end_index[3]+1:]
    """
    print(geom_block)
    print(optgeom_block)
    print(bs_block)
    print(func_block)
    print(scf_block)
    """
    
    return(geom_block,optgeom_block,bs_block,func_block,scf_block)

def write_input(file_name,geom_block,bs_block,func_block,scf_block, optgeom_block=[]):
    import itertools
    
    with open(file_name, 'w') as file:
        cry_input = list(itertools.chain(geom_block,optgeom_block,bs_block,
                                         func_block,scf_block))
        for line in cry_input:
            file.writelines(line)

def write_geom(dimensionality,): 
    pass        

def write_bs(basis_sets):
    import pickle
    
    bs_block = []
    try:    
        bs_dict_save = open("../files/bs_dict.pkl", "rb")
    except:
        bs_dict_save = open("../../files/bs_dict.pkl", "rb")
    bs_dict = pickle.load(bs_dict_save) #This dictionary contains all the basis sets
    for i in basis_sets:
        bs_block += [s + '\n' for s in bs_dict[i].split("\r\n")]
    
    bs_block += ['99 0\n','ENDBS\n']
    
    return(bs_block)

def extract_last_geom(file_name, print_cart=False):
    import sys
    import re
    from visualisation_tools import out2cif
    from mendeleev import element
    import numpy as np
    
    try: 
        file = open(file_name, 'r')
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .out file needs to be specified')
        sys.exit(1)

    for i,line in enumerate(data[::-1]):
        m = re.match(r'^ T = ATOM BELONGING TO THE ASYMMETRIC UNIT',line)
        if m:
            n_atoms = data[len(data)-i-3].split()[0]
            atom_positions = []       
            for j in range(int(n_atoms)):
                atom_line = data[len(data)-i-2-int(n_atoms)+j].split()[3:]
                atom_positions.append(atom_line)
            a,b,c,alpha,beta,gamma = data[len(data)-i-2-int(n_atoms)-5].split()
            out2cif(file_name,a,b,c,alpha,beta,gamma,atom_positions)
            out_name = str(file_name[:-4]+'.cif')
            atomic_numbers = []
            for atom in atom_positions:    
                atomic_numbers.append(element(atom[0].capitalize()).atomic_number)
            atoms = np.array(atom_positions)
            
            print('File %s written' % (out_name))
            
            if print_cart == True:
                print('\n Cartesian coordinates:\n')
                atoms[:,0] = atomic_numbers
                if float(a) < 500:
                    atoms[:,1] = atoms[:,1].astype('float')*float(a)
                if float(b) < 500:
                    atoms[:,2] = atoms[:,2].astype('float')*float(b)
                if float(c) < 500:
                    atoms[:,3] = atoms[:,3].astype('float')*float(c)
                
                for i in atoms:
                    print(' '.join(i))
            return None
        

    
#print(extract_last_geom('BN4x4_CuNP2_N.out')   ) 

    
