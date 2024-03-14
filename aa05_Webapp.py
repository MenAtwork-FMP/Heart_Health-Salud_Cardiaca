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
                page_icon=":butterfy",
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

            age = col1.slider('Age', min_value=1,max_value=100, step=1, value=23)
            height = col1.slider('Height(cm)', min_value=1,max_value=300, step=1, value=150)
            gender = col2.selectbox('Gender', ['Male', 'Female'])



            TSH = col1.slider('TSH', min_value=0.005,max_value=530.0, step=0.01, value=100.0)
            T3 = col1.slider('T3', min_value=0.05,max_value=18.0, step=0.01, value=12.0)
            TT4 = col1.slider('TT4', min_value=2.0,max_value=60.0, step=0.01, value=30.0)
            T4U = col1.slider('T4U', min_value=0.17,max_value=2.33, step=0.01, value=1.0)
            FTI = col1.slider('FTI', min_value=1.4,max_value=881.0, step=0.01, value=300.0)
            TBG = col1.slider('TBG', min_value=0.1,max_value=200.0, step=0.01, value=100.0)

            I131_treatment = col2.selectbox('I131_treatment', ['True', 'False'])
            query_hypothyroid = col2.selectbox('query_hypothyroid', ['True', 'False'])
            query_hyperthyroid = col2.selectbox('query_hyperthyroid', ['True', 'False'])
            lithium = col2.selectbox('lithium', ['True', 'False'])
            goitre = col2.selectbox('goitre', ['True', 'False'])
            tumor = col2.selectbox('tumor', ['True', 'False'])
            hypopituitary = col2.selectbox('hypopituitary', ['True', 'False'])
            psych = col2.selectbox('psych', ['True', 'False'])

            sex = col3.selectbox('sex', ['Male', 'Female'])
            on_thyroxine = col3.selectbox('on_thyroxine', ['True', 'False'])
            query_on_thyroxine = col3.selectbox('query_on_thyroxine', ['True', 'False'])
            on_antithyroid_meds = col3.selectbox('on_antithyroid_meds', ['True', 'False'])
            sick = col3.selectbox('sick', ['True', 'False'])
            if sex == 'Male':
                pregnant = col3.selectbox('pregnant', ['False'])
            else:
                pregnant = col3.selectbox('pregnant', ['True', 'False'])

            thyroid_surgery = col3.selectbox('thyroid_surgery', ['True', 'False'])
            referral_source = col3.selectbox('referral_source', ['SVI', 'SVHC', 'STMW', 'SVHD', 'WEST', 'other'])

            input = np.array([[age, sex, on_thyroxine, query_on_thyroxine, on_antithyroid_meds, sick,
                                pregnant, thyroid_surgery, I131_treatment, query_hypothyroid, query_hyperthyroid,
                                lithium, goitre, tumor, hypopituitary, psych, TSH, T3, TT4, T4U, FTI,
                                TBG, referral_source]])

            input = pd.DataFrame(input, columns=['age', 'sex', 'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_meds', 'sick',
                                                    'pregnant', 'thyroid_surgery', 'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid',
                                                    'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych', 'TSH', 'T3', 'TT4', 'T4U', 'FTI',
                                                    'TBG', 'referral_source'])

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
                    st.cache_data
                    def load_preprocess(pipeline_foldername, pipeline_filename, le_transformer_filename):
                        with open(os.path.join(pipeline_foldername, pipeline_filename), 'rb') as f:preprocess_pipeline = dill.load(f)
                        with open(os.path.join(pipeline_foldername, le_transformer_filename), 'rb') as f:le_transformer = dill.load(f)
                        return preprocess_pipeline, le_transformer

                    preprocess_pipeline, le_transformer = load_preprocess(
                        pipeline_foldername, pipeline_filename, le_transformer_filename)

                    # Loading the saved machine learning model
                    st.cache_data
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