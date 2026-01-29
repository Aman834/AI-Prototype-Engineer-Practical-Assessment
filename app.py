import streamlit as st
import tempfile
import os

from pdf_loader import load_and_split_pdf
from rag import create_rag_pipeline


# ----------------------------------
# Streamlit Page Config
# ----------------------------------
st.set_page_config(
    page_title="Chat with PDF",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Chat with PDF (RAG AI)")
st.write(
    "Upload a PDF and ask questions. "
    "The AI answers **only from the document context**."
)

# ----------------------------------
# PDF Input (Upload or Default)
# ----------------------------------
DEFAULT_PDF_PATH = "data/sample.pdf"
file_path = None

uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type="pdf"
)

# ---- Case 1: User uploads PDF ----
if uploaded_file:
    # 🔒 SAFETY CHECK: Empty file
    if uploaded_file.size == 0:
        st.error("❌ Uploaded PDF is empty. Please upload a valid PDF file.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    st.success("✅ PDF uploaded successfully!")

# ---- Case 2: Use default sample PDF ----
elif os.path.exists(DEFAULT_PDF_PATH):
    # 🔒 SAFETY CHECK: Empty default file
    if os.path.getsize(DEFAULT_PDF_PATH) == 0:
        st.error("❌ Default sample.pdf is empty. Please replace it with a valid PDF.")
        st.stop()

    file_path = DEFAULT_PDF_PATH
    st.info("ℹ️ Using default PDF from data/sample.pdf")

else:
    st.warning("📂 Please upload a PDF to continue.")

# ----------------------------------
# Build RAG Pipeline
# ----------------------------------
if file_path:
    with st.spinner("📖 Reading and processing PDF..."):
        try:
            chunks = load_and_split_pdf(file_path)
        except Exception as e:
            st.error(f"❌ Failed to read PDF: {e}")
            st.stop()

    if len(chunks) == 0:
        st.error("❌ No readable text found in the PDF.")
        st.stop()

    st.success(f"✅ PDF processed into {len(chunks)} text chunks")

    with st.spinner("🧠 Building AI retrieval system..."):
        qa_chain = create_rag_pipeline(chunks)

    st.divider()

    # ----------------------------------
    # User Question Input
    # ----------------------------------
    question = st.text_input(
        "Ask a question from the PDF",
        placeholder="e.g. What is the main contribution of this document?"
    )

    if question:
        with st.spinner("🤖 Thinking..."):
            response = qa_chain(question)

        # ----------------------------------
        # Display Answer
        # ----------------------------------
        st.subheader("✅ Answer")
        st.write(response["result"])

        # ----------------------------------
        # Display Source Context
        # ----------------------------------
        with st.expander("📚 Source Chunks Used"):
            for i, doc in enumerate(response["source_documents"], start=1):
                st.markdown(f"**Source {i}:**")
                st.write(doc.page_content[:400] + "...")
                st.divider()
