<h2>Installation guide</h2>

We recommend the use of <a href='https://docs.conda.io/en/latest/miniconda.html'>conda</a>. Conda is a package, dependency and environment management system. This means it will take care of installing and linking all the packages needed to run the notebooks. Furthermore, it will ensure that the right version of such packages is used.

<h3>Install miniconda</h3>
If you are familiar with conda skip this section.

Download miniconda from this <a href='https://docs.conda.io/en/latest/miniconda.html'>link</a>. Follow the instructions and you will create a folder in your home directory called miniconda. This folder will contain all the environments and packages.

<h3>Packages required</h3>
You can create the environment to run the notebooks by installing this <a href='files/cpt.yml'>yml file</a>
. Download the file and type the following command in the folder where the file is saved:
<br>
<br>
<i>conda env create -f cpt.yml</i>
<br>
<br>
This will download all the packages and create the dependencies that you will need to run the notebooks.

 If you would like to install the packages manually please refer to the list of packages contained in the yml file.

To activate the environment use:

<i>conda activate cpt</i>

You will need to run this command every time you shut down the terminal where you are working.

<h3>Download crystal_python_tools</h3>
You can download the repository by clicking on the green button above and download the zip file or type the following on your command line:
<br>
<br>
<i>gh repo clone bcamino/crystal_python_tools</i>
<br>
<br>
To run the notebooks type:

 <i>jupyter notebook</i>

 this will open a browser window where you can navigate to the folder where the notebooks are saved.
