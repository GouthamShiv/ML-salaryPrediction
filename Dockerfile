FROM python:3.9-slim-buster

WORKDIR /opt/app

ADD ["app.py", "explore.py", "predict.py", "saved_steps.pkl", "survey_results_public.csv", "dependencies.txt", "/opt/app/"]

RUN pip install --upgrade pip \
    && pip install -r dependencies.txt

CMD streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false

EXPOSE 8501