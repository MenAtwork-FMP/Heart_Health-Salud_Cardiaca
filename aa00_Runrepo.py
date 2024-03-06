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


subprocess.run(["python", utility_file_path])
subprocess.run(["python", dataset_file_path])

