import os
import glob
import io
# from ocr import get_text
from core import converter
from recognizer import audio_to_text
import streamlit as st
from download import set_download

PDF_NAME = "final_output.pdf"

# st.sidebar.image("AI_pirate.png", width=300)
st.sidebar.title("AI Pirates")

st.title("OCR and Audio to Hand Written PDF")

selection = st.sidebar.selectbox("Select Operation:", ["Audio to Handwritten"])  # "OCR to Handwritten"
font = st.sidebar.selectbox("Select Font:", ["default_font", "children_font"])
placeholder = st.sidebar.empty()

# if selection == "OCR to Handwritten":
#     image_list = []
#     uploaded_file = st.file_uploader("Browse an image")
#     if uploaded_file is not None:
#         with st.spinner('Wait for pdf generation ...'):
#             text = get_text(uploaded_file)
#             with open("text.txt", "w") as f:
#                 f.write(text)
#             image_list = converter(font)
#         st.success('Done!')
#
#     if image_list:
#         images = [image.split("\\")[1] for image in glob.glob(os.path.dirname(image_list[0]) + "/*.png")]
#         # selected_image = st.sidebar.selectbox("Select image.", images)
#         if images:
#             st.header("Original Image")
#             st.image(uploaded_file, width=500)
#             st.header("Hand Written PDF")
#             st.image(os.path.dirname(image_list[0]) + "/" + images[0], width=500)
#             set_download(PDF_NAME)
#             placeholder.markdown(f"Download PDF: [{PDF_NAME}](downloads/{PDF_NAME})")
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
        # pages = [f"Page {str(i + 1)}" for i in range(0, len(images))]
        # selected_page = st.sidebar.selectbox("Select page to view.", pages)
        if images:
            # idx = pages.index(selected_page)
            st.header("Text from audio")
            st.write(text)
            st.header("Handwritten PDF result")
            st.image(os.path.dirname(image_list[0]) + "/" + images[0], width=500)
            set_download(PDF_NAME)
            placeholder.markdown(f"Download PDF: [{PDF_NAME}](downloads/{PDF_NAME})")
