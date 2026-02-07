import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="InsightForge – Smarter Answers from Your Files",
    layout="wide",
)

# -------------------------------
# LOAD ENV & CONFIGURE GEMINI
# -------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# -------------------------------
# SIDEBAR CONTENT
# -------------------------------
with st.sidebar:
    st.title("📘 InsightForge")
    st.markdown(
        """
**Smarter Answers from Your Files**

InsightForge uses advanced AI models to read and understand uploaded documents.
Once a PDF is uploaded, the system extracts and processes the content securely.
Users can then ask questions in plain English, and InsightForge generates accurate
answers strictly based on the document’s information.
"""
    )

    st.markdown("---")

    st.subheader("🎯 Who is this for?")
    st.markdown(
        """
📚 **Students** – Understand textbooks, notes, and research papers  

🧪 **Researchers** – Extract insights without re-reading entire papers  

🧾 **Professionals** – Analyze reports, policies, and documentation  

🧑‍💻 **Recruiters** – Review resumes and profiles faster  
"""
    )

    st.markdown("---")
    st.caption("Powered by Gemini AI")

# -------------------------------
# MAIN UI
# -------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title {
        font-size: 18px;
        color: #cccccc;
        margin-bottom: 30px;
    }
    .answer-box {
        background-color: #111827;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1f2937;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">InsightForge</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Ask questions. Get precise answers. No manual searching.</div>',
    unsafe_allow_html=True,
)

# -------------------------------
# PDF UPLOAD
# -------------------------------
uploaded_file = st.file_uploader(
    "📤 Upload a PDF document",
    type=["pdf"],
    help="Upload research papers, reports, resumes, or notes",
)

document_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            document_text += text + "\n"

    if not document_text.strip():
        st.error("❌ Could not extract text from this PDF.")
        st.stop()

    st.success("✅ Document processed successfully.")

# -------------------------------
# QUESTION INPUT
# -------------------------------
question = st.text_input(
    "❓ Ask a question based on the uploaded document",
    placeholder="Example: Summarize the key findings of this document",
)

# -------------------------------
# ANALYZE BUTTON
# -------------------------------
if st.button("▶️ Analyze Document"):
    if not uploaded_file:
        st.warning("Please upload a PDF first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing document..."):
            prompt = f"""
You are an AI document analysis assistant.

RULES:
- Answer ONLY using the information from the document below.
- If the answer is not present, say: "The document does not contain this information."
- Be clear, concise, and accurate.

DOCUMENT:
{document_text}

QUESTION:
{question}
"""

            response = model.generate_content(prompt)

        st.markdown("### 📄 AI Response")
        st.markdown(
            f'<div class="answer-box">{response.text}</div>',
            unsafe_allow_html=True,
        )

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("© 2026 InsightForge | Built by Tharshini DJ")
