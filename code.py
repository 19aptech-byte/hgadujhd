import streamlit as st
from pypdf import PdfReader
import io

st.title("PDF Text Extractor")

st.write("Upload a PDF file to extract and display its text.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        # Read the uploaded PDF
        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        reader = PdfReader(pdf_bytes)

        # Extract text from all pages
        extracted_text = ""

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            extracted_text += f"\n--- Page {page_number} ---\n"
            extracted_text += text + "\n"

        # Display extracted text
        st.subheader("Extracted PDF Text")

        if extracted_text.strip():
            st.text_area(
                "PDF Content",
                value=extracted_text,
                height=400
            )
        else:
            st.warning(
                "No text found. This PDF may contain scanned images."
            )

        # Download extracted text
        st.download_button(
            label="Download Extracted Text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Error reading PDF: {e}")