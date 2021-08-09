#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 09:29:19 2021

@author: brunocamino
"""

def runcry(file_name):
    
    runcry_path = '/Users/brunocamino/crystal/runcry17'
    if runcry_path == None:
        return('Please set the runcry path before calling it')
    
    import subprocess
    import sys
    import re
    
    converged = False
    index = 0
    
    
    while converged == False:
        if index > 3:
            return None
        else:
            run_calc = '/Users/brunocamino/crystal/runcry17 ' + file_name
            process = subprocess.Popen(run_calc.split(), stdout=subprocess.PIPE, stderr= subprocess.PIPE)
            output, error = process.communicate()   
            index += 1
            try: 
                file = open(file_name+'.out', 'r')
                data = file.readlines()
                file.close()
            except:
                print('EXITING: a .out file needs to be specified')
                sys.exit(1)
            for i,line in enumerate(data[::-1]):  
                if re.match(r'^ EEEEEEEEEE TERMINATION',line) != None:
                    converged = True
                    return '%s.out calculation successfully completed' % file_name

    

def runprop(prop_name,wf_file):
    
    runprop_path = '/Users/brunocamino/crystal/runprop17'
    if runprop_path == None:
        return('Please set the runprop path before calling it')
    
    import subprocess
    import sys
    import re
    
    converged = False
    
    while converged == False:
        index = 0
        if index > 3:
            return None
        else:
            run_calc = '/Users/brunocamino/crystal/runprop17 ' + prop_name + ' ' + wf_file
            process = subprocess.Popen(run_calc.split(), stdout=subprocess.PIPE, stderr= subprocess.PIPE)
            output, error = process.communicate()   
            index += 1
            try: 
                file = open(prop_name+'.outp', 'r')
                data = file.readlines()
                file.close()
            except:
                print('EXITING: a .out file needs to be specified')
                sys.exit(1)
            for i,line in enumerate(data[::-1]):  
                if re.match(r'^ EEEEEEEEEE TERMINATION',line) != None:
                    converged = True


def clean_wf(path,file_name):
    import subprocess
    from os.path import join
    
    directory = path
    input_name = file_name[:-4]
    file_path = join(directory,input_name)
    clean_folder = 'rm ' + file_path + '.f*' 
    process = subprocess.Popen(clean_folder.split(), stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    output, error = process.communicate()

def vesta(file_name):
    
    vesta_path = '/Applications/VESTA/VESTA.app/Contents/MacOS/VESTA'
    if vesta_path == None:
        return('Please set the vesta path before calling it')
    
    import subprocess
    '''import psutil
    
    vesta_is_open = False
    for proc in psutil.process_iter():
        if 'vesta' in proc.name().lower():
            vesta_is_open = True 
    if vesta_is_open == False:
        open_vesta = vesta_path 
        import os
        os.spawnl(os.P_DETACH, open_vesta)
        print(open_vesta)
        process = subprocess.Popen(open_vesta.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()  '''
    
    run_vesta = vesta_path + ' ' + file_name
    process = subprocess.Popen(run_vesta.split(), stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    output, error = process.communicate()   
    