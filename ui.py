import os
import glob
import io
from core import converter
from recognizer import audio_to_text
import streamlit as st
from download import set_download

PDF_NAME = "final_output.pdf"

st.sidebar.title("AI Pirates")

st.title("OCR and Audio to Hand Written PDF")

selection = st.sidebar.selectbox("Select Operation:", ["Audio to Handwritten"])
font = st.sidebar.selectbox("Select Font:", ["default_font", "children_font"])
placeholder = st.sidebar.empty()


if selection == "Audio to Handwritten":
    image_list = []
    uploaded_file = st.file_uploader("Upload a wav file", type="wav")
    if uploaded_file is not None:
        with st.spinner('Wait for audio reading ...'):
            file_name = "uploaded.wav"
            with open(file_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            text = audio_to_text(file_name)
            os.remove(file_name)
            submit_button = False
        st.success("Done")

        if text:
            with open("text.txt", "w") as f:
                f.write(text)
            image_list = converter(font)

    if len(image_list):
        images = [image.replace("\\", "/").split("/")[-1] for image in
                  glob.glob(os.path.dirname(image_list[0]) + "/*.png")]
        if images:
            st.header("Text from audio")
            st.write(text)
            st.header("Handwritten PDF result")
            st.image(os.path.dirname(image_list[0]) + "/" + images[0], width=500)
            set_download(PDF_NAME)
            placeholder.markdown(f"Download PDF: [{PDF_NAME}](downloads/{PDF_NAME})")
