import json

from time import sleep

import pandas as pd
import streamlit as st
import altair as alt

from common import RESULTS_FILE, INTERVAL_SEC


def get_data():
    """
    Fetches the data from the result JSON.
    """
    data = []
    with open(RESULTS_FILE) as f:
        for line in f:
            data.append(json.loads(line))
    df = pd.DataFrame(data)
    return df


def make_app(slots):
    """
    Creates a Streamlit application. Meant to be refreshed frequently!
    """
    title = slots["title"]
    title.markdown("# PV Simulator")

    column = slots["select"]

    chart = slots["chart"]
    df = get_data()
    ch = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("timestamp:T", axis=alt.Axis(title="Timestamp")),
            y=alt.Y(f"{column}:Q", axis=alt.Axis(title="Power (kW)")),
        )
    )
    chart.altair_chart(ch, use_container_width=True)


def make_slots():
    """
    Builds placeholders in a Steamlit app that are meant to be updated.
    """
    with open("/var/opt/README.md") as f:
        readme = f.read()
    slots = {
        "title": st.empty(),
        "select": st.selectbox(
            "Metric", options=["total_power", "pv", "meter"]
        ),
        "chart": st.empty(),
        "readme": st.markdown(readme),
    }
    return slots


def main():
    """
    Runs the app!
    """
    slots = make_slots()
    while True:
        make_app(slots)
        sleep(INTERVAL_SEC)


main()
