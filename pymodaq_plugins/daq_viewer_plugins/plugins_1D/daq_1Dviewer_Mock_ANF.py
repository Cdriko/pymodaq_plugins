from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets
from pymodaq.daq_viewer.utility_classes import DAQ_Viewer_base
import numpy as np
from easydict import EasyDict as edict
from collections import OrderedDict
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo, gauss1D, linspace_step, DataFromPlugins, Axis
from pymodaq.daq_viewer.utility_classes import comon_parameters
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.parametertree.parameterTypes as pTypes
import pymodaq.daq_utils.custom_parameter_tree as custom_tree

import numpy


class DAQ_1DViewer_Mock_ANF(DAQ_Viewer_base):

    params = comon_parameters + [
        {'title': 'Speed', 'name': 'speed', 'type': 'slide', 'value': 0.001, 'min': 0,'max':6.28},
        {'title': 'Amp', 'name': 'amp', 'type': 'float', 'value': 10, 'min': 0},
        {'title': 'Noise', 'name': 'noise', 'type': 'slide', 'value': 0.2, 'min': 0,'max':10}

    ]
    hardware_averaging = False

    def __init__(self, parent=None, params_state=None): #init_params is a list of tuple where each tuple contains info on a 1D channel (Ntps,amplitude, width, position and noise)
        super(DAQ_1DViewer_Mock_ANF,self).__init__(parent, params_state)
        self.ind_data = 0
        self.time_x=0



    def commit_settings(self,param):

        pass

    def ini_detector(self, controller=None):
        """
            Initialisation procedure of the detector updating the status dictionnary.

            See Also
            --------
            set_Mock_data, daq_utils.ThreadCommand
        """
        self.status.update(edict(initialized=False,info="",x_axis=None,y_axis=None,controller=None))
        try:

            if self.settings.child(('controller_status')).value()=="Slave":
                if controller is None: 
                    raise Exception('no controller has been defined externally while this detector is a slave one')
                else:
                    self.controller=controller
            else:
                self.controller="Mock controller"

            self.status.initialized=True
            self.status.controller=self.controller
            #self.status.x_axis = self.x_axis
            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status',[getLineInfo()+ str(e),'log']))
            self.status.info=getLineInfo()+ str(e)
            self.status.initialized=False
            return self.status

    def close(self):
        """
            Not implemented.
        """
        pass




    def grab_data(self, Naverage=1, **kwargs):
        self.time_x+=self.settings.child('speed').value()
        x=numpy.linspace(self.time_x,self.time_x+10,100)

        data=(self.settings.child('amp').value()*numpy.sin(x))+self.settings.child('noise').value()*numpy.random.random_sample(100)

        self.data_grabed_signal.emit([DataFromPlugins(name='Mock1', data=[data], dim='Data1D')])

    def stop(self):
        """
            not implemented.
        """
        
        return ""
