import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def pareto_plot(df_abc):
    fig = px.line(
    data_frame=df_abc,
    width=800, 
    height=600,
    x='SKU_%', 
    y='QTY%_CS',
    labels={ "SKU_%": 'Percentage of SKU (%)',
    "QTY%_CS": 'Percentage of the Quantity (%)'}) #, title="ABC Analysis: Distribution by Quantity"
    # 5%, 20% of SKU (A and B)
    fig.add_vline(x=5, line_width=1, line_dash="dot", line_color="red")
    fig.add_vline(x=20, line_width=1, line_dash="dot", line_color="red")
    # 20%, 50% of SKU Number
    fig.add_hline(y=80, line_width=1, line_dash="dot", line_color="blue")
    fig.add_hline(y=95, line_width=1, line_dash="dot", line_color="blue")

    # Quick Analysis
    nsku_qty80 = round((df_abc[df_abc['QTY%_CS'] > 80]['SKU_%'].values[0]),2)
    qty_nsku20 = round((df_abc[df_abc['SKU_%'] > 20]['QTY%_CS'].values[0]),2)
    st.write(fig)

    return nsku_qty80, qty_nsku20

def abc_analysis(df, interval, list_family, family_col):
    fig = px.scatter(
    data_frame=df[df[family_col].isin(list_family)],
    width=800, 
    height=600,
    x='QTY%', 
    y='CV',
    color ='ABC',
    labels={ "QTY%": 'Percentage of Quantity (%)',
    "CV": 'Coefficient of Variation (σ/μ)'}) # ,title="Distribution by Demand Variability"
    colors = {'A':'red', 'B':'green', 'C':'blue'}
    # ABC
    n_sku = len(df)
    n_a, n_b = int(0.05*n_sku), int(0.5*n_sku)
    # A, B, C on turnover
    to_a, to_b = df[df['SKU_ID']==n_a]['QTY%'].max(), df[df['SKU_ID']==n_b]['QTY%'].max()
    # A, B and C
    fig.add_vline(to_a , line_width=1, line_dash="dot", line_color="red")
    fig.add_vline(to_b , line_width=1, line_dash="dot", line_color="red")
    # CV = 1
    fig.add_hline(1 , line_width=1, line_dash="dot", line_color="black")
    # Set limit in CV
    fig.update(layout_yaxis_range = [0,interval])
    st.write(fig)

def abc_barplot(df_abc, family_col, metric_col):
    # BAR PLOT OF SKU DISTRIBUTION BY FAMILY AND ABC CLASS
    df_dist = pd.DataFrame(df_abc[[family_col,'ABC', 'QTY']].groupby(
        [family_col,'ABC'])['QTY'].count()).reset_index()
    # Simple histogram
    fig = px.bar(data_frame=df_dist,
        width=800, 
        height=600,
        x=family_col,
        y = 'QTY',
        color = 'ABC',
        labels={ family_col: 'Split by {}'.format(family_col),
        metric_col: 'Number of SKU'}, barmode = "group")
    fig.update_traces(marker_line_width=1,marker_line_color="black")
    st.write(fig)

def normality_test(df, interval,family_col):
    fig = px.scatter(
    data_frame=df,
    width=800, 
    height=600,
    x='CV', 
    y='%MAX/MEAN',
    color ='NOT_NORMAL',
    labels={ "QTY%": 'Percentage of Quantity (%)',
    "CV": 'Coefficient of Variation (σ/μ)',
    'NOT_NORMAL': 'Distribution is not normal'})
    # ABC
    n_sku = len(df)
    n_a, n_b = int(0.05*n_sku), int(0.5*n_sku)
    # A, B, C on turnover
    to_a, to_b = df[df['SKU_ID']==n_a]['QTY%'].max(), df[df['SKU_ID']==n_b]['QTY%'].max()
    # A, B and C
    fig.add_vline(to_a , line_width=1, line_dash="dot", line_color="red")
    fig.add_vline(to_b , line_width=1, line_dash="dot", line_color="red")
    # CV = 1
    fig.add_hline(1 , line_width=1, line_dash="dot", line_color="black")

    st.write(fig)
    st.markdown(
    """
💡_For all the items that are normally distributed you can use a set of mathematical formula to estimate the minimum safety stock and build inventory management rules
to meet your targets of cycle service level. 
([More details in this Article](https://towardsdatascience.com/inventory-management-for-retail-stochastic-demand-3020a43d1c14))_
""")


def distribution(df_abc, df, date_col, sku_col, metric_col):
    # List of items with the lowest CV
    LIST_LOW = list(df_abc.sort_values(['CV'], ascending = True)[sku_col].values[0:3])
    LIST_DAYS = list(df[date_col].unique())
    col1, col2 = st.beta_columns(2)
    with col1:
        item_low = st.selectbox("TOP 3 SKU WITH THE LOWEST CV",index= 0, options =LIST_LOW,key="date")
    # ABC @ ITEM-LEVEL
    # Item with Low CV
    df_dist = df[df[sku_col].isin(LIST_LOW)].copy()
    # ABC SKU-LEVEL
    df_dist = pd.DataFrame(df_dist[[sku_col, date_col, metric_col]]
                        .groupby([sku_col, date_col]).sum()).reset_index()
    df_dist = df_dist[df_dist[sku_col]==item_low]
    # Simple histogram
    fig = px.histogram(data_frame=df_dist,
        width=800, 
        height=600,
        x=metric_col,
        labels={ metric_col: 'Sales Volume per Day (Units/Day)',
        "count": 'Number of Days'})
    fig.update_traces(marker_line_width=1,marker_line_color="black")
    st.write(fig)
    st.markdown(
    '''
    _Can you visually confirm if we can assume that the sales of the **item {}** are distributed normally?_
    '''.format(item_low))