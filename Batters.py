import streamlit as st
import pandas as pd

data = pd.read_csv("Data\\Batters.csv")
st.subheader(f"Batters ({len(data)} Entries):")
st.write(data)