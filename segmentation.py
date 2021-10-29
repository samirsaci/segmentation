import streamlit as st
from streamlit import caching
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import math
from scipy import stats
from scipy.stats import shapiro
import base64

from utils.processing import(
    load_upload,
    load_local,
    abc_processing
)
from utils.ui import (
    introduction,
    abc_ui,
    pareto_ui,
    dataset_ui,
    normality_ui,
    distribution_ui
)
from utils.plot import (
    pareto_plot,
    abc_analysis,
    normality_test,
    distribution
)

# Set page configuration
st.set_page_config(page_title ="Statistical Product Segmentation",
                    initial_sidebar_state="expanded",
                    layout='wide',
                    page_icon="🛒")

# Page Title 
introduction()


# Set up the page
@st.cache(persist=False,
          allow_output_mutation=True,
          suppress_st_warning=True,
          show_spinner= True)
# Preparation of data
def prep_data(df):
    df_input = df.rename({date_col:"ds",metric_col:"y"},errors='raise',axis=1)
    st.markdown("The selected date column is now labeled as **ds** and the values columns as **y**")
    df_input = df_input[['ds','y']]
    df_input =  df_input.sort_values(by='ds',ascending=True)
    return df_input

# -- Page 
caching.clear_cache()

# Information about the Dataset
st.header("**Information about the Dataset 🛠️**")

# Upload Data Set
st.sidebar.subheader('Load a Dataset loading 💾')
st.sidebar.write("Upload your dataset (.csv)")
# Upload
input = st.sidebar.file_uploader('')
if input is None:
    dataset_type = 'LOCAL'
    st.sidebar.write("_If you do not upload a dataset, an example is automatically loaded to show you the features of this app._")
    df_abc, df = load_local()
    date_col, metric_col, list_var, list_sku, family_col = dataset_ui(df_abc, df, dataset_type)
else:
    dataset_type = 'UPLOADED'
    with st.spinner('Loading data..'):
        df = load_upload(input)
        st.write(df.head())
        df_abc = pd.DataFrame()
    date_col, metric_col, list_var, list_sku, family_col = dataset_ui(df_abc, df, dataset_type)
# User Guide/Source Guide
st.sidebar.markdown('''
        **📖 [User Guide]
        (https://towardsdatascience.com/product-segmentation-for-retail-with-python-c85cc0930f9a)**
    ''')
st.sidebar.markdown('''
        **👁️‍🗨️ [Source Code]
        (https://towardsdatascience.com/product-segmentation-for-retail-with-python-c85cc0930f9a)**
    ''')
# Process filtering
st.write("\n")
st.subheader('''
📊 Your dataset with the final version of the features''')
df = df[list_var].copy()
st.write(df.head(2))

# Start Calculation ?
if st.checkbox('Start Calculation?',key='show', value=False):
    start_calculation = True
else:
    if dataset_type == 'LOCAL':
        start_calculation = True
    else:
        start_calculation = False

# Process df_abc for uploaded dataset
if dataset_type == 'UPLOADED' and start_calculation:
    df_abc, n_sku, n_a, n_b, to_a, to_b  = abc_processing(df, date_col, metric_col, list_sku)

else:
    list_sku = ['SKU', 'ITEM', 'FAMILY', 'CATEGORY', 'STORE']

# Start Calculation after parameters fixing
if start_calculation:

    # Part 1: Pareto Analysis of the Sales
    st.header("**Pareto Analysis 🛠️**")
    nsku_qty80, qty_nsku20 = pareto_plot(df_abc)
    pareto_ui(df_abc, nsku_qty80, qty_nsku20)

    # Part 2: ABC Analysis
    interval, list_family = abc_ui(df_abc, family_col)
    abc_analysis(df_abc, interval, list_family, family_col)

    # Part 3: Normality Test
    normality_ui()
    normality_test(df_abc, interval, family_col)

    # Part 4: Low CV Distribution
    distribution_ui()
    distribution(df_abc, df, date_col)
                
            
    st.header('**Export results ✨**')
    st.write("_Finally you can export the results of your segmentation with all the parameters calculated._")
    if st.checkbox('Export Data',key='show'):
        with st.spinner("Exporting.."):
            st.write(df_abc.head())
            df_abc = df_abc.to_csv(decimal=',')
            b64 = base64.b64encode(df_abc.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

        
