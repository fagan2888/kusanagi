import os,sys,utils
from theano.misc.pkl_utils import dump as t_dump, load as t_load

class Loadable(object):
    def __init__(self,name,filename,*args,**kwargs):
        # here we will store the registered
        self.registered_keys = set()
        self.registered_types = set()
        self.filename = filename
        self.name = name
        self.state_changed = True

    def set_state(self,state):
        ''' sets the class state from the input dictionary.'''
        assert isinstance(state,dict), "The state must be a dictionary (Files that saved a lit of variables will need to be converted)"
        for key in state.keys():
            self.__dict__[key] = state[key]

    def get_state(self):
        ''' gets the class state for the variable names in self.registered_keys'''
        state= {}
        for key in self.registered_keys:
            state[key] = self.__dict__[key]

        for attr_name in self.__dict__.keys():
            value = self.__dict__[attr_name]
            if any([isinstance(value,type_) for type_ in self.registered_types]):
                state[attr_name] = value
        return state

    def register(self,variable_names):
        ''' registers a variable name ( or each variable name in a list ) as a state variable'''
        if not type(variable_names) is list:
            variable_names = [variable_names]

        for varname in variable_names:
            assert varname in self.__dict__, 'Tried to register a non-existent attribute'
            self.registered_keys.add(varname)

    def unregister(self,variable_names):
        ''' unregisters a variable name ( or each variable name in a list ) as a state variable'''
        if not type(variable_names) is list:
            variable_names = [variable_names]

        for varname in variable_names:
            if variable_name in registered_keys:
                self.registered_keys.remove(variable_name)
    
    def register_types(self,types_):
        ''' registers every variables of the given type ( or of every given type in types_) as state variables'''
        # TODO we are trusting the user on this
        if not type(types_) is list:
            types_ = [types_]

        for type_ in types_:
            self.registered_types.add(type_)

    def unregister_types(self,types_):
        ''' unregisters every variables of the given type ( or of every given type in types_) as state variables'''
        # TODO we are trusting the user on this
        if not type(types_) is list:
            types_ = [types_]

        for type_ in types_:
            self.registered_types.remove(type_)
        
    def load(self, output_folder=None,output_filename=None):
        output_folder = utils.get_output_dir() if output_folder is None else output_folder
        [output_filename, self.filename] = utils.sync_output_filename(output_filename, self.filename, '.zip')
        path = os.path.join(output_folder,output_filename)
        try:
            with open(path,'rb') as f:
                utils.print_with_stamp('Loading state from %s'%(path),self.name)
                state = t_load(f)
                self.set_state(state)
            self.state_changed = False
        except IOError:
            utils.print_with_stamp('Unable to load state from %s'%(path),self.name)

    
    def save(self, output_folder=None,output_filename=None):
        sys.setrecursionlimit(100000)
        output_folder = utils.get_output_dir() if output_folder is None else output_folder
        [output_filename, self.filename] = utils.sync_output_filename(output_filename, self.filename, '.zip')

        if self.state_changed or output_folder is not None or output_filename is not None:
            # check if output_folder exists, create it if necessary.
            if not os.path.exists(output_folder):
                try:
                    os.makedirs(output_folder)
                except OSError:
                    utils.print_with_stamp( 'Unable to create the directory: %s'%(output_folder), self.name )
                    raise

            # contrusct file path
            path = os.path.join(output_folder,output_filename)
            with open(path,'wb') as f:
                utils.print_with_stamp('Saving state to %s'%(path),self.name)
                t_dump(self.get_state(),f,2)
            self.state_changed = False
