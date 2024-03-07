####################
# IMPORT LIBRARIES #
####################

import logging
import os
import pandas as pd
from aa01_Utility import Utility


#####################
# Set Log Messenger #
#####################

logmessenger = logging.getLogger(__name__)
logmessenger.setLevel(logging.INFO)

parameters = Utility().read_parameters()
logs_folder = parameters['folder_names']['logs_main_folder']
logs_file_name = parameters['file_names']['logs_file_name']

#Reset log file
if os.path.exists(os.path.join(logs_folder, logs_file_name)):
    os.remove(os.path.join(logs_folder, logs_file_name))


Utility().create_folder(logs_folder)

file_handler = logging.FileHandler(os.path.join(logs_folder, logs_file_name))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(filename)s : %(message)s')

file_handler.setFormatter(formatter)
logmessenger.addHandler(file_handler)

logmessenger.info('Dataset module initialized')


##################
# Define Methods #
##################

class CreateDataset:

    def __init__(self) -> None:
        pass

    def load_and_save_dataset(self, final_url, filename):
        try:
            base_url = parameters['urls']['base_url']
            final_url = base_url + final_url.split('/')[-2]

            data = pd.read_csv(final_url)

            main_data_folder = parameters['folder_names']['data_main_folder']
            raw_data_folder = parameters['folder_names']['raw_data_folder']

            Utility().create_folder(main_data_folder)
            Utility().create_folder(os.path.join(main_data_folder, raw_data_folder))

            data.to_csv(os.path.join(main_data_folder, raw_data_folder, str(
                filename)), index=False, sep=',')

        except Exception as e:
            logmessenger.error(e)
            raise e


if __name__ == "__main__":

    data_url = parameters['urls']['data_url']

    md = CreateDataset()
    logmessenger.info('Data loading process started.')

    raw_data_filename = parameters['file_names']['raw_data_file_name']
    md.load_and_save_dataset(data_url, raw_data_filename)
    
    logmessenger.info('Data loading completed and saved to the directory Data/raw')
