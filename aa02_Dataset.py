####################
# IMPORT LIBRARIES #
####################

import logging
import os
from aa01_Utility import Utility


#####################
# Set Log Messenger #
#####################

logmessenger = logging.getLogger(__name__)
logmessenger.setLevel(logging.INFO)

parameters = Utility().read_parameters()
logs_folder = parameters['folder_names']['logs_main_folder']
logs_file_name = parameters['file_names']['logs_file_name']

Utility().create_folder(logs_folder)

file_handler = logging.FileHandler(os.path.join(logs_folder, logs_file_name))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s : %(message)s')

file_handler.setFormatter(formatter)
logmessenger.addHandler(file_handler)

logmessenger.info('Dataset module initialized')


