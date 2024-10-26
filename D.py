#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install streamlit')


# In[23]:


import subprocess

# Use subprocess to execute the shell command
subprocess.run(['pip', 'install', 'streamlit'], check=True)


# In[2]:


import streamlit as st
import pandas as pd
from pickle import load
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler


# In[3]:


# Page title

st.title("Forecasting Stock Prices App")


# In[4]:


# Sidebar menu

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "Forecasting Stock"],
        icons=["house","graph-up"],
        menu_icon="cast",
        default_index=0,
    )


# In[5]:


# Home page content

if selected == "Home":
    stock_symbol = "RELIANCE"
    st.header("Welcome to the Forecasting Stock Prices App")
    data=pd.read_csv(r"RELIANCE.NS.csv",parse_dates=True)
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Close'],
        mode='lines', name='Close Price',  # Changed mode to 'lines'
        line=dict(color='blue', width=2),
        hovertemplate='Date: %{x}<br>Close: %{y}<extra></extra>'
    ))

    # Annotate significant peaks
    peaks = data[data['Close'] == data['Close'].max()]
    for peak in peaks.itertuples():
        fig.add_annotation(
            x=peak.Date, y=peak.Close,
            text="Peak",
            showarrow=True,
            arrowhead=1,
            ax=-10,
            ay=-40
        )

    fig.update_layout(
        title=f'{stock_symbol} Stock Close Price (2000-2024)',
        xaxis_title='Date',
        yaxis_title='Close Price',
        xaxis=dict(
            rangeslider=dict(visible=True),
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            showline=True,
            showgrid=True
        ),
        yaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            showline=True,
            showgrid=True
        ),
        hovermode='x unified',
        template='plotly_dark'
    )

    st.plotly_chart(fig)


# In[6]:


# Stock Forecasting page content

selected = st.sidebar.selectbox("Choose an option", ["Home", "Forecasting Stock", "About"])

if selected == "Home":
    st.title("Welcome to the Home Page")
    st.write("This is the home page of our stock forecasting application.")
    
elif selected == "Forecasting Stock":
    st.markdown(
        """
        <style>
        .header2 {
            color: orange;
            font-size: 28px;
            text-align: center;
            padding: 8px;
            background-color: black;
            border-radius: 3px;
            margin-bottom: 0px;
         }
         </style>
         """,
        unsafe_allow_html=True
    )
st.markdown('<p class="header2">Stock Forecasting Using Linear Regression</p>', unsafe_allow_html=True)
stock_symbol = st.text_input("Stock Symbol", "RELIANCE")
start_date = st.date_input("Start Date", pd.to_datetime("2024-04-30"))
end_date = st.date_input("End Date", pd.to_datetime("2025-05-01"))


# In[7]:


# Ensure dates

if not np.is_busday(start_date):
    start_date = pd.bdate_range(start=start_date, periods=1)[0]
if not np.is_busday(end_date):
    end_date = pd.bdate_range(end=end_date, periods=1)[0]


# In[18]:


# Show user input

st.write("Stock Symbol:", stock_symbol)
st.write("Start Date:", start_date)
st.write("End Date:", end_date)

filename = 'Reliance_Industries_Stock_Market_Prediction(PROJECT).ipynb'
predtdf=data.to_csv(filename, index=False)


# In[ ]:


# Convert to pandas datetime object

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
# Filter the DataFrame based on start_date

result = predtdf[(predtdf['Dates'] >= start_date_str) & (predtdf['Dates'] <= end_date_str)]['Predicted_values']


# In[22]:


# Apply more styling options to the DataFrame

styled_result = (
    result.to_frame()  # Convert Series to DataFrame
    .style
    .set_properties(**{'background-color': 'lightyellow',  # Set background color
                           'color': 'black',  # Set text color
                           'border': '1px solid black',  # Add border
                           'text-align': 'center'})  # Align text
    .set_table_styles([{'selector': 'th',  # Apply styles to table headers
                            'props': [('background-color', 'lightblue'),  # Set header background color
                                      ('color', 'black'),  # Set header text color
                                      ('font-weight', 'bold'),  # Make header text bold
                                      ('text-align', 'center')]},  # Align header text
                           {'selector': 'td',  # Apply styles to table data cells
                            'props': [('text-align', 'center')]}])  # Align cell text
    .format({'predicted': '{:.2f}'})  # Format predicted values to two decimal places
    )

# Display the styled DataFrame

st.write("Predicted Values:")
st.write(styled_result)


# In[ ]:




