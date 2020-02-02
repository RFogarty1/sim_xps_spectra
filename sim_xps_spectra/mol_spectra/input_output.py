

""" These input-output functions are specific to this module, though will probably always be whats wanted """


def getTotalContribStrFromSpectraOutput( spectraOutput, energyFmt=None, intensityFmt=None ):
	""" Gets a string used to write total spectrum output to a file
	
	Args:
		spectraOutput: (GenSpectraOutput object) This contains all information for a generated spectrum
		energyFmt: (Str, optional) The format string for the energies. Default = "{:.9f}"
		intensityFmt: (Str, optional) The format string for the intensities. Default = "{:.9f}"
			 
	Returns
		 outStr: (Str) String containing data on the total generated spectrum
 
	Raises:
		 Errors
	"""

	energyFmt = "{:.9f}" if energyFmt is None else energyFmt
	intensityFmt = "{:.9f}" if intensityFmt is None else intensityFmt
	formStr = "{}, {}".format( energyFmt, intensityFmt )

	outData = spectraOutput.totalSpectralContributions
	outStrList = ["#Energy, Intensities"]
	for line in outData:
		outStrList.append( formStr.format(line[0],line[1]) )


	return "\n".join(outStrList)


def getAllContribsOutputStrFromSpectraOutput( spectraOutput, energyFmt=None, intensityFmt=None ):
	""" Gets a str to write all contributions to spectraOutput (e.g. fragA-S-3p contribution)
	
	Args:
		spectraOutput: (GenSpectraOutput object) This contains all information for a generated spectrum
		energyFmt: (Str, optional) The format string for the energies. Default = "{:.9f}"
		intensityFmt: (Str, optional) The format string for the intensities. Default = "{:.9f}"
			 
	Returns
		 outStr: (Str) String containing data on the contributions to the spectrum
 
	"""
	energyFmt = "{:.9f}" if energyFmt is None else energyFmt
	intensityFmt = "{:.9f}" if intensityFmt is None else intensityFmt

	labelList = spectraOutput.label
	dataList = spectraOutput.spectralContributions

	#Get the labels
	labelStrs = ", ".join( ["{}-{}-{}".format(x.fragKey, x.eleKey, x.aoKey) for x in labelList] )
	labelStrs = "#labels = " + labelStrs

	outStrList = [labelStrs]
	outStrList.append( "#Energy, Intensities" )
	dataStrFmt = energyFmt + ", " + ", ".join( [intensityFmt for x in range(len(dataList))] )

	for idx,x in enumerate(dataList[0]):
		energy = x[0]
		currData = [ a[idx][1] for a in dataList ]
		outStrList.append( dataStrFmt.format( energy, *currData) )

	return "\n".join(outStrList)
