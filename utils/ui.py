import streamlit as st
import pandas as pd
from utils.processing import (
    load_local,
    load_upload)
import base64

def introduction():
    st.title('ABC Analysis & Product Segmentation 🛍️')
    st.markdown('''
        _For more information about the theory behind: **[Article - Product Segmentation for Retail](https://towardsdatascience.com/product-segmentation-for-retail-with-python-c85cc0930f9a)**_
    ''')
       # User Guide/Source Guide
    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown('''
              📖 <a href="https://github.com/samirsaci/segmentation">**User Guide**</a>
        ''')
    with col2:
        st.markdown('''
             👁️‍🗨️ <a href="https://github.com/samirsaci/">**Source Code**</a>
        ''', unsafe_allow_html=True)
    with st.beta_expander('''How can this app help you?'''):
        st.write('''This Streamlit Web Application has been designed for **Supply Chain Engineers** to support them in their **Inventory Management**.
        It will help you to automate **product segmentation using statistics**.''')
        st.markdown(
    """
    1. 💾 Upload a dataset or use the example  _(If you use the example you do not need to follow the next steps.)_
    2. 📅 [Parameters] select the columns for the date _(day, week, year)_ and the values _(quantity, $)_ 
    3. 📉 [Parameters] select all the columns you want to keep in the analysis
    4. 🏬 [Parameters] select all the related to product master data _(SKU ID, FAMILIY, CATEGORY, STORE LOCATION)_
    5. 🛍️ [Parameters] select one feature you want to use for analysis by family
    6. 🖱️  Click on **Start Calculation?** to launch the analysis
     
    \
    _For more details have a look at the [📖 User Guide](https://github.com/samirsaci/)_

    """)

def upload_ui():
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
 
    # Process filtering
    st.write("\n")
    st.subheader('''📊 Your dataset with the final version of the features''')
    df = df[list_var].copy()
    st.write(df.head(2))

    return date_col, metric_col, list_var, list_sku, family_col, dataset_type, df, df_abc



def dataset_ui(df_abc, df, dataset_type):
    # Show Features
    st.subheader("🔧 Please select columns for the following features")
    columns = df.columns
    # st.write(list(columns))
    col1, col2 = st.beta_columns(2)
    with col1:
        date_col = st.selectbox("Select date column",index= len(df.columns) - 2,options=columns,key="date")
    with col2:
        metric_col = st.selectbox("Select values column",index=len(df.columns)-1,options=columns,key="values")
    output = 0 

    st.subheader('🛎️ Please choose the following features in your dataset')
    with st.beta_expander("FEATURES TO USE FOR THE ANALYSIS"):
        st.markdown('''
        Select the columns that you want to include in the analysis of your sales records._
    ''')
        dict_var = {}
        for column in df.columns:
            dict_var[column] = st.checkbox("{} (IN/OUT)".format(column), value = 1)

    if dataset_type == 'UPLOADED':
        with st.beta_expander("FEATURES FOR THE SKU INFORMATION (ID, STORE, FAMILY)"):
            st.markdown('''
        Select the columns used for product master data (SKU ID, Family, Category, Store Location)_
    ''')
            dict_sku = {}
            for column in df.columns:
                if column in ['SKU', 'ITEM', 'FAMILY', 'CATEGORY', 'STORE']:
                    val = 1
                else:
                    val = 0
                dict_sku[column] = st.checkbox("{} (YES/NO)".format(column) , value = val)
    else:
        with st.beta_expander("FEATURES FOR THE SKU INFORMATION (ID, STORE, FAMILY)"):
            st.markdown('''
        _Select the columns used for product master data (SKU ID, Family, Category, Store Location)_
    ''')
            dict_sku = {}
            for column in df.columns:
                if column in ['SKU', 'ITEM', 'FAMILY', 'CATEGORY', 'STORE']:
                    val = 1
                else:
                    val = 0
                dict_sku[column] = st.checkbox("{} (YES/NO)".format(column) , value = val)

    with st.beta_expander("FEATURES FOR THE SKU FAMILY"):
        st.markdown('''
        _Select the column you want to use to group your SKUs (Category, Sub-Category, Department)_
    ''')
        family_col = st.selectbox("Select a column for the product family", index= 3,options=columns,key="date")

    filtered = filter(lambda col: dict_var[col]==1, df.columns)
    list_var =list(filtered)

    filtered = filter(lambda col: dict_sku[col]==1, df.columns)
    list_sku =list(filtered)


    return date_col, metric_col, list_var, list_sku, family_col

def pareto_ui(df_abc, nsku_qty80, qty_nsku20):
    col1,col2 = st.beta_columns(2)
    with col1:
        st.write('80% of your volume is generated by **{}% for your SKU portofolio**'.format(nsku_qty80))
    with col2:    
        st.write('20% of your SKU portofolio represent **{}% for your volume**'.format(qty_nsku20))

def abc_ui(df, family_col):
    st.header("**ABC Analysis with Demand Variability 🔤**")
    col1,col2 = st.beta_columns(2)
    with col1:
            interval = st.slider(
            'SET THE MAXIMUM VALUE FOR Y-AXIS CV',
            0, 
            int(df['CV'].max())
            , value = 4)

    dict_family = {}
    with st.beta_expander("SELECT THE SKU FAMILIES YOU WANT TO INCLUDE IN THE CHART"):
        for miff in df[family_col].unique():
                dict_family[miff] = st.checkbox("{} (YES/NO)".format(miff) , value = 1)
    filtered = filter(lambda col: dict_family[col]==1, df[family_col].unique())
    list_family =list(filtered)

    return interval, list_family


def normality_ui():
    st.header("**Normality Test ✔️**")
    st.markdown(
'''_Can we reject the null hypothesis that the sales distribution of the item follows a normal distribution?_
''')
    st.markdown(
        '''
This model is using the Shapiro-Wilk test for normality implemented using Scipy library of python 
_(**[Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)**)_.
''')

def distribution_ui():
    st.header("**Example of distributions with a low CV 📟**")
    st.markdown(
'''
_A rule of thumb to estimate the normality of a distribution is to 
assume that below 0.5 you can assumte that the distribution is normal._
''')
    
def export_ui(df_abc):
    st.header('**Export results ✨**')
    st.write("_Finally you can export the results of your segmentation with all the parameters calculated._")
    if st.checkbox('Export Data',key='show'):
        with st.spinner("Exporting.."):
            st.write(df_abc.head())
            df_abc = df_abc.to_csv(decimal=',')
            b64 = base64.b64encode(df_abc.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)