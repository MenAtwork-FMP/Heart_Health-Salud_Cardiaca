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
                page_icon=":heart",
                layout="wide",
                initial_sidebar_state="expanded",
            )

            # Adding the title to the page
            st.title('Heart Attack Risk Assessment')

            # Adding a author name to the project
            st.caption('A project by MenAtWork repo ')

            # Making Predictions
            st.header('Input data to assess heart attack risk')
            st.markdown("Minimum and Maximum input values bound to the actual data of a reduced sample of the subjects studied")
            st.markdown("The intent is to provide the concept of what can be further developed for specific use cases.")

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

            predict = st.button('Run Assessment')

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
                    prediction_prob = model.predict_proba(transformed_input)

                    # Showing the prediction made to the user
                    

                    if prediction == 0:
                        if prediction_prob[0,0] >= 0.8:
                            answer = "VERY LOW RISK"
                        elif prediction_prob[0,0] >= 0.6:
                            answer = "LOW RISK"
                        else:
                            answer = "LOW RISK"
                    else:
                        if prediction_prob[0,1] >= 0.9:
                            answer = "VERY HIGH RISK"
                        elif prediction_prob[0,1] >= 0.6:
                            answer = "HIGH RISK"
                        else:
                            answer = "MODERATE RISK"
                    
                    st.subheader(
                        f"Assessment scale:\n"
                        f"VERY LOW >> LOW >> MODERATE >> HIGH >> VERY HIGH\n\n"
                        f"Analyzing the given data there is a  {answer} of heart attack"
                    )
                    

        except Exception as e:
            raise e


if __name__ == "__main__":
    wa = WebApp()
    wa.webapp()