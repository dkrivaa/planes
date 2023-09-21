import engine
import streamlit as st

df = engine.get_data()
print(len(df))

engine.delays_depart()
engine.delays_arrive()





