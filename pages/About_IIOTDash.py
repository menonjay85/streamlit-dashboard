import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
from data import retrieve
import streamviz
import datetime

st.set_page_config(
    page_title= "Dashboard",
    page_icon= "🤣"
)

st.markdown("# Check it out")
st.sidebar.header("Yello")
st.divider()

# Initial Filter
col1, col2, col3 = st.columns(3)
id = col1.selectbox("Select Machine", ('100', '200'))
today = datetime.datetime.now()
start = datetime.date(today.year, 1, 25)
end = datetime.date(today.year, 12, 31)

d1 = col2.date_input(
    "Select your start filter date", format="MM.DD.YYYY",
)

d2 = col3.date_input(
    "Select your end filter date", format="MM.DD.YYYY",
)
st.divider()

# Creation of single element container
placeholder = st.empty()

totalDF = pd.DataFrame()

# Connect to the DB
# conn, cur = retrieve.connectDB()
update_key = 0

while True:
    df = retrieve.getSensorDataOne()
    # Ensures data is appended and stored locally
    totalDF = pd.concat((df, totalDF), ignore_index=True)

    tempList = df['temperature'].tolist()
    pressList = df['pressure'].tolist()
    humList = df['humidity'].tolist()
    statusList= df['status'].tolist()


    with placeholder.container():
        # create four columns
        kp1, kp2, kp3, kp4 = st.columns(4)

        avgTemp = np.mean(totalDF['temperature'])
        avgPress = np.mean(totalDF['pressure'])
        avgHum = np.mean(totalDF['humidity'])



        kp1.metric(
            label="Temperature 🌡️",
            value= tempList[0],
            delta= round((tempList[0] - avgTemp), 2)
        )
        kp2.metric(
            label="Pressure 💨",
            value= pressList[0],
            delta= round((pressList[0] - avgPress), 2)
        )
        kp3.metric(
            label="Humidity 💧",
            value= humList[0],
            delta= round((humList[0] - avgHum), 2)
        )
        kp4.metric(
            label="Status 💡",
            value= statusList[0]
        )

        # Create 3 columns for charts

        fig_col1, fig_col2, fig_col3 = st.columns(3)
        with fig_col1:
            st.markdown("#### Temperature")
            fig = st.line_chart(data=totalDF, x=None, y="temperature")
        
        with fig_col2:
            st.markdown("#### Pressure")
            fig = st.line_chart(data=totalDF, x=None, y="pressure")
                                
        with fig_col3:
            st.markdown("#### Temp Gauge")
            # fig = streamviz.gauge(gVal=tempList[0], sFix='F', gSize='MED', gcHigh='#032CAC', gcLow="#6583BF", gcMid="#054BA6", grLow=10, grMid=30)
            streamviz.gauge(
                gVal=tempList[0], gSize="SML", sFix='F',
                gTitle="Plotly Stream Gauge", gMode="gauge+number",
                grLow=10, grMid=30, gcLow="#6583BF", 
                gcMid='#032CAC', gcHigh='#032CAC', arTop=100
            )
        
        st.markdown("### Detailed Data View")
        st.dataframe(totalDF)
        time.sleep(3)