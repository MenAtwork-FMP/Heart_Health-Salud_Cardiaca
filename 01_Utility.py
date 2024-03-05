####################
# IMPORT LIBRARIES #
####################

import yaml
import os


###################
# DEFINE METHODS #
###################

class Utility:

###Create INIT file
    def __init__(self, params_path='params.yaml') -> None:
        self.params_path = params_path

####Create method to create folders if they do not exist.
    def create_folder(self, folder_name):
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

        except Exception as e:
            raise e

###Creat method to read parameters
    def read_parameters(self):
        try:
            with open(self.params_path, 'r') as params_file:
                params = yaml.safe_load(params_file)

        except Exception as e:
            raise e

        else:
            return params
