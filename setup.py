from distutils.core import setup

setup(name='sim_xps_spectra',
	  version='1.0',
	  author='Richard Fogarty',
	  author_email = 'richard.m.fogarty@gmail.com',
	  packages = ['sim_xps_spectra','sim_xps_spectra.gen_spectra','sim_xps_spectra.broad_functs', 'sim_xps_spectra.plotters',
	              'sim_xps_spectra.mol_spectra', 'sim_xps_spectra.x_sections', 'sim_xps_spectra.shared', 'sim_xps_spectra.parsers']
	 )

