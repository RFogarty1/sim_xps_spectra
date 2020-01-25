

import gen_basis_helpers.shared.data_plot_base as dPlotters


class DataPlotterStandard(dPlotters.DataPlotterStandard):
	pass


class DataPlotterXPS_Standard(dPlotters.DataPlotterStandard):

	def __init__(self, **kwargs):
		self.registeredKwargs.add("reversedXAxis")
		kwargsDict = self._getDefaultKwargsDict()
		kwargsDict.update(kwargs)
		super().__init__(**kwargsDict)

	def _getDefaultKwargsDict(self):
		defaultKwargs = dict()
		defaultKwargs["xlabel"] = "Binding Energy / eV"
		defaultKwargs["ylabel"] = "Intensity / arb. units"
		defaultKwargs["reversedXAxis"] = True
		return defaultKwargs

	def createPlot(self, data, **kwargs):
		with dPlotters.temporarilySetDataPlotterRegisteredAttrs(self,kwargs):
			outFig = super().createPlot(data, **kwargs)
			outAxis = outFig.get_axes()[0]
			if self.reversedXAxis:
				currXLim = outAxis.get_xlim()
				if currXLim[0] < currXLim[1]:
					outAxis.set_xlim( [currXLim[1], currXLim[0]] )

		return outFig

