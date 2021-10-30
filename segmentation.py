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
    abc_processing)
from utils.ui import (
    introduction,
    abc_ui,
    pareto_ui,
    dataset_ui,
    normality_ui,
    distribution_ui,
    upload_ui,
    export_ui)
from utils.plot import (
    pareto_plot,
    abc_analysis,
    normality_test,
    distribution,
    abc_barplot)

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
    col = df.columns
    return col

# -- Page 
caching.clear_cache()

# Information about the Dataset
st.header("**Information about the Dataset 🛠️**")

# Upload Data Set
date_col, metric_col, list_var, sku_col, family_col, dataset_type, df, df_abc = upload_ui()


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
    df_abc, n_sku, n_a, n_b, to_a, to_b  = abc_processing(df, date_col, metric_col, sku_col, family_col)
else:
    list_sku = ['SKU', 'ITEM', 'FAMILY', 'CATEGORY', 'STORE']

# Start Calculation after parameters fixing
if start_calculation:

    # Part 1: Pareto Analysis of the Sales
    st.header("**Pareto Analysis 💹**")
    nsku_qty80, qty_nsku20 = pareto_plot(df_abc)
    pareto_ui(df_abc, nsku_qty80, qty_nsku20)

    # Part 2: ABC Analysis
    interval, list_family = abc_ui(df_abc, family_col)
    abc_analysis(df_abc, interval, list_family, family_col)
    abc_barplot(df_abc, family_col, metric_col)

    # Part 3: Normality Test
    normality_ui()
    normality_test(df_abc, interval, family_col)

    # Part 4: Low CV Distribution
    distribution_ui()
    distribution(df_abc, df, date_col, sku_col, metric_col)
                
    # Part 5: Export Results
    export_ui(df_abc)

        
