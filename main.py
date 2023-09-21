import engine
import streamlit as st

df = engine.get_data()
print(len(df))
print(df.columns)

engine.delays_depart()
engine.delays_arrive()





