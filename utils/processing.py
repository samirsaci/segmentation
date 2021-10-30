import pandas as pd
import streamlit as st
import numpy as np
from scipy import stats
from scipy.stats import shapiro


# Load data from user upload
def load_upload(input):
    # Create Data Frame
    df = pd.read_csv(input,sep=None ,engine='python', encoding='utf-8',
                parse_dates=True,
                infer_datetime_format=True, index_col=0)

    return df

# Load data from the local repository 
def load_local():
    # Create Data Frame
    df_abc = pd.read_csv('data/example_segmentation.csv',sep=None ,engine='python', encoding='utf-8',
                parse_dates=True,
                infer_datetime_format=True)
    # Mapping Family
    for col in ['CATEGORY', 'FAMILY']:
        LIST_UNIQUE = df_abc[col].unique()
        df_abc[col] = df_abc[col].map(
        dict(zip(LIST_UNIQUE, [col + '_' + str(i) for i in range(len(LIST_UNIQUE))])))
    # Sample data used to show the head
    df = pd.read_csv('data/df_sample_dist.csv',sep=None ,engine='python', encoding='utf-8',
                parse_dates=True,
                infer_datetime_format=True, index_col=0)
    
    return df_abc, df

def abc_processing(df, date_col, metric_col, sku_col, family_col):
    # Group by (Item + Family)
    GPBY = [sku_col, family_col]
    # DAYS 
    LIST_DAYS = list(df[date_col].unique())
    # Start Calculation
    df_abc = pd.pivot_table(df, 
    index=GPBY, columns=date_col, values=metric_col, aggfunc=np.sum)
    df_abc.reset_index(inplace = True)
    # Total Units
    df_abc['QTY'] = df_abc[LIST_DAYS].sum(axis = 1)
    # Calculate mean and standard deviation
    # Mean
    df_abc['MEAN'] = df_abc[LIST_DAYS].mean(axis = 1)
    df_abc['MAX'] = df_abc[LIST_DAYS].max(axis = 1)
    df_abc['%MAX/MEAN'] = df_abc['MAX']/df_abc['MEAN']
    # Filter out the reference withou sales
    df_abc = df_abc[df_abc['MEAN']>0]
    # Standard
    df_abc['STD'] = df_abc[LIST_DAYS].std(axis = 1)
    # Coefficient of Variation
    df_abc['CV'] = df_abc['STD']/df_abc['MEAN']
    df_abc.reset_index(inplace = True)
    # Normalility Test
    df_abc['NORMALITY_P'] = df_abc[LIST_DAYS].apply(lambda row : stats.shapiro(row)[1], axis = 1)
    alpha = 0.05
    df_abc['NOT_NORMAL'] = df_abc['NORMALITY_P'] < alpha
    # Number of days of active sales
    df_abc['DAYS_ACTIVE'] = (df_abc[LIST_DAYS]>0).sum(axis=1)
    # # ABC SKU-LEVEL
    df_abc = df_abc.drop(LIST_DAYS, axis =1).copy()
    df_abc['QTY%'] = (100*df_abc['QTY']/df_abc['QTY'].sum())
    # Sort 
    df_abc.sort_values(['QTY%'], ascending = False, inplace = True, ignore_index=True)
    df_abc['QTY%_CS'] = df_abc['QTY%'].cumsum()
    # A, B, C on SKU Number
    n_sku = len(df_abc)
    n_a, n_b = int(0.05*n_sku), int(0.5*n_sku)
    df_abc['SKU_ID'] = pd.Series(range(1, len(df_abc))).astype(int)
    df_abc['SKU_%'] = 100 * (df_abc['SKU_ID'] / len(df_abc))
    df_abc['ABC'] = pd.Series(range(len(df_abc))).apply(lambda t: 'A' if t <= n_a-1 else 'B' if t <= n_b-1 else 'C')
    # A, B, C on turnover
    to_a, to_b = df_abc[df_abc['SKU_ID']==n_a]['QTY%'].max(), df_abc[df_abc['SKU_ID']==n_b]['QTY%'].max()
    # FOCUS = F(CV, ABC)
    df_abc['FOCUS'] = df_abc[['ABC','CV']].apply(lambda t:
    'LOW_IMPORTANCE' if t['ABC']=='C' else 'STABLE_DEMAND' if (t['CV']<=1) else 'HIGH_IMPORTANCE', axis = 1)

    return df_abc, n_sku, n_a, n_b, to_a, to_b 