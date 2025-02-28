import streamlit as st
import time
from processor import TextProcessor
from utils import format_percentage, get_match_feedback, create_match_explanation
import PyPDF2
import io

# Page configuration
st.set_page_config(
    page_title="Resume-to-Job Matcher",
    page_icon="📄",
    layout="wide"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    """
    Extract text from uploaded PDF file
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def main():
    st.title("📄 Resume-to-Job Matcher")
    st.markdown("""
    Upload your resume (PDF) and paste a job description to see how well they match!
    The application uses advanced NLP to analyze the similarity between your resume
    and the job requirements.
    """)

    # Initialize text processor
    processor = TextProcessor()

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"],
            help="Please upload your resume in PDF format"
        )

        if uploaded_file:
            st.success("PDF uploaded successfully!")
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = None

    with col2:
        st.subheader("Job Description")
        job_text = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="Copy and paste the job description here..."
        )

    # Process button
    if st.button("Analyze Match"):
        if not resume_text or not job_text:
            st.error("Please provide both resume (PDF) and job description.")
            return

        with st.spinner("Analyzing your match..."):
            try:
                # Process texts
                resume_doc = processor.preprocess_text(resume_text)
                job_doc = processor.preprocess_text(job_text)

                # Get match analysis
                analysis = processor.analyze_match(resume_doc, job_doc)

                # Display results
                st.markdown("### Results")

                # Create three columns for metrics
                score_col, feedback_col = st.columns([1, 2])

                with score_col:
                    st.markdown(
                        f"""
                        <div class="match-score">
                            Match Score: {format_percentage(analysis['similarity_score'])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with feedback_col:
                    st.info(get_match_feedback(analysis['similarity_score']))

                # Display detailed analysis
                st.markdown("### Detailed Analysis")
                st.markdown(
                    f"""
                    <div class="explanation">
                    {create_match_explanation(
                        analysis['matching_terms'],
                        analysis['missing_terms']
                    )}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    main()