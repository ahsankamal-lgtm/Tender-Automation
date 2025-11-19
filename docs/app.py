import streamlit as st
from pathlib import Path
from docx import Document  # to read Word (.docx) files

# ---------- BASIC PAGE SETTINGS (MUST BE FIRST STREAMLIT CALL) ----------
st.set_page_config(
    page_title="Wavetec Tender Library",
    layout="wide"
)

# ---------- SIMPLE & ROBUST LOGIN ----------
def check_password():
    """Returns True if the user entered the correct credentials."""

    # Read auth secrets safely to avoid KeyError
    auth = st.secrets.get("auth", {})
    correct_username = auth.get("username")
    correct_password = auth.get("password")

    # If secrets are missing, show a clear error instead of crashing
    if not correct_username or not correct_password:
        st.error(
            "🔐 Authentication is not configured.\n\n"
            "Please add the following to this app's **Secrets** in Streamlit Cloud:\n\n"
            "[auth]\n"
            'username = "YOUR_USERNAME"\n'
            'password = "YOUR_PASSWORD"'
        )
        return False

    def password_entered():
        """Verify username and password, update session state."""
        entered_username = st.session_state.get("username", "")
        entered_password = st.session_state.get("password", "")

        if entered_username == correct_username and entered_password == correct_password:
            st.session_state["password_correct"] = True
            # Don't keep password in memory
            st.session_state.pop("password", None)
        else:
            st.session_state["password_correct"] = False

    # First run: show login form
    if "password_correct" not in st.session_state:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password", on_change=password_entered)
        return False

    # If wrong credentials were entered
    if not st.session_state["password_correct"]:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password", on_change=password_entered)
        st.error("❌ Incorrect username or password")
        return False

    # Correct credentials
    return True


# ---------- STOP APP IF NOT LOGGED IN ----------
if not check_password():
    st.stop()

# ---------- TITLE & INTRO ----------
st.title("📚 Wavetec Tender Library")
st.write("Central knowledge base for automated tender and RFP responses.")

# ---------- PATHS ----------
BASE_DIR = Path(__file__).parent

# Map of categories to their folder names in the repo
CATEGORY_FOLDERS = {
    "Corporate Profile": BASE_DIR / "Corporate Profile",
    "Technical Profile": BASE_DIR / "Technical Profile",
    "Security Profile": BASE_DIR / "Security Profile",
    "Services And Delivery": BASE_DIR / "Services And Delivery",
}

# ---------- HELPER: READ WORD DOCUMENT ----------
def load_docx_text(file_path: Path) -> str:
    if not file_path.exists():
        return "❗ This document does not exist: " + str(file_path)
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n\n".join(p for p in paragraphs if p.strip())

def list_docx_files(folder: Path):
    if not folder.exists():
        return []
    return sorted([p for p in folder.glob("*.docx")])

# ---------- SIDEBAR: CATEGORY + DOCUMENT SELECTION ----------
st.sidebar.header("📂 Document Library")

category = st.sidebar.selectbox(
    "Select a category:",
    list(CATEGORY_FOLDERS.keys())
)

folder_path = CATEGORY_FOLDERS[category]
doc_files = list_docx_files(folder_path)

if not doc_files:
    st.warning(f"No .docx files found in folder: {folder_path.name}")
else:
    doc_display_names = [f.name for f in doc_files]
    selected_doc_name = st.sidebar.selectbox(
        "Select a document:",
        doc_display_names
    )

    selected_doc_path = folder_path / selected_doc_name

    st.subheader(f"{category} → {selected_doc_name}")
    st.caption(f"Source file: {selected_doc_path.relative_to(BASE_DIR)}")

    content = load_docx_text(selected_doc_path)
    st.markdown(content)
