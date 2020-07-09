import pathlib
from shutil import copy2
import pandas as pd
import streamlit as st


def set_download(file_name="final_output.pdf"):
    # st.markdown("Download from [downloads/final_output.pdf](downloads/final_output.pdf)")
    # HACK This only works when we've installed streamlit with pipenv, so the
    # permissions during install are the same as the running process
    file_to_download = pathlib.Path.cwd() / f"{file_name}"
    STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'static'
    # We create a downloads directory within the streamlit static asset directory
    # and we write output files to it
    DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")
    if not DOWNLOADS_PATH.is_dir():
        DOWNLOADS_PATH.mkdir()

    copy2(file_to_download, DOWNLOADS_PATH)


if __name__ == "__main__":
    set_download()
