# sim_xps_spectra
Code to simulate XPS spectra. For now the only user interface is the run_gelius_for_mlinpt_folder.py script. Written in python 3.X.

# Installation instructions (Linux)
1) Install numpy and matplotlib dependencies (e.g. "pip install numpy --user", "pip install  matplotlib --user")
2) Install gen_basis_helpers dependency
  - git clone https://github.com/RFogarty1/plato_gen_basis_helpers.git
  - Navigate to the cloned directory 
  - python setup.py install --user
  - Note theres no need for this to pass all its tests (assuming it only fails due to import errors) since we only need a very small part of this code.
3) Install this repo
  - git clone https://github.com/RFogarty1/sim_xps_spectra.git
  - Navigate to the cloned directory
  - Modify the sim_xps_spectra/shared/config_vars.py BASE_DATA_DIR_PATH variable to point to wherever you cloned the repo to
  - python setup.py install --user
4) Run the tests
  - cd test
  - python run_all_unit_tests.py
5) Check the help message on the run_gelius_for_mlinpt_folder.py for instructions on how to run, or look at the windows instructions below
  - Navigate to the clone directory
  - cd scripts/
  - python run_gelius_for_mlinpt_folder.py -h
 
# Installation instructions (Windows, without linux subsystem)
In this section I'm going to assume you dont even have python or git installed in any way.

1) First we need to install python3.
  - https://www.python.org/downloads/release/python-381/
  - You probably want the Windows x86 executable installer
  - When installing, make sure you tick the box "add python to PATH"
2) Install numpy/matplotlib dependencies
  - Open either command prompt or powershell
  - pip install numpy --user
  - pip install matplotlib --user
3) Install git. There are multiple ways this could be done but im going to use github desktop in these instructions
  - Download and install from from https://desktop.github.com/
4) Install the gen_basis_helpers dependency
  - Launch GitHub Desktop
  - Go to File->clone a repository
  - enter "https://github.com/RFogarty1/plato_gen_basis_helpers.git" in the URL tab under Repository URL
  - Download/clone repository
  - Navigate to the folder containing the repository, there should be a "Show in explorer" button appeared in github desktop
  - Once in the folder (using windows explorer) go to File->open windows powershell
  - Type "python setup.py install --user" (Without the quotation marks)
5) Install the sim_xps_code
  - Launch github desktop
  - Go to File->Clone a repository
  - The url this time is "https://github.com/RFogarty1/sim_xps_spectra"
  - Navigate to the repository (sim_xps_spectra) we just downloaded
  - Edit the sim_xps_spectra\shared\config_vars.py file and set "BASE_DATA_DIR_PATH" to the path to your github dir. For example mine happened to be BASE_DATA_DIR_PATH = r"C:\Users\polic\Documents\GitHub\sim_xps_spectra". Note we need the r in front of the quotation marks when using windows file paths to tell python not to treat the backslashes as a special escape character
  - This file editing is needed to tell the code where to find cross-sections, it will need repeating each time you update the code
  - Open the repository directory in powershell
  - python setup.py install --user
  - Navigate to sim_xps_spectra\test
  - Run the tests using "python run_all_unit_tests.py"
  - The output should be something like:
----------------------------------------------------------------------
Ran 36 tests in 0.043s

OK

6) Updating code (will add later)


# Using the code (Windows, mostly transferable)



