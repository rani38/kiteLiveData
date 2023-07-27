import pandas as pd
import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os
from main import plot_ADX
load_dotenv()
# Function to connect to the MySQL database and fetch data

def fetch_data_from_mysql():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("hostname"),
            user="root",
            password=os.getenv("password"),
            database=os.getenv("database")
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT ADX,DI_plus,DI_minus FROM adxdis;"
            cursor.execute(query)
            data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=column_names)
            value = plot_ADX(df)
            connection.close()
            return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Fetch data from MySQL
df = fetch_data_from_mysql()

if df is not None:
    st.write("Data from MySQL:")
    st.write(df)
else:
    st.error("Failed to fetch data from MySQL.")