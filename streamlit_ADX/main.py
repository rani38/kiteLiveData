import streamlit as st
import pandas as pd
import altair as alt

def plot_ADX(df):

    # Load the data
    # df = pd.read_csv("adxdis.csv")

    # Define the line chart using Altair
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
    return True
