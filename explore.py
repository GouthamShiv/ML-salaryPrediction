import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to group countries which are having records less than provided cut-off
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

# Function to convert the YearsCode to float value and map
# TEXT values ('More than 50 years' & 'Less than 1 year') to float as well
def clean_experience(exp):
    if exp == 'More than 50 years':
        return 50
    if exp == 'Less than 1 year':
        return 0.5
    return float(exp)

# Function to convert the EdLevel to simpler category
def clean_education(ed):
    if 'Bachelor’s degree' in ed:
        return 'Bachelor’s degree'
    if 'Master’s degree' in ed:
        return 'Master’s degree'
    if 'Professional degree' in ed or 'Other doctoral' in ed:
        return 'Post graduation'
    return 'Less than Bachelor’s'

@st.cache
def loadData():
    df = pd.read_csv('survey_results_public.csv')

    # Filter to required columns only
    df = df[["Country", "EdLevel", "YearsCode", "Employment", "ConvertedCompYearly"]]

    # Rename the column ConvertedCompYearly to Salary
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

    # Filter data frame to eleminate rows not having salary
    df = df[df["Salary"].notnull()]

    # Drop rows if any of it's fields are not having value (NA)
    df = df.dropna()

    # Filter for full-time employed records and drop 'Employment' column
    df = df[df['Employment'] == 'Employed full-time']
    df = df.drop('Employment', axis=1)

    # Function call to group the countries to 'Other' category if count of records for that country is less than 400
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)


    # Filter the data frame [salary <= 250000 and salary >= 10000]
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']

    # Clean experience and education
    df['YearsCode'] = df['YearsCode'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)

    return df

df = loadData()

def showExplorePage():
    st.title('Explore Software Engineer Salaries')
    st.write("""### Stack Overflow Developer Survey 2021""")

    # PiChart
    data = df['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal') # Equal aspect ratio ensures that the PIE is drawn as a circle.

    st.write("""#### Number of data from different countries""")
    st.pyplot(fig1)

    # BarChart
    st.write("""#### Mean Salary Based on Country""")
    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    # LineChart
    st.write("""#### Mean Salary Based on Experience""")
    data = df.groupby(['YearsCode'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)
