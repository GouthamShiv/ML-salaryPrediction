import streamlit as st
import pickle as pkl
import numpy as np


def loadModel():
    with open('saved_steps.pkl', 'rb') as file:
        data = pkl.load(file)
    return data


data = loadModel()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']


def showPredictPage():
    st.title('Software Developer Salary Prediction')
    st.write("""### We need some information to predict the salary""")

    countries = (
        'United States of America',
        'India',
        'Germany',
        'United Kingdom of Great Britain and Northern Ireland',
        'Canada',
        'France',
        'Brazil',
        'Spain',
        'Netherlands',
        'Australia',
        'Poland',
        'Italy',
        'Russian Federation',
        'Sweden',
        'Turkey',
        'Switzerland',
        'Israel',
        'Norway',
    )

    educationList = (
        'Less than Bachelor’s',
        'Bachelor’s degree',
        'Master’s degree',
        'Post graduation',
    )

    country = st.selectbox('Country', countries)
    education = st.selectbox('Education Level', educationList)
    experience = st.slider('Years of experience', 0, 50, 3)

    predict = st.button('Estimate Salary')
    if predict:
        userInput = np.array([[country, education, experience]])
        userInput[:, 0] = le_country.transform(userInput[:, 0])
        userInput[:, 1] = le_education.transform(userInput[:, 1])
        userInput = userInput.astype(float)

        salary = regressor.predict(userInput)
        st.subheader(f'The estimated salary is ${salary[0]:.2f}')