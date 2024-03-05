####################
# IMPORT LIBRARIES #
####################

import yaml
import os
import logging


#####################
# Set Log Messenger #
#####################

logmessenger = logging.getLogger(__name__)
logmessenger.setLevel(logging.INFO)

logfolder = 'Logs'
logfilename = 'Logs.log'
logfilenamepath = os.path.join(logfolder,logfilename)

if not os.path.exists(logfolder):
        os.makedirs(logfolder)
else:
    if os.path.exists(logfilenamepath):
        with open(logfilenamepath, "w") as file:
            pass
    else:
        open(logfilenamepath, "w").close()

file_handler = logging.FileHandler(logfilenamepath)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s : %(message)s')
file_handler.setFormatter(formatter)
logmessenger.addHandler(file_handler)

logmessenger.info('Log Messenger set up finalized')


###################
# DEFINE METHODS #
###################

class Utility:

###Create INIT file for parameters.yaml
    def __init__(self, parameters_path='parameters.yaml') -> None:
        self.parameters_path = parameters_path
    logmessenger.info('Yaml INIT method created')

####Create method to create folders if they do not exist.
    def create_folder(self, folder_name):
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

        except Exception as e:
            raise e
    logmessenger.info('Create Folder method defined')        

###Create method to read parameters
    def read_parameters(self):
        try:
            with open(self.params_path, 'r') as params_file:
                params = yaml.safe_load(params_file)

        except Exception as e:
            raise e

        else:
            return params
    logmessenger.info('Read parameters method defined')        