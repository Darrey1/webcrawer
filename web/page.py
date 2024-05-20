import streamlit as st
import pandas as pd
import asyncio
import os 
import csv
import pandas as pd
import numpy as np
import pandas as pd
import streamlit as st
#import altair as alt
file_path = os.path.dirname(__file__)
dir_name = os.path.dirname(file_path)
app_csv = os.path.join(dir_name, 'output.csv')
shoesstore_cvs = os.path.join(dir_name, 'shoestore.csv')



def csv_table(df):
    
    df["Timespan"] = pd.to_datetime(df["Timespan"])

    config = {
            "Image": st.column_config.ImageColumn(
                "Image", help="Product market preview image",
                width=50
            ),
        "Url":st.column_config.LinkColumn(
            "Link",
            display_text="Product Url"
        ),
        "Price": st.column_config.NumberColumn(
            "Price (in USD)",
            help="The price of the product in USD",
            min_value=0,
            max_value=1000,
            step=1,
            format="$%d",
        ),
        "Timespan": st.column_config.DatetimeColumn(
            "Timespan",
            format="D MMM YYYY, h:mm a",
            step=60,
        )
    }
    
    st.data_editor(
        df,
        column_config=config,
        hide_index=True,
    )
    
    
    
def data_analysis(df):
    new_df = df.loc[:, ['Timespan', 'Price']]
    st.divider()
    st.write("A line chart of price against time",unsafe_allow_html=True)
    
    st.line_chart(new_df, x="Timespan", y="Price",color=["#0000FF"])#, "#0000FF"
    st.divider()
    st.write("A bar chart of price against time",unsafe_allow_html=True)
    st.bar_chart(new_df, x="Timespan", y="Price",color=["#FF0000"])
    
    


#@st.cache_data
def load_data():
    df1 = pd.read_csv(app_csv)
    df2 = pd.read_csv(shoesstore_cvs)
    return df1, df2


def streamlit_app():
    st.sidebar.title('Menu')
    df1, df2 =load_data()
    menu_options = ['Home', 'CSV Table', 'Analysis', 'Scrap']
    selected_option = st.sidebar.radio('Select an option', menu_options)


    if selected_option == 'Home':
        st.subheader('Web Scraping and Data Visualization for Product Monitoring',divider='rainbow')
        st.write('Our project aims to gather information about various products from websites. With web scraping technology, we extract details like product names, descriptions, images, prices, and ages. This data helps users make informed decisions and stay updated on product trends. Explore our site to learn more about product scraping and its applications.!')
        st.balloons()
        st.divider()
        new_df = df1.loc[:, ['Timespan', 'Price']]
        st.bar_chart(new_df, x="Timespan", y="Price")
        st.divider()
    elif selected_option == 'CSV Table':
        st.title('CSV Table')
        st.write('Web1 : https://www.aperfectdealer.com/')
        csv_table(df1)
        st.divider()
        st.write('Web2 : https://shoestores.com/')
        csv_table(df2)
    elif selected_option == 'Analysis':
        st.subheader('Market Data Analysis And Visualisation')
        data_analysis(df1)
    elif selected_option == 'Scrap':
        st.title('Scrap')
        st.write('Scraping functionality goes here.')
        
        
        

