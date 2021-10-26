import typing
import numpy as np

def performGillespie(propensities=lambda time, state: 'Computed Propensities',
        initial=np.ndarray, tSpan=['tStart','tEnd']):
    'yields states'

class Parameters():
    def __init__(numCompartments, parameterNames=list):
        'Setup Parameters'
    
    def configureParams(parameters=np.ndarray):
        'Store parameters'
    
    def __getitem__():
        'Retrieve parameters'


class DataCollector():
    def begin(*args, **kwargs): # Configuration
        pass

    def report(state):
        pass

    def getResult():
        'Return collected data (+ some processing)'


class Model(pints.ForwardModel):
    def __init__(numcompartments):
        'Configure Parameters class and Data Collector'
        pass

    def n_parameters():
        pass

    def n_outputs():
        pass

    def simulate(paramsAndIntials=np.ndarray, times=list):
        'Returns np.ndarray'
        'Exact output format etc is specified by datacollector'
        #Initialize Parameters
        #Initialize DataCollector
        #Perform simulation and Report to DataCollector
        #Retrieve and return output from datacollector
        pass


