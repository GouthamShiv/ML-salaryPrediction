FROM python:latest

WORKDIR /opt/app

ADD ["app.py", "explore.py", "predict.py", "saved_steps.pkl", "survey_results_public.csv", "dependencies.txt", "/opt/app/"]

RUN pip install --upgrade pip

RUN pip install -r dependencies.txt

CMD ["streamlit", "run", "app.py"]

EXPOSE 8501