<h1>crystal_python_tools</h1>

This repository contains python tools to be used with the electronic structure code [CRYSTAL](https://www.crystal.unito.it/index.php).

<h3>Installation</h3>

For a comprehensive installation guide please refer to this <a href='installation_guide.md'>document</a>.


<h3>The problem/need this project addresses</h3>

This project was developed for both the experienced and non experienced python users and keeping in mind ease of use.

There are several fantastic python projects assisting computational chemists and material scientists in the interface and automatisation of simulations. For example, [ASE](https://wiki.fysik.dtu.dk/ase/) and [pymatgen](https://pymatgen.org/index.html). However, they require some level of fluency in python.

The goal of this repository is simple, but hopefully appreciated by the CRYSTAL users that despite being fluent in unix, do not master python.

<h3>Structure of the project</h3>
<ul>
  <li><b>Workflows</b> (jupyter notebook): these consist of a set of operation/calculations that are usually performed in a sequence. By setting few variables at the notebook, the user will be able to run a series of tasks, such as most of the convergence tests usually performed when starting to study a new material.
    <ul>
      <li>Convergence tests</li>
      <li>Electronic structure</li>
      <li>Surface adsorption</li>
      <li>Surface projected bulk band structure</li>
      <li>Structure manipulation</li>
    </ul>
  </li>
  <li><b>Building blocks</b> (jupyter notebook): these consist of a single task, such as testing the k point convergence.
   <ul>
       <li>basis set</li>
       <li>functional choice</li>
       <li>grid size convergence</li>
       <li>k point convergence</li>
       <li>sample adsorption sites</li>
       <li>sample surface</li>
       <li>tolinteg convergence</li>           
   </ul>
   <li> <b>Functions</b> (python files): these are the foundation upon which the whole repository is built. They perform the core tasks made available in a user friendly way in the jupyter notebooks.
    <ul>
      <li>settings</li>
      <li>crystal_io</li>
      <li>extract info</li>
      <li>geom modification</li>
      <li>spbs</li>
      <li>visualisation tools</li>
      <li>plotting</li>      
    </ul>
  </li>
</ul>

For a complete list of the different tasks that can be performed in the jupyter notebooks and functions, please refer to the picture below.
![repository_structure](images/repository_structure.jpg)

<h3>Recommended usage</h3>

If you are not too familiar with python I recommend to only interact with the notebooks. These offer a variety of tasks and only require you to fill the variable section and run the cells you need.

I would recommend to use the repository as follows:
<ul>
  <li>
  if it is the very first time you are using the repository on a machine, modify and run the <i>Settings</i> notebook. In this notebook you will need to specify the path to your runcry and runprop scripts (downloadable from the this <a href="http://tutorials.crystalsolutions.eu/tutorial.html?td=others&tf=howtorun">link</a>). In addition, please add the path to <a href='https://jp-minerals.org/vesta/en/'>VESTA</a> in order to be able to visualise structures.
  </li>
  <li>
  make a copy of the workflow or the building_blocks folder (or both folders if you plan to use both). Call the copied folders with a name that describes what you are researching, such as Ti02_water_splitting. It's important the folders are still in the crystal_python_tools folder;
  </li>
  <li>
  fill the variable cell for each workflow/building_block you intend to use and enjoy the ease of running the notebook and having all your results analysed in a single place
  </li>
</ul>

<h3>Examples</h3>
If this is your first time using the crystal_python_tools or if you need a refresher, please have a look at the <b>examples</b> folder. In there you will find all the workflows and building_blocks run by using (mostly) MgO, a CRYSTAL all time favourite. These notebooks also include some extra explanations. Please do not copy these for production purposes since some of the parameters had to be modified to take into account the fact they are in the <b>examples</b> folder.

<h3>Running the calculations</h3>

Throughout the whole project the idea is that you will start by having an initial input (file_name.d12). You will be required to input this name and the directory name in the jupyter notebooks. In this step, it's important to remember the structure of the repository. For example, if your input is in the /data folder and your jupyter notebook is in /workflows, the directory = '../data'.
The initial input is read by the notebooks and stored in different blocks (geom_block, scf_block, etc.). The ntebooks work on this objects and at the end they are written to a different input. This way, you can keep a basic input, for example mgo.d12, which is just the bulk, keep reading that input and perform different tasks.

In terms of performing the calculations, the notebooks offer three options:
<ul>
  <li>
  <b>run = True</b>: the notebook will create the inputs, run the calculations and analyse the outputs. You can use this option if the CRYSTAL executable is installed on the machine were you are running the notebooks;
  </li>
  <li>
  <b>run = False</b>: the notebook will create the inputs, but will not run the calculations. This is the option to use if the CRYSTAL executable is not installed on your machine or if the computing requirements exceed the ones of the machine were you are running the notebook;
  </li>
  <li>
  <b>run = 'Analyse'</b>: the notebook will analyse the outputs present in the specified directory. This is the option to use if the calculations were performed on a different machine (for example a super computer) and you are analysing the results on your local machine. If you intend to use this option, we recommend to generate the inputs by using run = False in order to have a consistent naming structure that is then recognised by run = 'Analyse'.
  </li>
  </ul>

  <b>Future development</b>

  The first verion of this project was released on August 2021.The choice of the tasks permormed by the notebooks was dictated by the research project I was carrying out at the time. However, there are many more ways these notebooks could assist researcher in running CRYSTAL calculations.

  At the moment, I am working on the following aspects:
  <ul>
  <li>spbs: plotting the surface (slab) band structure in order to highlight the surface states;</li>
  <li>surface adsorption: sample different adsorption sites;</li>
  <li>generate input from scratch;</li>
  <li>adsorption of a molecule on a nanoparticle</li>
  </ul>

  If you would like to be involved or have suggestions about future developments, please get in touch (camino.bruno@gmail.com).
