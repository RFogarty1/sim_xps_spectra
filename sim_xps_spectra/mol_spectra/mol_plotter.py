
import sim_xps_spectra.plotters.standard_plotters as dPlotObjs

def getTotalContribsPlotFromSpectraOutput( spectraOutput ):
	""" Description of function
	
	Args:
		spectraOutput: (GenSpectraOutput object) This contains all information for a generated spectrum
			 
	Returns
		 outPlot: (pyplot figure handle) Plot of the data
 
	"""
	dPlotter = dPlotObjs.DataPlotterXPS_Standard()
	data = spectraOutput.totalSpectralContributions
	outPlot = dPlotter.createPlot( [data] )

	return outPlot


def getAllContribsPlotFromSpectraOutput( spectraOutput ):
	dataLabels = ["Total"] + ["{}-{}-{}".format(x.fragKey, x.eleKey, x.aoKey) for x in spectraOutput.label]
	dataLabels = [x.replace("-None","") for x in dataLabels]
	dPlotter = dPlotObjs.DataPlotterXPS_Standard()
	data = [spectraOutput.totalSpectralContributions] + spectraOutput.spectralContributions
	outPlot = dPlotter.createPlot( data, legend=True, dataLabels=dataLabels )
	return outPlot

