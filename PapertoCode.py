import streamlit as st
import pdfplumber
import openai
from PIL import Image

# Set up the title of your Streamlit app
st.title('Paper to Code Implementation')

# Load and display the image
image_path = 'path_to_your_image.png'
image = Image.open(image_path)
st.image(image, caption='Scientific paper code implementation with GenAI', width=600)

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages if page.extract_text() is not None]
    return "\n".join(pages)

# Function to refine content
def refine_content(extracted_text):
    # Placeholder for content refinement logic
    return extracted_text

# Summarize text using the OpenAI API
def summarize_text(refined_text, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Adjusted for the Chat Completions API
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following scientific text:\n\n{refined_text}"},
            ],
            temperature=0.7,
            max_tokens=200
        )
        # Assuming the summary is the 'content' of the last message in the response
        summarized_text = response.choices[0].message['content'].strip()
        return summarized_text
    except Exception as e:
        st.error(f"Error in summarization: {e}")
        return ""

# Function for user to review and edit the summarized text
def user_review_summarization(refined_text, api_key):
    summarized_text = summarize_text(refined_text, api_key)
    return st.text_area("Edit the summary as needed:", value=summarized_text)

# Function to integrate summarized text into Python code
def integrate_into_code(user_summary, existing_code):
    # Placeholder for code integration logic
    return f"{existing_code}\n\n# Integrated Summary:\n{user_summary}"

# Function to display PDF
def display_pdf(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

# Streamlit interface with enhanced UI/UX
def main():
    st.title("Paper to Code")
    st.markdown("Upload a scientific paper and convert its key concepts into Python code.")

    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    if api_key:
        uploaded_file = st.file_uploader("Upload Paper (PDF)", type=["pdf"])

        if uploaded_file is not None:
            col1, col2 = st.columns(2)

            with col1:
                st.header("Uploaded Paper")
                pdf_file_path = display_pdf(uploaded_file)
                st.markdown(f'<iframe src="file://{pdf_file_path}" width="100%" height="400"></iframe>', unsafe_allow_html=True)

            with col2:
                st.header("Generated Code")
                extracted_text = extract_text_from_pdf(uploaded_file)
                refined_text = refine_content(extracted_text)
                user_editable_summary = user_review_summarization(refined_text, api_key)
                existing_code = "# Existing Python code"
                integrated_code = integrate_into_code(user_editable_summary, existing_code)
                st.code(integrated_code, language='python')
                st.download_button("Download Generated Code", integrated_code, file_name="generated_code.py")

if __name__ == "__main__":
    main()
