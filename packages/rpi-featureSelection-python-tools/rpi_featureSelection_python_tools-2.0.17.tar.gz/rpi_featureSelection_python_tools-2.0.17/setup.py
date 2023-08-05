from setuptools import setup

setup(
	name='rpi_featureSelection_python_tools',  # This is the name of your PyPI-package. 
	version= '2.0.17',  # Update the version number for new releases
	author= 'Keyi Liu',
	entry_points = {
		'd3m.primitives': [
			'rpi_featureSelection_python_tools.IPCMBplus_Selector = rpi_featureSelection_python_tools.feature_selector:IPCMBplus_Selector'
		],
	},
	packages=['rpi_featureSelection_python_tools']
)
