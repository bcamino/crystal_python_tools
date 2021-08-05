#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 18:20:06 2021

@author: brunocamino
TO DO: 
    - think of a better algorithm to print based on the dimensionality
"""
#from crystal_io import read_input
import re

#def make_supercell(file_name,expansion_matrix,geom_block=[]):
def make_supercell(geom_block,scf_block,expansion_matrix):
    
    #if len(geom_block) == 0:
        #geom_block = read_input(file_name)[0]
    
    #scf_block = read_input(file_name)[4]
    
    # Create the supercell block
    scel_block = ['SUPERCEL\n']            
    if 'CRYSTAL' in geom_block[1]:
        dim = 3
    elif 'SLAB' in geom_block[1]:
        dim = 2
    elif 'POLYMER' in geom_block[1]:
        dim = 1
    
    for i in range(0,dim): 
        s = (expansion_matrix[i*dim:i*dim+dim])   
        scel_block += [(' '.join([str(elem) for elem in s]))+str('\n')]
    if dim == 3:
        geom_block[int(geom_block[5])+6:int(geom_block[5])+6] = scel_block
    else:
        geom_block[int(geom_block[4])+5:int(geom_block[4])+5] = scel_block
    for i, line in enumerate(scf_block):
        m = re.match(r'SHRINK',line)
        if m:
           s1 = (int(scf_block[i+1].split()[0])//int(expansion_matrix[0])) 
           s2 = (int(scf_block[i+1].split()[1])//int(expansion_matrix[0])) 
           scf_block[i+1] = str(s1) + '  '+ str(s2)+'\n'
           #scf_block[i+1] = ' '.join([int(scf_block[i+1][0])//expansion_matrix[0], int(scf_block[i+1][1])//expansion_matrix[0]])    
           #print()
    return geom_block, scf_block



def insert_atom(geom_block,atomic_number,coordinates):
    #start with sa and think about multiple atoms
    # it could be an array or list of type and list of coord
    
    atom_inse_block = ['ATOMINSE\n',str(len(atomic_number))+'\n']
    for i in range(len(atomic_number)):
        atom_inse_block += [str(atomic_number[i])+' '+' '.join([str(i) for i in coordinates[i]])+str('\n')]
        #s = str(atomic_number[i])+' ' + str(coordinates[i])
        #atom_inse_block += [(''.join([str(elem) for elem in s]))+str('\n')]
    
    if 'CRYSTAL' in geom_block[1]:
        n_atoms = int(geom_block[5])
        end_coord = n_atoms + 6
    else:
        n_atoms = int(geom_block[4])
        end_coord = n_atoms + 5
    
    if 'SUPERCEL' in geom_block[end_coord] :
        # This takes into account how many lines to skip 
        # if a supercell is created
        if 'CRYSTAL' in geom_block[1]:
            pos = end_coord + 4 
        else:
            pos = end_coord + 3
    else:
        pos = end_coord
    geom_block[pos:pos] = atom_inse_block
    
    return geom_block


#def remove_atom(file_name,atoms_index,geom_block=[]):
def remove_atom(geom_block,atoms_index):
    #start with sa and think about multiple atoms
    # it could be an array or list of type and list of coord
    #if len(geom_block) == 0:
        #geom_block = read_input(file_name)[0]
    
    atom_remo_block = ['ATOMREMO\n',str(len(atoms_index))+'\n']
    atom_remo_block += [(' '.join([str(elem) for elem in atoms_index]))+str('\n')]
    
    if 'SUPERCEL\n' in geom_block:#[int(geom_block[4])+5] :
        # This takes into account how many lines to skip 
        # if a supercell is created
        if 'CRYSTAL\n' in geom_block[1]:
            pos = int(geom_block[5])+ 4 + len(geom_block[int(geom_block[5])+ 7])
        else:
            pos = int(geom_block[4])+ 4 + len(geom_block[int(geom_block[4])+ 5])     
    else:
        if 'CRYSTAL\n' in geom_block[1]:
            pos = int(geom_block[5])+6
        else:
            pos = int(geom_block[4])+5
    geom_block[pos:pos] = atom_remo_block
    
    return geom_block


def substitute_atom(geom_block,replaced_atom,atomic_number):
    #start with sa and think about multiple atoms
    # it could be an array or list of type and list of coord
    #if len(geom_block) == 0:
        #geom_block = read_input(file_name)[0]
    
    atom_rep_block = ['ATOMSUBS\n',str(len(atomic_number))+'\n']
    for i in range(len(atomic_number)):
        s = replaced_atom[i] + ' ' +atomic_number[i] 
        atom_rep_block += [(''.join([str(elem) for elem in s]))+str('\n')]
    
    if 'SUPERCEL\n' in geom_block:
        # This takes into account how many lines to skip 
        # if a supercell is created
        if 'CRYSTAL\n' in geom_block[1]:
            pos = int(geom_block[5])+ 4 + len(geom_block[int(geom_block[5])+ 7])
        else:
            pos = int(geom_block[4])+ 4 + len(geom_block[int(geom_block[4])+ 6])      
    else:
        if 'CRYSTAL\n' in geom_block[1]:
            pos = int(geom_block[5])+6
        else:
            pos = int(geom_block[4])+5
    geom_block[pos:pos] = atom_rep_block
    
    return geom_block

def displace_atom(geom_block,displaced_atom,coordinates):
    #start with sa and think about multiple atoms
    # it could be an array or list of type and list of coord
    #if len(geom_block) == 0:
        #geom_block = read_input(file_name)[0]
    
    atom_rep_block = ['ATOMDISP\n',str(len(displaced_atom))+'\n']
    for i in range(len(displaced_atom)):
        #s = displaced_atom[i] + ' ' +coordinates[i] 
        #atom_rep_block += [(''.join([str(elem) for elem in s]))+str('\n')]
        atom_rep_block += [str(displaced_atom[i])+' '+' '.join([str(i) for i in coordinates[i]])+str('\n')]
    
    """if 'SUPERCEL' in geom_block[int(geom_block[4])+5] :
        # This takes into account how many lines to skip 
        # if a supercell is created
        pos = int(geom_block[4])+ 4 + len(geom_block[int(geom_block[4])+ 6])        
    else:
        pos = int(geom_block[4])+5
    geom_block[pos:pos] = atom_rep_block"""
    
    if 'CRYSTAL' in geom_block[1]:
        n_atoms = int(geom_block[5])
        end_coord = n_atoms + 6
    else:
        n_atoms = int(geom_block[4])
        end_coord = n_atoms + 5
    
    if 'ATOMINSE\n' in geom_block:
        pos = int(geom_block.index('ATOMINSE\n'))+int(geom_block[int(geom_block.index('ATOMINSE\n'))+1])+2    
    elif 'SUPERCEL' in geom_block[end_coord] :
        # This takes into account how many lines to skip 
        # if a supercell is created
        pos = end_coord + 4       
    else:
        pos = end_coord
    
    geom_block[pos:pos] = atom_rep_block
    
    return geom_block


#print(substitute_atom('BN.d12',['1','2'],['23','24']))
#print(displace_atom('BN.d12',['1'],['0.2 0.24 0.2']))
