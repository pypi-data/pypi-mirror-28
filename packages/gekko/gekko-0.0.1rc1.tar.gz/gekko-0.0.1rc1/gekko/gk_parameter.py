import os 
from .gk_operators import GK_Operators
"""
Param_input_options = []
Param_inout_options = ['VALUE']
Param_output_options = []


FV_input_options = Param_input_options+['LB','UB','CRITICAL', 'DMAX', 'DMAXHI', 
                                        'DMAXLO', 'FSTATUS', 'LOWER','MEAS', 
                                        'PSTATUS','STATUS', 'UPPER', 'VDVL', 
                                        'VLACTION', 'VLHI', 'VLLO']
FV_inout_options = Param_inout_options+[]
FV_output_options = Param_output_options+['LSTVAL', 'NEWVAL']

MV_inout_options = FV_inout_options+[]
MV_input_options = FV_input_options + ['COST', 'DCOST', 'MV_STEP_HOR','REQONCTRL', 'TIER']
MV_output_options = FV_output_options + ['AWS', 'DPRED', 'NXTVAL', 'PRED', ]

#gather in dictionary
parameter_options = {'FV':{'inputs':FV_input_options, 'outputs':FV_output_options, 'inout': FV_inout_options}, 
                     'MV':{'inputs':MV_input_options,'outputs':MV_output_options,'inout':MV_inout_options},
                     None:{'inputs':Param_input_options,'outputs':Param_output_options,'inout':Param_inout_options}}

"""
from .properties import parameter_options as options

class GKParameter(GK_Operators):
    """Represents a parameter in a model."""
    counter = 1

    def __init__(self, name='', value=0, integer=False):
        if name == '':
            name = 'p' + GKParameter.counter
            GKParameter.counter += 1
            if integer == True:
                name = 'int_' + name
                
        # prevents the __setattr__ function from sending options to the server
        # until the __init__ function has completed since they should only be
        # sent if changed from their defaults
        self.__dict__['_initialized'] = False
        
        GK_Operators.__init__(self, name, value=value)

        #self.VALUE = value #initialized value SET IN GK_Operators
            
        if not hasattr(self,'type'): #don't overwrite FV and MV
            self.type = None 

        # now allow options to be sent to the server
        self._initialized = True
        
        
    def __repr__(self):
        return str(self.value) #'%s = %f' % (self.name, self.value)

    def __len__(self):
        return len(self.value)
    def __getitem__(self,key):
        return self.value[key]
    def __setitem__(self,key,value):
        self.value[key] = value


    def __setattr__(self, name, value):
        if self._initialized:
            #ignore cases on global options
            name = name.upper()

            #only allow user to set input or input/output options:
            if name in options[self.type]['inputs']+options[self.type]['inout']:
                self.__dict__[name] = value
                #write option to dbs file
                if self.type != None: #only for FV and MV
                    if name != 'VALUE': #don't write values to dbs
                        f = open(os.path.join(self.path,'overrides.dbs'),'a')
                        f.write(self.name+'.'+name+' = '+str(value)+'\n')
                        f.close()
                    
            #don't allow writing to output properties by default
            elif name in options[self.type]['outputs']:
                #define outputs by passing list/tuple with 1st element being True
                #to override the output writing prevention 
                try:
                    if value[0] == True:
                        self.__dict__[name] = value[1]
                    else:
                        raise TypeError
                except TypeError:
                    print(str(name)+" is an output property")
                    raise AttributeError
                    
            #no other properties allowed
            else:
                print(str(name)+" is not a recognized property")
                raise AttributeError
                
        #for initializing model
        else:
            self.__dict__[name] = value
            
            
class GK_FV(GKParameter):
    """Fixed Variable. Inherits GKParameter."""

    def __init__(self, name='', value=0, lb=None, ub=None, gk_model=None, model_path=None, integer=False):

        # prevents the __setattr__ function from sending options to the server
        # until the __init__ function has completed since they should only be
        # sent if changed from their defaults
        self.__dict__['_initialized'] = False

        if not hasattr(self,'type'): #don't overwrite MV
            self.type = 'FV'
        self.model_name = gk_model
        #self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.model_name) OLD from when model file were in the same directory; now using temp files
        self.path = model_path #use the same path as the model 
        
        #Unlike variables, parameters don't need bounds unless they are special (MV,FV)
        self.LB = lb #lower bound
        self.UB = ub #upper bound
        
        # FV options
        self.CRITICAL = 0
        self.DMAX = 1.0e20
        self.DMAXHI = 1.0e20
        self.DMAXLO = -1.0e20
        self.FSTATUS = 1.0
        if lb is not None:
            self.LOWER = lb
        else:
            self.LOWER = -1.0e20
        self.LSTVAL = 1.0
        self.MEAS = None
        self.NEWVAL = 1.0
        self.PSTATUS = 1
        self.STATUS = 1
        if ub is not None:
            self.UPPER = ub
        else:
            self.UPPER = 1.0e20
        self.VDVL = 1.0e20
        self.VLACTION = 0
        self.VLHI = 1.0e20
        self.VLLO = -1.0e20
       
        GKParameter.__init__(self, name=name, value=value, integer=integer)


    def meas(self,measurement):
        self.MEAS = measurement
        #open measurement.dbs file
        f = open(os.path.join(self.path,'measurements.dbs'),'a')
        #write measurement
        f.write(self.name+'.MEAS = '+str(measurement)+', 1, none\n')
        #close file
        f.close()
        
        #write tag file
        f = open(os.path.join(self.path,self.name),'w')
        #write measurement
        f.write(str(measurement))
        #close tag file
        f.close()
        
        
        



class GK_MV(GK_FV):
    """ Manipulated Variable. Inherits GK_FV."""

    def __init__(self, name='', value=0, lb=None, ub=None, gk_model=None, model_path=None, integer=False):
        
        # prevents the __setattr__ function from sending options to the server
        # until the __init__ function has completed since they should only be
        # sent if changed from their defaults
        self.__dict__['_initialized'] = False

        # prevents the __setattr__ function from sending options to the server
        # until the __init__ function has completed since they should only be
        # sent if changed from their defaults
        self.initialized = False

        self.type = 'MV'

        # options for manipulated variables
        self.AWS = 0
        self.COST = 0.0
        self.DCOST = 0.00001
        self.DPRED = 0.0
        self.MV_STEP_HOR = 0
        self.NXTVAL = 1.0
        self.PRED = 1.0
        self.REQONCTRL = 0
        self.TIER = 1

        
        GK_FV.__init__(self, name=name, value=value, lb=lb, ub=ub, gk_model=gk_model, model_path=model_path, integer=integer)

        
    def dt(self):
        return GK_Operators('$' + self.name)
