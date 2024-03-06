####################
# IMPORT LIBRARIES #
####################

import yaml
import os


###################
# DEFINE METHODS #
###################

class Utility:

###Create INIT file for parameters.yaml
    def __init__(self, parameters_path='parameters.yaml') -> None:
        self.parameters_path = parameters_path

####Create method to create folders if they do not exist.
    def create_folder(self, folder_name):
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

        except Exception as e:
            raise e    

###Create method to read parameters
    def read_parameters(self):
        try:
            with open(self.parameters_path, 'r') as parameters_file:
                parameters = yaml.safe_load(parameters_file)

        except Exception as e:
            raise e

        else:
            return parameters        
