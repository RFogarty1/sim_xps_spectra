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
  - Edit the sim_xps_spectra\shared\config_vars.py file and set "BASE_DATA_DIR_PATH" to the path to your cloned directory. For example mine happened to be BASE_DATA_DIR_PATH = r"C:\Users\polic\Documents\GitHub\sim_xps_spectra". Note we need the r in front of the quotation marks when using windows file paths to tell python not to treat the backslashes as a special escape character
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

1) Run the example code
  - Go to Examples\cmd_line\bmim_scn folder
  - Open the run_commands file with a text editor (notepad will do)
  - Each line represents the command to create 1 spectrum, but in linux. To swap to windows commands we need to replace forward slashes with back slashes
  - Open powershell in this directory
  - type each of the run commands with slashes changed, e.g.
  "python ..\..\..\scripts\run_gelius_for_mlinpt_folder.py . -fwhm 0.8"
  
 2) More generally
   - The overall synatx is "python <PATH_TO_SCRIPT> <PATH_TO_FOLDERS_TO_RUN_ON> <SIMULATION_OPTIONS>"
   - The example code uses relative paths, meaning the commands will only work if you type them from within the correct directory
  - To run the code from anywhere you need to use absolute paths
  - PATH_TO_SCRIPT is the localtion of the file run_gelius_for_mlinpt_folder.py, mine happens to be
"C:\Users\polic\Documents\GitHub\sim_xps_spectra\scripts\run_gelius_for_mlinpt_folder.py"
  - PATH_TO_FOLDERS_TO_RUN_ON represents paths to folders containing the *MLinpt.txt files used to generated spectra. In my case the absoulte path to the folder used in the example would be
"C:\Users\polic\Documents\GitHub\sim_xps_spectra\Examples\cmd_line\bmim_scn"
  -  <SIMULATION_OPTIONS> determine how the spectrum will be simulated. At minimum you need -fwhm set
  - If you only set fwhm, then a density of states will be simulated (no cross-sections used)
  - If you only set fwhm and hv (photon energy) then the effect of the emission angle will be ignored (this would be simulate a spectrum calculated at the magic angle, which is about 55 degrees)
  - If you set fwhm, hv and angle then you will get a simulated spectrum which accounts for angular-dependence of the cross-sections
  
# Important notes on cross-sections

1) The default cross-sections are the Yeh-Lindau values, which were obtained from https://vuo.elettra.eu/services/elements/WebElements.html. In turn this site lists as sources "J.J. Yeh, Atomic Calculation of Photoionization Cross-Sections and Asymmetry Parameters, Gordon and Breach Science Publishers, Langhorne, PE (USA), 1993 and from J.J. Yeh and I.Lindau, Atomic Data and Nuclear Data Tables, 32, 1-155 (1985). "

2) These cross-sections do not cover polarisation functions, for example d-orbitals on an oxygen atom. In these cases the Yeh-Lindau database object is set to return cross-sections for a lower angular momentum, e.g. O2p cross section for the O2d orbital. This isnt hard to change if calling the code through your own python scripts, but cant currently be changed from the command line interface.

3) Spectra can currently only be calculated at the photon energy where cross-sections are tabulated for all elements involved. If you enter a photon energy where we dont have the tabulated value (e.g. 1482.34 eV) then the spectrum will be calculated using the nearest photon energy available (1486.6 eV in this example). The name of the output folder will encode the photon energy ACTUALLY used to calculate the spectrum.


