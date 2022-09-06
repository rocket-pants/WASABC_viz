## using streamlit to display WASABC data
import streamlit as st
import pandas as pd, numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# streamlit config
st.set_page_config(
    page_title='WASABC',
    page_icon=':beer',
    layout="wide")

# seaborn config
sns.set()

st.title('Categories')


with st.sidebar:
    st.image('wasabc.png')
    st.markdown(
    """
    Some data viz for the past several years of WASABC  

    Over the years AABC and BJCP have changed style guidelines. This application maps all old styles to the AABC 2022 categories. Where styles are no longer included in AABC the closest style is used.

    """
    )

# load data
#@st.cache
def load_data():
    data=pd.read_csv('WASABC_clean_data.csv', encoding='utf-8')
    return data


df=load_data()

df_cat=pd.read_csv('category names 2022.csv', usecols=['Category', '2022 Category Name'])
df_cat=df_cat.rename(columns =  {'2022 Category Name':'Category name'})

# clean data
df=df[df['Score']!=0]


# add and clean category name
df=pd.merge(df, df_cat[['Category','Category name']], how = 'left', on = 'Category')
df=df.sort_values(by=['Category', 'Subcategory', 'Year'])

categories = df['Category name'].unique()

cats=st.multiselect(
    'Select one or more categories',
    categories ,    'IPA')

# df_cat=df[['Category','Category name', 'Year', 'Score']][df['Category name']==cats]

# st.write(df_cat[['Category name', 'Year', 'Score']].groupby('Year', as_index=False)['Score'].mean())

fig=px.line(df[['Category','Category name', 'Year', 'Score']][df['Category name'].isin(cats)].groupby(['Category','Category name','Year'], as_index=False)['Score'].mean(), 
x='Year', y='Score', color='Category name', markers=True)
st.plotly_chart(fig)

# fig=plt.figure(figsize=(12,6))
# sns.lineplot(data=df[['Category name', 'Year', 'Score']].groupby(['Category name','Year'], as_index=False)['Score'].mean(), x='Year', y='Score', hue='Category name')
# st.pyplot(fig)
# st.line_chart(data=df_cat[['Category name', 'Year', 'Score']].groupby('Year', as_index=False)['Score'].mean(), x='Year')

# st.write(int(df_cat['Score'][df_cat['Category name']==cats].mean()))
# fig=plt.figure(figsize=(10,4))
# sns.barplot(data=df_entries_per_year, x='Year', y='Entries', color='orange')
# plt.title('Entries per year')
# st.pyplot(fig)