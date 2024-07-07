import streamlit as st
import os
from io import StringIO
import pdfplumber
from docx import Document
from pptx import Presentation
import tempfile
import base64

def read_pdf(file):
    content = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content += page.extract_text()
    return content

def read_docx(file):
    doc = Document(file)
    content = "\n".join([para.text for para in doc.paragraphs])
    return content

def read_txt(file):
    return file.read().decode('utf-8')

def read_pptx(file):
    prs = Presentation(file)
    content = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                content.append(shape.text)
    return "\n".join(content)

def save_concatenated_file(content):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(content)
    return temp_file.name

def main():
    st.title("Création base de connaissances pour les GPTs")
    st.write("Par Jérome IAvarone")
    st.write("")
    st.write("")
    st.subheader("Chargez vos fichiers :")

    uploaded_files = st.file_uploader("", type=["pdf", "doc", "docx", "txt", "ppt", "pptx"], accept_multiple_files=True)
    
    if st.button("Créer sa base de connaissances"):
        if not uploaded_files:
            st.warning("Chargez au moins 2 fichiers.")
        else:
            all_content = ""
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                file_extension = os.path.splitext(file_name)[1].lower()
                if file_extension == ".pdf":
                    file_content = read_pdf(uploaded_file)
                elif file_extension in [".doc", ".docx"]:
                    file_content = read_docx(uploaded_file)
                elif file_extension == ".txt":
                    file_content = read_txt(uploaded_file)
                elif file_extension in [".ppt", ".pptx"]:
                    file_content = read_pptx(uploaded_file)
                else:
                    file_content = ""
                
                all_content += f"--------------------------- BEGIN {file_name} ---------------------------\n"
                all_content += file_content
                all_content += f"\n--------------------------- END {file_name} ---------------------------\n\n"

            concatenated_file_path = save_concatenated_file(all_content)
            st.success("Traitement réalisé avec succès :)")

            with open(concatenated_file_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="concatenated_file.txt">Télécharger vos fichiers concaténés</a>'
                st.markdown(href, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("© 2024 Jérome Iavarone - jerome.iavarone@gmail.com")

if __name__ == "__main__":
    main()
