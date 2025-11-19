import streamlit as st
from pathlib import Path
from docx import Document  # to read Word (.docx) files

# ---------- BASIC PAGE SETTINGS ----------
st.set_page_config(
    page_title="Wavetec Tender Library",
    layout="wide"
)

st.title("📚 Wavetec Tender Library")
st.write("Central knowledge base for automated tender and RFP responses.")

# ---------- PATHS ----------
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"

# Map of categories to Word filenames
DOCUMENTS = {
    "Corporate Profile": "Corporate_Profile.docx",
    "Technical Profile": "Technical_Profile.docx",
    "Security Profile": "Security_Profile.docx",
    "Hardware Specifications": "Hardware_Specs.docx",
    "Software Specifications": "Software_Specs.docx",
    "Case Studies": "Case_Studies.docx",
}

# ---------- HELPER: READ WORD DOCUMENT ----------
def load_docx_text(file_path: Path) -> str:
    if not file_path.exists():
        return "❗ This document has not been added yet."
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs]
    # Join paragraphs with blank lines so it's readable
    return "\n\n".join(p for p in paragraphs if p.strip())

# ---------- SIDEBAR ----------
st.sidebar.header("📂 Document Categories")
selected_category = st.sidebar.radio(
    "Select a document to view:",
    list(DOCUMENTS.keys())
)

# ---------- MAIN CONTENT ----------
file_name = DOCUMENTS[selected_category]
file_path = DOCS_DIR / file_name

st.subheader(selected_category)
st.caption(f"Source file: docs/{file_name}")

content = load_docx_text(file_path)
st.markdown(content)
