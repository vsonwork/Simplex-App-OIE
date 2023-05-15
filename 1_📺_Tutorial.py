import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
	page_title = "Simplex App",
	page_icon = "1️⃣",
	layout="wide"
)



_, col_video, _ = st.columns([1, 8, 1], gap="large")
video_file = open("powerBI.mp4", 'rb')
video_bytes = video_file.read()
col_video.title("Tutorial")
col_video.video(video_bytes)

col_video.markdown("### Video credit:")
col_video.markdown("Creator&ensp;: User __Son Nguyen__ from __ONCE IS ENOUGH__.")
col_video.write("YouTube: [Simplex Method App | ONCE IS ENOUGH](https://www.youtube.com/watch?v=xHewnG5eiKE)")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
