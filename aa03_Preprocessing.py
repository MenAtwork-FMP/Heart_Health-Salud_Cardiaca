####################
# IMPORT LIBRARIES #
####################

from aa01_Utility import Utility
import pandas as pd
import numpy as np
import logging
import os
import dill
import shutil

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


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

class Preprocessing:

    def __init__(self) -> None:
        pass

    def remove_columns(self):

        try:
            main_data_foldername = parameters['folder_names']['data_main_folder']
            raw_data_foldername = parameters['folder_names']['raw_data_folder']
            temp_data_foldername = parameters['folder_names']['temp_data_folder']
            
            temp_data_filename = parameters['file_names']['temp_data_file_name']
            raw_data_filename = parameters['file_names']['raw_data_file_name']
            

            # Reading the raw data
            df = pd.read_csv(os.path.join(main_data_foldername,raw_data_foldername, raw_data_filename))

            # Removing the unnecessary features
            df.drop(['ID', 'Patient'], axis=1, inplace=True)

            # Creating a Data folder to save the processed data
            Utility().create_folder(main_data_foldername)
            Utility().create_folder(os.path.join(main_data_foldername, temp_data_foldername))

            # Saving the data to new folder
            df.to_csv(os.path.join(main_data_foldername, temp_data_foldername,temp_data_filename), index=False, sep=',')

            logmessenger.info('Removed unnecessary columns from the data.')

        except Exception as e:
            logmessenger.error(e)
            raise e

    def adjust_blood_pressure_column(self):

        try:
            main_data_foldername = parameters['folder_names']['data_main_folder']
            temp_data_foldername = parameters['folder_names']['temp_data_folder']
            
            temp_data_filename = parameters['file_names']['temp_data_file_name']

            # Reading the temp data
            df = pd.read_csv(os.path.join(main_data_foldername,temp_data_foldername, temp_data_filename))

            # Adjusting values of blood presssure column.
            df[['systolic_pressure', 'diastolic_pressure']] = df['Blood Pressure(mmHg)'].str.split('/', expand=True)
            df['systolic_pressure'] = df['systolic_pressure'].astype(int)
            df['diastolic_pressure'] = df['diastolic_pressure'].astype(int)
            df.drop(columns=['Blood Pressure(mmHg)'], inplace=True)

            # Creating a Data folder to save the processed data
            Utility().create_folder(main_data_foldername)
            Utility().create_folder(os.path.join(main_data_foldername, temp_data_foldername))

            # Saving the processed data
            df.to_csv(os.path.join(main_data_foldername,temp_data_foldername,temp_data_filename),index=False, sep=',')

            logmessenger.info('Blood pressure data adjusted.')

        except Exception as e:
            logmessenger.error(e)
            raise e

    def adding_bmi(self):

        try:
            main_data_foldername = parameters['folder_names']['data_main_folder']
            temp_data_foldername = parameters['folder_names']['temp_data_folder']
            
            temp_data_filename = parameters['file_names']['temp_data_file_name']

            # Reading the temp data
            df = pd.read_csv(os.path.join(main_data_foldername,temp_data_foldername, temp_data_filename))

            # Adding a column with the BMI calculation
            df['BMI'] = df['Weight(kg)'] / ((df['Height(cm)']/100 )** 2)

            # Creating a Data folder to save the processed data
            Utility().create_folder(main_data_foldername)
            Utility().create_folder(os.path.join(main_data_foldername, temp_data_foldername))

            # Saving the processed data
            df.to_csv(os.path.join(main_data_foldername,temp_data_foldername,temp_data_filename),index=False, sep=',')

            logmessenger.info('BMI calculation added.')

        except Exception as e:
            logmessenger.error(e)
            raise e

    def endcoding(self):
     
        try:
            main_data_foldername = parameters['folder_names']['data_main_folder']
            temp_data_foldername = parameters['folder_names']['temp_data_folder']
            
            temp_data_filename = parameters['file_names']['temp_data_file_name']

            # Reading the temp data
            df = pd.read_csv(os.path.join(main_data_foldername,temp_data_foldername, temp_data_filename))


            # Splitting the data into independent and dependent features
            Xfeatures = df.drop(columns=['Heart Attack'],axis=1)
            ylabel = df['Heart Attack']
            logmessenger.info('Splitted the data into independent and dependent features.')


            # label encoding the target column
            label_transformer = LabelEncoder()
            ylabel = label_transformer.fit_transform(ylabel)


            # Saving the label encoder transformer to pickle file
            pipeline_foldername = parameters['folder_names']['pipeline_foldername']
            label_transformer_filename = parameters['file_names']['label_transformer_file_name']


            # Creating a Data folder to save the pipeline
            Utility().create_folder(pipeline_foldername)


            # Saving the label encoder fitting earlier
            with open(os.path.join(pipeline_foldername, label_transformer_filename), 'wb') as f:
                dill.dump(label_transformer, f)
            logmessenger.info('Label encoded.')


            # Reading model parameters
            random_state = parameters['model_parameters']['random_state']
            n_estimators = parameters['model_parameters']['n_estimators']
            criterion = parameters['model_parameters']['criterion']
            max_depth = parameters['model_parameters']['max_depth']
            min_samples_split = parameters['model_parameters']['min_samples_split']
            min_samples_leaf = parameters['model_parameters']['min_samples_leaf']
            test_size = parameters['model_parameters']['test_size']

            
            # Splitting the data into training validation sets
            all_columns = df.columns.values
            all_columns = list(all_columns)
            all_columns.remove("Heart Attack")
            
            X_train, X_val, y_train, y_val = train_test_split(
                Xfeatures, ylabel, random_state=random_state, test_size=test_size)
            
            X_train = pd.DataFrame(X_train, columns=all_columns)
            X_val = pd.DataFrame(X_val, columns=all_columns)

            logmessenger.info('Splitted the data into the data for training and the data for validation.')

            
            # finding the names of numerical and categorical columns
            cat_cols = [feature for feature in X_train.columns if X_train[feature].dtypes == 'O']
            num_cols = [feature for feature in X_train.columns if feature not in cat_cols]


            # creating a pipeline to process categorical columns
            cat_pipe = Pipeline([
                ('cat_encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan)),
            ])
            logmessenger.info('Created a pipeline to preprocess the categorical features in the data.')


            # Creating numerical pipeline
            num_pipe = Pipeline([
                ('scaler', MinMaxScaler())
            ])
            logmessenger.info('Created a pipeline to preprocess the numerical features in the data.')


            # Creating a combined preprocess pipeline, training it and then saving it.
            preprocess_pipe = ColumnTransformer([
                ('num_pipeline', num_pipe, num_cols),
                ('cat_pipeline', cat_pipe, cat_cols)
            ], remainder='passthrough')
            logmessenger.info('Combined the preprocess pipelines created for categorical and numerical data preprocessing.')


            # Transforming the train and validation data using preprocess pipeline
            X_train = preprocess_pipe.fit_transform(X_train)
            logmessenger.info('Proccesed train data with complete pipeline.')
            X_val = preprocess_pipe.transform(X_val)
            logmessenger.info('Proccesed validation data with complete pipeline.')

            # Saving the fitted preprocess pipeline
            preprocess_pipe_filename = parameters['file_names']['preprocess_pipeline_filename']
            preprocess_pipe_path = os.path.join(pipeline_foldername, preprocess_pipe_filename)

            with open(preprocess_pipe_path, 'wb') as pickle_file:
                dill.dump(preprocess_pipe, pickle_file)
            logmessenger.info('Saved the fitted preprocess pipeline as a python pickle file.')

    
            # Saving X_train, X_val, y_train, y_val

            processed_data_folder = parameters['folder_names']['processed_data_folder']
            Utility().create_folder(main_data_foldername)
            Utility().create_folder(os.path.join(main_data_foldername, processed_data_folder))

            processed_X_train = parameters['file_names']['processed_X_train']
            X_train = pd.DataFrame(X_train)
            X_train.columns = all_columns
            X_train.to_csv(os.path.join(main_data_foldername, processed_data_folder, processed_X_train), index=False, sep=',')
            logmessenger.info('Preprocess X_train saved.')

            processed_X_val = parameters['file_names']['processed_X_val']
            X_val = pd.DataFrame(X_val)
            X_val.columns = all_columns
            X_val.to_csv(os.path.join(main_data_foldername, processed_data_folder, processed_X_val), index=False, sep=',')
            logmessenger.info('Preprocessed X_val saved')

            processed_y_train = parameters['file_names']['processed_y_train']
            y_train = pd.DataFrame(y_train)
            y_train.columns = ['target']
            y_train.to_csv(os.path.join(main_data_foldername, processed_data_folder, processed_y_train), index=False, sep=',')
            logmessenger.info('Preprocessed y_train saved')

            processed_y_val = parameters['file_names']['processed_y_val']
            y_val = pd.DataFrame(y_val)
            y_val.columns = ['target']
            y_val.to_csv(os.path.join(main_data_foldername, processed_data_folder, processed_y_val), index=False, sep=',')
            logmessenger.info('Preprocessed y_val saved')

            # Removing the interm data directories since they are of no use now
            temp_data_foldername = parameters['folder_names']['temp_data_folder']

            shutil.rmtree(os.path.join(main_data_foldername, temp_data_foldername))
            logmessenger.info('Temp data directories removed.')

        except Exception as e:
            logmessenger.error(e)
            raise e       


if __name__ == '__main__':

    preprocessdata = Preprocessing()
    logmessenger.info('Preprocessing module initialized')
    preprocessdata.remove_columns()
    preprocessdata.adjust_blood_pressure_column()
    preprocessdata.adding_bmi()
    preprocessdata.endcoding()