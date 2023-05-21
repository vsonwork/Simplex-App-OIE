import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
	page_title = "Simplex App",
	page_icon = "1️⃣",
	layout="wide"
)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://raw.githubusercontent.com/vsonwork/Simplex-App-OIE/main/img/background_main.jpg?token=GHSAT0AAAAAACBEEOWHVKVZSZE5WPCU7ZVCZDC4CBQ");
background-size: 150%;
background-position: top left;
background-repeat: repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("https://raw.githubusercontent.com/vsonwork/Simplex-App-OIE/main/img/background_sida.webp?token=GHSAT0AAAAAACBEEOWGKNFY6SERGIVWB3W6ZDC4CIA");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

_, col_video, _ = st.columns([1, 8, 1], gap="large")
video_file = open("/video/simplex_video.mp4", 'rb')
video_bytes = video_file.read()
col_video.title("Tutorial")
col_video.video(video_bytes)

col_video.markdown("### Video credit:")
col_video.markdown("Creator&ensp;: User __Son Nguyen__ from __ONCE IS ENOUGH__.")
col_video.write("YouTube: [Simplex Method App | ONCE IS ENOUGH](https://www.youtube.com/watch?v=U6hXUP0tJlw)")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
