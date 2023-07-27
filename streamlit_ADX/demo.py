# main.py

import altair as alt
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Function to connect to the MySQL database and fetch data
@st.cache(ttl=60)  # Cache the data for 60 seconds
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
            query = "SELECT datetime, ADX, DI_plus, DI_minus FROM adxdis;"
            cursor.execute(query)
            data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=column_names)
            connection.close()
            return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit App
st.title("ADX, DI_minus, and DI_plus Line Chart")

# Function to plot ADX, plusDI, and minusDI using Plotly
def plot_ADX(df):
    # Create the plot using Plotly
    fig = px.line(df, x='datetime', y=['ADX', 'DI_plus', 'DI_minus'],
                  title="ADX, DI_minus, and DI_plus Line Chart",
                  labels={"value": "Value", "variable": "Variable"},
                  template="plotly_white")

    # Set the desired theme
    theme_name = "plotly_dark"  # Change this to your desired theme name

    # Apply the template theme
    fig.update_layout(template=theme_name)
    #
    # # Display the plot using Streamlit
    # st.plotly_chart(fig, use_container_width=True)

    # Get the selected data (if any) from the plot
    selected_data = st.select_slider("Select a data point:", options=fig.data[0]['x'])

    if selected_data:
        # Add vertical line
        fig.add_shape(
            dict(
                type="line",
                x0=selected_data,
                x1=selected_data,
                y0=0,
                y1=1,
                xref="x",
                yref="paper",
                line=dict(color="red", width=2, dash="dash"),
            )
        )

        # Add annotations
        for y_col in ['ADX', 'DI_plus', 'DI_minus']:
            y_val = df.loc[df['datetime'] == selected_data, y_col].iloc[0]
            fig.add_annotation(
                x=selected_data,
                y=y_val,
                xref="x",
                yref="y",
                text=f"{y_col}: {y_val:.2f}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40,
            )

    # Update layout to adjust the height to fit the annotations
    fig.update_layout(
        height=500 + len(fig.layout.annotations) * 30
    )

    # Display the updated plot with vertical line and annotations
    st.plotly_chart(fig, use_container_width=True)



# Fetch data from MySQL
df = fetch_data_from_mysql()



if st.button("Interactive Chart"):

    # Define the line chart using Altair
    chart = alt.Chart(df).mark_line().encode(
        x="datetime:T",
        y=alt.Y("value:Q", axis=alt.Axis(title="Value")),
        color=alt.Color("variable:N", legend=alt.Legend(title="Variable")),
        tooltip=["datetime:T", alt.Tooltip("value:Q", format=".2f")]
    ).transform_fold(
        ["ADX", "DI_minus", "DI_plus"],
        as_=["variable", "value"]
    ).interactive()

    # Display the chart with Streamlit
    st.title("ADX, DI_minus, and DI_plus Line Chart")
    st.altair_chart(chart, use_container_width=True)







if df is not None:
    st.write("Data from MySQL:")
    st.write(df)

    # Display the plot using the function from streamlit_ADX.py
    if 'plot_state' not in st.session_state:
        st.session_state.plot_state = True

    if st.session_state.plot_state:
        st.write("Plotting the chart...")
        st.session_state.plot_state = False

    # Update the plot whenever the data is refreshed
    st.write("Updated Plot:")
    plot_ADX(df)
else:
    st.error("Failed to fetch data from MySQL.")




