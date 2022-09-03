## using streamlit to display WASABC data
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

# streamlit config
st.set_page_config(
    page_title='WASABC',
    page_icon=':beer',
    layout="wide")

# seaborn config
sns.set()

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

st.title('WASABC through the years')


with st.sidebar:
    st.image('wasabc.png')
    st.markdown(
    """
    Some data viz for the past several years of WASABC  

    Over the years AABC and BJCP have changed style guidelines. This application maps all old styles to the AABC 2022 categories. Where styles are no longer included in AABC the closest style is used.

    """
    )

# yeah
df_entries_per_year=df[['Year', 'Entry Number']].groupby('Year', as_index=False).count()
df_entries_per_year=df_entries_per_year.rename(columns={'Entry Number':'Entries'})

col1, col2, col3 = st.columns([1,3,1])

with col2:
    fig=plt.figure(figsize=(10,4))
    sns.barplot(data=df_entries_per_year, x='Year', y='Entries', color='orange')
    plt.title('Entries per year')
    st.pyplot(fig)

# st.bar_chart(df_entries_per_year, x='Year', y='Entry Number')

years=df['Year'].sort_values().unique()

# years=years.
col1, col2 = st.columns([1,3])
with col1:
    all_years = st.button('Select all years?')
    clear_years = st.button('Clear years')

with col2:
    if not all_years:
        year = st.select_slider(
       'Select year:',
        options=years, value = 2022)

# st.write(all_years, year)
# df_count_by_cat = df[['Category', 'Entry Number']][df['Year']==year].groupby('Category', as_index=False).count()
# df_count_by_cat=df_count_by_cat.rename(columns={'Entry Number':'Entries'})

# fig=plt.figure(figsize=(10,4))
# sns.barplot(data=df_count_by_cat, x='Category', y='Entries', color='orange')
# plt.title('Entries per category')
# st.pyplot(fig)

# st.dataframe(df_count_by_cat)

col1, col2 = st.columns(2)
with col1:
    # count of entries by category
    if all_years:
        fig=plt.figure(figsize=(10,4))
        df_count_by_cat = df[['Category','Category name', 'Entry Number']].groupby(['Category','Category name'], as_index=False).count() #.sort_values(by='Category', ascending = False)
        df_count_by_cat=df_count_by_cat.rename(columns={'Entry Number':'Entries'})
        
        # st.dataframe(df_count_by_cat)
        sns.barplot(data=df_count_by_cat, x='Category name', y='Entries', color='orange')
        plt.title('Entries per category')
        plt.xticks(rotation=90)
        st.pyplot(fig)
    else:
        fig=plt.figure(figsize=(10,4))
        df_count_by_cat = df[['Category','Category name', 'Entry Number']][df['Year']==year].groupby(['Category', 'Category name'], as_index=False).count()
        df_count_by_cat=df_count_by_cat.rename(columns={'Entry Number':'Entries'})
        
        sns.barplot(data=df_count_by_cat, x='Category name', y='Entries', color='orange')
        plt.title('Entries per category')
        plt.xticks(rotation=90)
        st.pyplot(fig)

with col2:
    # scores by style
    # count of entries by category
    if all_years:
        fig=plt.figure(figsize=(10,4))
        sns.boxplot(x=df['Category name'], y=df['Score'], color='orange')
        plot_title = 'Category scores'
        plt.title(plot_title)
        plt.xticks(rotation=90)
        st.pyplot(fig)
    else:
        fig=plt.figure(figsize=(10,4))
        # df_count_by_year = df[df['Year']==year].groupby('Category', as_index=False).sum()
        # df_count_by_cat=df_count_by_cat.rename(columns={'Entry Number':'Entries'})
        
        sns.boxplot(x=df[df['Year']==year]['Category name'], y=df[df['Year']==year]['Score'], color='orange')
        plot_title = 'Category scores for '  + str(year)
        plt.title(plot_title)
        plt.xticks(rotation=90)
        st.pyplot(fig)
