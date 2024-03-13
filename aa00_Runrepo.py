############################################
# Main Code File to run other subprocesess #
############################################

#import libraries
import subprocess


##########################
# Subprocesses execution #
##########################

utility_file_path = "./aa01_Utility.py"
dataset_file_path = "./aa02_Dataset.py"
preprocessing_file_path = "./aa03_preprocessing.py"


subprocess.run(["python", utility_file_path])
subprocess.run(["python", dataset_file_path])
subprocess.run(["python", preprocessing_file_path])

