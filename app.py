import streamlit as st
from predict import showPredictPage
from explore import showExplorePage

pageToView = st.sidebar.selectbox('Explore or Predict', ('Predict', 'Explore'))

if pageToView == 'Predict':
    showPredictPage()
else:
    showExplorePage()