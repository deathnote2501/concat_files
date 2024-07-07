import streamlit as st
import os
from docx import Document
from PyPDF2 import PdfReader
from pptx import Presentation

def convert_pdf_to_txt(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def convert_docx_to_txt(docx_file):
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def convert_txt_to_txt(txt_file):
    return txt_file.read().decode("utf-8")

def convert_pptx_to_txt(pptx_file):
    prs = Presentation(pptx_file)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text

def concatenate_files(files):
    concatenated_text = ""
    for file in files:
        if file.type == "application/pdf":
            concatenated_text += convert_pdf_to_txt(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            concatenated_text += convert_docx_to_txt(file)
        elif file.type == "text/plain":
            concatenated_text += convert_txt_to_txt(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            concatenated_text += convert_pptx_to_txt(file)
        else:
            st.error(f"Unsupported file type: {file.type}")
    return concatenated_text

st.title("File Concatenation Tool")

uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, type=['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx'])

if st.button("Concatenate"):
    if uploaded_files:
        concatenated_text = concatenate_files(uploaded_files)
        st.subheader("Concatenated Text")
        st.text(concatenated_text)

        with open("concatenated_output.txt", "w") as f:
            f.write(concatenated_text)
        
        st.success("Files have been concatenated and saved to concatenated_output.txt")
    else:
        st.error("Please upload at least one file")
