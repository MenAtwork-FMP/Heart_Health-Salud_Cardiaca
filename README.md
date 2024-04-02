# Heart Health Assessment / Evaluación de Salud Cardiaca
 
![](https://img.shields.io/github/last-commit/MenAtwork-FMP/Heart_Health-Salud_Cardiaca)
![](https://img.shields.io/github/languages/count/MenAtwork-FMP/Heart_Health-Salud_Cardiaca)
![](https://img.shields.io/github/languages/top/MenAtwork-FMP/Heart_Health-Salud_Cardiaca)
![](https://img.shields.io/github/repo-size/MenAtwork-FMP/Heart_Health-Salud_Cardiaca)
![](https://img.shields.io/github/directory-file-count/MenAtwork-FMP/Heart_Health-Salud_Cardiaca)
![](https://img.shields.io/github/license/MenAtwork-FMP/Heart_Health-Salud_Cardiaca)


# Problem Statement:


#### English:
Heart Disease is among the most prevalent chronic diseases impacting millions of people around the world. Understanding the complex interplay of factors such as cholesterol levels, blood pressure, body mass index (BMI), physical activity levels, dietary habits, and family history of heart disease is crucial. These variables, among others, collectively contribute to an individual's overall risk profile for cardiovascular events. A holistic approach that considers these variables can provide a more accurate assessment of an individual's heart health and guide personalized interventions to reduce the risk of heart attacks.

By conducting a thorough evaluation of these key variables, healthcare providers can develop targeted interventions and lifestyle modifications to improve heart health and reduce the risk of cardiovascular events in patients. This comprehensive approach is essential for effectively managing heart health and promoting overall well-being.

The tool here developed, provides a preliminary concept to further mature into a reliable assistance for healthcare providers and patients alike to take targeted actions on improving their risk profile.


#### Spanish:
La enfermedad cardíaca es una de las enfermedades crónicas más prevalentes que afecta a millones de personas en todo el mundo. Comprender la compleja interacción de factores como los niveles de colesterol, la presión arterial, el índice de masa corporal (IMC), los niveles de actividad física, los hábitos alimenticios y la historia familiar de enfermedad cardíaca es crucial. Estas variables, entre otras, contribuyen colectivamente al perfil de riesgo general de un individuo para eventos cardiovasculares. Un enfoque holístico que tenga en cuenta estas variables puede proporcionar una evaluación más precisa de la salud cardíaca de un individuo y guiar intervenciones personalizadas para reducir el riesgo de ataques cardíacos.

Al realizar una evaluación exhaustiva de estas variables clave, los proveedores de atención médica pueden desarrollar intervenciones dirigidas y modificaciones en el estilo de vida para mejorar la salud cardíaca y reducir el riesgo de eventos cardiovasculares en los pacientes. Este enfoque integral es esencial para gestionar de manera efectiva la salud cardíaca y promover el bienestar general.

La herramienta aquí desarrollada proporciona un concepto preliminar para madurar en una asistencia confiable para proveedores de atención médica y pacientes por igual, para tomar acciones específicas para mejorar su perfil de riesgo|


# Deployed app link

Check out the deployed app at https://heartrisk.streamlit.app/

# Data used

The utilized dataset was modified from the original.
Get the project sample data from https://drive.google.com/file/d/1j48kuBVZ70pe_GsT97geOiE8ye7jpc4L/view?usp=drive_link  


Or the original dataset version
from https://www.kaggle.com/datasets/mahad049/heart-health-stats-dataset/download?datasetVersionNumber=1


# Programming Languages Used
<img src = "https://img.shields.io/badge/-Python-3776AB?style=flat&logo=Python&logoColor=white">


# Python Libraries and tools Used
<img src="http://img.shields.io/badge/-Git-F05032?style=flat&logo=git&logoColor=FFFFFF"> <img src = "https://img.shields.io/badge/-NumPy-013243?style=flat&logo=NumPy&logoColor=white"> <img src = "https://img.shields.io/badge/-Pandas-150458?style=flat&logo=pandas&logoColor=white"> <img src="http://img.shields.io/badge/-sklearn-F7931E?style=flat&logo=scikit-learn&logoColor=FFFFFF">  <img src = "https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white"> <img src = "https://img.shields.io/badge/-mlflow-0194E2?style=flat&logo=mlflow&logoColor=white"> <img src = "https://img.shields.io/badge/-Pydantic-000000?style=flat&logoColor=white">


## To run the repository locally

First, clone the repo
```bash
    git clone https://github.com/MenAtwork-FMP/Heart_Health-Salud_Cardiaca.git
```

Go to the project directory (for instance hearthealth), create a conda enviroment and activate it. Change ".condaenv" for whatever name you want for the enviroment.

```bash
    cd hearthealth
    conda create -n .condaenv python=3.10
    conda activate .condaenv
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run all the code. If you run aa00_Runrepo.py, the script will execute all the different steps sequentially.
(aa01_Utility, aa02_Dataset, aa03_Preprocessing, aa04_Model)

```bash
  python aa00_Runrepo.py
```

Or you can run each python file individually to follow along the code

Visualize the metrics in different experiments

```bash
  mlflow ui
```

Make predictions using trained model

```bash
  streamlit run webapp.py
```

## 🚀 About Me
TBD.


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fabio-mena-5416264/)