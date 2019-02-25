#This is a Nipype generator. Warning, here be dragons.
#!/usr/bin/env python

import sys
import nipype
import nipype.pipeline as pe

import nipype.interfaces.io as io
import nipype.interfaces.fsl as fsl

#Generic datagrabber module that wraps around glob in an
io_S3DataGrabber = pe.Node(io.S3DataGrabber(outfields=["outfiles"]), name = 'io_S3DataGrabber')
io_S3DataGrabber.inputs.bucket = 'openneuro'
io_S3DataGrabber.inputs.sort_filelist = True
io_S3DataGrabber.inputs.template = 'sub-01/anat/sub-01_T1w.nii.gz'
io_S3DataGrabber.inputs.anon = True
io_S3DataGrabber.inputs.bucket_path = 'ds000101/ds000101_R2.0.0/uncompressed/'
io_S3DataGrabber.inputs.local_directory = '/tmp'

#Wraps command **bet**
fsl_BET = pe.Node(interface = fsl.BET(), name='fsl_BET', iterfield = [''])

#Generic datasink module to store structured outputs
io_DataSink = pe.Node(interface = io.DataSink(), name='io_DataSink', iterfield = [''])
io_DataSink.inputs.base_directory = '/tmp'

#BIDS datagrabber module that wraps around pybids to allow arbitrary
io_BIDSDataGrabber = pe.Node(interface = io.BIDSDataGrabber(), name='io_BIDSDataGrabber', iterfield = [''])

#Create a workflow to connect all those nodes
analysisflow = nipype.Workflow('MyWorkflow')
analysisflow.connect(fsl_BET, "out_file", io_DataSink, "BET_results")
analysisflow.connect(io_BIDSDataGrabber, "T1", fsl_BET, "in_file")

#Run the workflow
plugin = 'MultiProc' #adjust your desired plugin here
plugin_args = {'n_procs': 1} #adjust to your number of cores
analysisflow.write_graph(graph2use='flat', format='png', simple_form=False)
analysisflow.run(plugin=plugin, plugin_args=plugin_args)
