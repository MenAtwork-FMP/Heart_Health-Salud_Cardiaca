####################
# IMPORT LIBRARIES #
####################

import streamlit as st
import numpy as np
from aa01_Utility import Utility
import os
import dill
import joblib
import pandas as pd


##################
# Define Methods #
##################

parameters = Utility().read_parameters()

class WebApp:

    def __init__(self) -> None:
        pass

    def webapp(self):

        try:
            st.set_page_config(
                page_title="Heart Attack Risk Assessment",
                page_icon=":butterfly",
                layout="wide",
                initial_sidebar_state="expanded",
            )

            # Adding the title to the page
            st.title('Heart Attack Risk Assessment')

            # Adding a author name to the project
            st.caption('A project by Analytics ')

            # Making Predictions
            st.header('Input your data to make a prediction')

            # Creating an interfact to get inputs from the user
            col1, col2, col3 = st.columns(3, gap='large')

            age = col1.slider('Age', min_value=30,max_value=60, step=1, value=35)
            height = col1.slider('Height(cm)', min_value=155,max_value=183, step=1, value=160)
            weight = col1.slider('Weight (Kg)', min_value=60,max_value=89, step=1, value=65)
            cholesterol = col1.slider('Cholesterol(mg/dL)', min_value=50,max_value=300, step=1, value=180)
            glucose = col1.slider('Glucose(mg/dL)', min_value=75,max_value=100, step=1, value=80)
            exercise = col2.slider('Exercise(hours/week)', min_value=1,max_value=4, step=1, value=2)
            systolic = col2.slider('Systolic blood presssure', min_value=105,max_value=135, step=1, value=110)
            diastolic = col2.slider('Diastolic blood pressure', min_value=65,max_value=85, step=1, value=80)
            BMI = col2.slider('Body mass Index', min_value=24,max_value=27, step=1, value=25)

            gender = col3.selectbox('Gender', ['Male', 'Female'])
            smoker = col3.selectbox('Smoker', ['Yes', 'No'])

            input = np.array([[age,gender,height,weight,cholesterol,glucose,smoker,exercise,systolic,diastolic,BMI]])

            input = pd.DataFrame(input, columns=['Age','Gender','Height(cm)','Weight(kg)',
                                                 'Cholesterol(mg/dL)','Glucose(mg/dL)','Smoker',
                                                 'Exercise(hours/week)','systolic_pressure',
                                                 'diastolic_pressure','BMI'])

            predict = st.button('Make a Prediction')

            # Actions after user clicks on 'Make a Prediction' button
            if predict:
                with st.spinner('Please wait'):
                    pipeline_foldername = parameters['folder_names']['pipeline_foldername']
                    pipeline_filename = parameters['file_names']['preprocess_pipeline_filename']
                    le_transformer_filename = parameters['file_names']['label_transformer_file_name']
                    model_foldername = parameters['folder_names']['model_folder']
                    model_name = parameters['file_names']['model_file_name']

                    # Loading saved preprocess pipeline
                    @st.cache_data
                    def load_preprocess(pipeline_foldername, pipeline_filename, le_transformer_filename):
                        with open(os.path.join(pipeline_foldername, pipeline_filename), 'rb') as f:preprocess_pipeline = dill.load(f)
                        with open(os.path.join(pipeline_foldername, le_transformer_filename), 'rb') as f:le_transformer = dill.load(f)
                        return preprocess_pipeline, le_transformer

                    preprocess_pipeline, le_transformer = load_preprocess(
                        pipeline_foldername, pipeline_filename, le_transformer_filename)

                    # Loading the saved machine learning model
                    @st.cache_data
                    def load_model(model_foldername, model_name):
                        model = joblib.load(os.path.join(
                            model_foldername, model_name))
                        return model

                    model = load_model(model_foldername, model_name)

                    # Preprocessing the input provided by the user
                    transformed_input = preprocess_pipeline.transform(input)
                    

                    # Making predictions using the saved model and the preprocessed data
                    prediction = model.predict(transformed_input)
                    prediction = le_transformer.inverse_transform(prediction)


                    # Showing the prediction made to the user
                    st.subheader(
                        f"Patient's predicted condition:   {prediction}")

        except Exception as e:
            raise e


if __name__ == "__main__":
    wa = WebApp()
    wa.webapp()