####################
# IMPORT LIBRARIES #
####################

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, balanced_accuracy_score, precision_score, recall_score, f1_score, classification_report
import json
import os
import joblib
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from aa01_Utility import Utility
import mlflow
import mlflow.sklearn


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


##################
# Define Methods #
##################

class ModelTraining:

    def __init__(self) -> None:
        pass

    def model_training(self):

        try:
            main_data_foldername = parameters['folder_names']['data_main_folder']
            processed_data_foldername = parameters['folder_names']['processed_data_folder']
            
            pr_X_train_filename = parameters['file_names']['processed_X_train']
            pr_X_val_filename = parameters['file_names']['processed_X_val']
            pr_y_train_filename = parameters['file_names']['processed_y_train']
            pr_y_val_filename = parameters['file_names']['processed_y_val']

            X_train = pd.read_csv(os.path.join(main_data_foldername, processed_data_foldername, pr_X_train_filename)).values
            X_val = pd.read_csv(os.path.join(main_data_foldername, processed_data_foldername, pr_X_val_filename)).values
            y_train = pd.read_csv(os.path.join(main_data_foldername, processed_data_foldername, pr_y_train_filename)).values.flatten()
            y_val = pd.read_csv(os.path.join(main_data_foldername, processed_data_foldername, pr_y_val_filename)).values.flatten()

            # Initializing a machine learning model

            with mlflow.start_run():

                # read parameters from yaml file                    
                random_state = parameters['model_parameters']['random_state']
                n_estimators = parameters['model_parameters']['n_estimators']
                criterion = parameters['model_parameters']['criterion']
                max_depth = parameters['model_parameters']['max_depth']
                min_samples_split= parameters['model_parameters']['min_samples_split']
                min_samples_leaf= parameters['model_parameters']['min_samples_leaf']
                test_size= parameters['model_parameters']['test_size']
               
               # define log parameters
                mlflow.log_param('n_estimators', n_estimators)
                mlflow.log_param('max_depth', max_depth)
                mlflow.log_param('min_sample_split', min_samples_split)
                mlflow.log_param('min_sample_leaf', min_samples_leaf)

                # create random forest ML pipeline
                randforest_pipe = RandomForestClassifier(
                    random_state=random_state,
                    n_estimators=n_estimators,
                    criterion=criterion,
                    min_samples_split=min_samples_split,
                    min_samples_leaf=min_samples_leaf
                )
                logmessenger.info('Random Forest Model initialized')


                # Fitting the model on train data
                randforestmodel = randforest_pipe.fit(X_train, y_train)
                logmessenger.info('Model trained on the train data.')

                # Predicting metrics using the trained model and the test data
                y_pred = randforestmodel.predict(X_val)

                balanced_accuracy_scr = balanced_accuracy_score(y_val, y_pred)
                precision_scr = precision_score(y_val, y_pred, average='weighted')
                recall_scr = recall_score(y_val, y_pred, average='weighted')
                f1_scr = f1_score(y_val, y_pred, average='weighted')
                clf_report = classification_report(y_val, y_pred, output_dict=True)
                clf_report = pd.DataFrame(clf_report).transpose()

                mlflow.log_metric('balanced_accuracy_score',balanced_accuracy_scr)
                mlflow.log_metric('precision_score', precision_scr)
                mlflow.log_metric('recall_score', recall_scr)
                mlflow.log_metric('f1_score', f1_scr)

                logmessenger.info('Trained model evaluation done using validation data.')

            # Saving the calculated metrics into a json file in the Metrics folder
            metrics_folder = parameters['folder_names']['metrics_folder']
            metrics_filename = parameters['file_names']['metrics_file_name']

            Utility().create_folder(metrics_folder)

            with open(os.path.join(metrics_folder, metrics_filename), 'w') as json_file:
                metrics = dict()
                metrics['balanced_accuracy_score'] = balanced_accuracy_scr
                metrics['precision_score'] = precision_scr
                metrics['recall_score'] = recall_scr
                metrics['f1_score'] = f1_scr

                json.dump(metrics, json_file, indent=4)

            report_file_name = parameters['file_names']['report_filename']

            clf_report.to_csv(os.path.join(metrics_folder, report_file_name))

            logmessenger.info('Saved evaluations in files.')

            # Saving the trained machine learing model in the models folder
            model_foldername = parameters['folder_names']['model_folder']
            model_name = parameters['file_names']['model_file_name']

            Utility().create_folder(model_foldername)
            model_dir = os.path.join(model_foldername, model_name)

            joblib.dump(randforestmodel, model_dir)

            logmessenger.info('Trained model saved as a joblib file.')

        except Exception as e:
            logmessenger.error(e)
            raise e


if __name__ == "__main__":

    mt = ModelTraining()
    mt.model_training()
