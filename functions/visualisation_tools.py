"""
Created on Mon Apr 19 18:36:34 2021

@author: brunocamino

This script transforms an output .gui CRYSTAL file to a .cif file
usage: gui2cif filename.gui

TO DO: 
    - check on name of the input (gui or not)
    
TROUBLESHOOTING:
    - you need to restart the kernel to see the changes
    
"""
def gui2cif(file_name):
    import sys
    import math
    import numpy as np
    from mendeleev import element

    """   
    if file_name[-3] == 'gui':
        in_name = file_name[:-3]
    else:
        file_name = str(file_name) + '.gui'
        in_name = file_name
    """
    # Exit if the .gui file doesn't exist
    try: 
        file = open(file_name, 'r')
        in_name = str(file_name)
        data = file.readlines()
        file.close()
    except:
        print('EXITING: a .gui file needs to be specified')
        sys.exit(1)
    
    #Read the lattice vectors    
    vector_1 = np.array(data[1].split()).astype('float')
    vector_2 = np.array(data[2].split()).astype('float')
    vector_3 = np.array(data[3].split()).astype('float')
    
    #Lattice vector matrix
    lattice = np.array([vector_1,vector_2,vector_3])
    
    #Calculate the lattice vectors length
    vector_1_norm = np.linalg.norm(vector_1)
    vector_2_norm = np.linalg.norm(vector_2)
    vector_3_norm = np.linalg.norm(vector_3)
    if vector_1_norm > 300:
        vector_1_norm = 15
        lattice[0][0] = 15.
    if vector_2_norm > 300:
        vector_2_norm = 15
        lattice[1][1] = 15.
    if vector_3_norm > 300:
        vector_3_norm = 15.0000
        lattice[2][2] = 15.
    
    
    
    #Calculate the angles
    alpha = np.arccos(np.dot(vector_2/np.linalg.norm(vector_2),vector_3/np.linalg.norm(vector_3)))
    beta = np.arccos(np.dot(vector_1/np.linalg.norm(vector_1),vector_3/np.linalg.norm(vector_3)))
    gamma = np.arccos(np.dot(vector_1/np.linalg.norm(vector_1),vector_2/np.linalg.norm(vector_2)))
    
    #Read the number of symmops and number of atoms
    symmops = int(data[4].split()[0])
    n_atoms = int(data[5+symmops*4].split()[0])
    
    #Write the cif file
    out_name = str(file_name[:-4]+'.cif')
    with open(out_name, 'w') as file:
        file.writelines('###############################################################################\n')
        file.writelines('data_OPT_STEP_0\n')
        file.writelines('\n')
        file.writelines('_symmetry_space_group_name_H-M \'P 1\'\n')
        file.writelines('_cell_length_a '+ str(vector_1_norm)+'\n')
        file.writelines('_cell_length_b '+ str(vector_2_norm)+'\n')
        file.writelines('_cell_length_c ' + str(vector_3_norm)+'\n')
        file.writelines('_cell_angle_alpha '+ str(math.degrees(alpha)) + ' \n' )
        file.writelines('_cell_angle_beta '+ str(math.degrees(beta)) + ' \n' )
        file.writelines('_cell_angle_gamma ' + str(math.degrees(gamma)) + '\n' )
        file.writelines('\n')
        file.writelines('loop_ \n')
        file.writelines('_atom_site_label \n')
        file.writelines('_atom_site_fract_x \n')
        file.writelines('_atom_site_fract_y \n')
        file.writelines('_atom_site_fract_z \n')    
        for i in range(6+symmops*4,6+symmops*4+n_atoms):
            cart = np.array(data[i].split()[1::]).astype('float')
            frac = cart.dot(np.linalg.inv(lattice))
            file.writelines(element(int(data[i].split()[0])).symbol + ' ' + ' '.join(map(str, frac)) + '\n')
    

def out2cif(file_name,a,b,c,alpha,beta,gamma,atom_positions):
    dim = 3
    if float(c) > 300:
        c = 15.0 
        dim = 2
    if float(b) > 300:
        b = 15. 
        dim = 1
    if float(a) > 300:
        a = 15.
        dim = 0

    out_name = str(file_name[:-4]+'.cif')
    with open(out_name, 'w') as file:
            file.writelines('###############################################################################\n')
            file.writelines('data_OPT_STEP_0\n')
            file.writelines('\n')
            file.writelines('_symmetry_space_group_name_H-M \'P 1\'\n')
            file.writelines('_cell_length_a '+ str(a)+'\n')
            file.writelines('_cell_length_b '+ str(b)+'\n')
            file.writelines('_cell_length_c ' + str(c)+'\n')
            file.writelines('_cell_angle_alpha '+ str(alpha) + ' \n' )
            file.writelines('_cell_angle_beta '+ str(beta) + ' \n' )
            file.writelines('_cell_angle_gamma ' + str(gamma) + '\n' )
            file.writelines('\n')
            file.writelines('loop_ \n')
            file.writelines('_atom_site_label \n')
            file.writelines('_atom_site_fract_x \n')
            file.writelines('_atom_site_fract_y \n')
            file.writelines('_atom_site_fract_z \n')
            for i in range(len(atom_positions)):
                if dim ==3:
                    file.writelines(' '.join(atom_positions[i] + '\n'))    
                elif dim ==2 :
                    file.writelines(' '.join(atom_positions[i][0:3]) + ' '+  str(float(atom_positions[i][3])/c) + '\n')
                elif dim ==1 :
                    file.writelines(' '.join(atom_positions[i][0:2]) + ' '+  str(float(atom_positions[i][2])/b) +
                                    ' '+  str(float(atom_positions[i][3])/c) + '\n')
                elif dim ==0 :
                    file.writelines(' '.join(atom_positions[i][0]) + ' ' + str(float(atom_positions[i][1])/a) +
                                    ' '+  str(float(atom_positions[i][2])/b) +
                                    ' '+  str(float(atom_positions[i][3])/c) + '\n')
                
            """
            for i in range(6+symmops*4,6+symmops*4+n_atoms):
                cart = np.array(data[i].split()[1::]).astype('float')
                frac = cart.dot(np.linalg.inv(lattice))
                file.writelines(element(int(data[i].split()[0])).symbol + ' ' + ' '.join(map(str, frac)) + '\n')
            """


