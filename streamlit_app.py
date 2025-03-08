import streamlit as st
import requests
import json
import os
from pathlib import Path
import tempfile
from dotenv import load_dotenv
import pandas as pd
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Mistral OCR Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to get or create session state
def init_session_state():
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.environ.get("MISTRAL_API_KEY", "")
    if "ocr_result" not in st.session_state:
        st.session_state.ocr_result = None
    if "raw_ocr" not in st.session_state:
        st.session_state.raw_ocr = None
    if "file_name" not in st.session_state:
        st.session_state.file_name = ""
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "error" not in st.session_state:
        st.session_state.error = None
    if "need_rerun" not in st.session_state:
        st.session_state.need_rerun = False

# Initialize session state
init_session_state()

def process_document(file, api_key):
    """Process a document file with the API"""
    API_ENDPOINT = "http://localhost:8000/api/structured-ocr"
    
    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key
    
    try:
        files = {
            "file": (file.name, file, "application/octet-stream")
        }
        
        response = requests.post(
            API_ENDPOINT, 
            headers=headers,
            files=files,
            timeout=120  # Increased timeout for large documents
        )
        
        if response.status_code == 200:
            result = response.json()
            # Log the raw response for debugging
            logger.info(f"API Response Keys: {list(result.keys())}")
            if "raw_markdown" in result:
                logger.info(f"Raw markdown found, length: {len(result['raw_markdown'])}")
                logger.info(f"Raw markdown snippet: {result['raw_markdown'][:100]}...")
                st.session_state.raw_ocr = result["raw_markdown"]
            else:
                logger.warning("No raw_markdown field found in API response")
                st.session_state.raw_ocr = None
            return result
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
    except Exception as e:
        logger.exception("Failed to process document")
        raise Exception(f"Failed to process document: {str(e)}")

def convert_to_displayable(value):
    """Convert values to formats that can be displayed in Streamlit tables"""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return value

def display_json_as_table(json_data):
    """Convert JSON to a more readable table format"""
    # Handle nested dictionaries in ocr_contents
    if "ocr_contents" in json_data:
        ocr_contents = json_data["ocr_contents"]
        
        # Create a DataFrame for flat key-values
        flat_items = {}
        nested_items = {}
        
        for key, value in ocr_contents.items():
            if isinstance(value, dict):
                nested_items[key] = value
            else:
                flat_items[key] = convert_to_displayable(value)
        
        if flat_items:
            st.subheader("Document Content")
            df = pd.DataFrame(list(flat_items.items()), columns=["Field", "Value"])
            st.table(df)
        
        # Display nested dictionaries
        for section, content in nested_items.items():
            st.subheader(f"{section.replace('_', ' ').title()}")
            content_display = {k: convert_to_displayable(v) for k, v in content.items()}
            df = pd.DataFrame(list(content_display.items()), columns=["Field", "Value"])
            st.table(df)
    
    # Display general metadata
    metadata = {
        "File Name": json_data.get("file_name", ""),
        "Topics": ", ".join(str(topic) for topic in json_data.get("topics", [])),
        "Languages": ", ".join(str(lang) for lang in json_data.get("languages", [])),
    }
    
    st.subheader("Document Metadata")
    metadata_df = pd.DataFrame(list(metadata.items()), columns=["Field", "Value"])
    st.table(metadata_df)

def create_download_json(data):
    """Create a download link for JSON data"""
    json_str = json.dumps(data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{st.session_state.file_name}_ocr_result.json">Download JSON Result</a>'
    return href

def create_download_text(text, filename):
    """Create a download link for text data"""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download Raw OCR Text</a>'
    return href

# Check if we need to rerun the app (after processing is complete)
if st.session_state.need_rerun:
    st.session_state.need_rerun = False
    st.rerun()

# Sidebar for configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Mistral API Key", 
        value=st.session_state.api_key,
        type="password",
        help="Enter your Mistral API key. If not provided, will use the key from environment variables."
    )
    st.session_state.api_key = api_key
    
    st.markdown("---")
    st.markdown("""
    ### About
    This app uses Mistral's OCR to extract structured information from documents.
    
    Supported file formats:
    - PDF
    - JPG/JPEG
    - PNG
    """)

# Main content
st.title("📄 Mistral OCR Document Extractor")
st.markdown("""
Upload a document to extract structured information using Mistral's powerful OCR and AI capabilities.
""")

# File uploader
uploaded_file = st.file_uploader(
    "Upload a document", 
    type=["pdf", "jpg", "jpeg", "png"],
    help="Select a document file to process"
)

if uploaded_file is not None:
    # Display document preview
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Document Preview")
        if file_extension in [".jpg", ".jpeg", ".png"]:
            st.image(uploaded_file, use_column_width=True)
        elif file_extension == ".pdf":
            st.markdown(f"PDF: {uploaded_file.name}")
            # Can't display PDF preview directly in Streamlit

    with col2:
        st.subheader("Process Document")
        process_button = st.button("Extract Information", use_container_width=True, type="primary")
        
        if process_button:
            if st.session_state.processing:
                st.warning("Processing already in progress...")
            else:
                st.session_state.processing = True
                st.session_state.file_name = uploaded_file.name
                
                with st.spinner("Processing document... (This may take 30-60 seconds)"):
                    try:
                        result = process_document(uploaded_file, st.session_state.api_key)
                        st.session_state.ocr_result = result
                        st.session_state.error = None
                    except Exception as e:
                        st.session_state.error = str(e)
                        st.session_state.ocr_result = None
                    finally:
                        st.session_state.processing = False
                        st.session_state.need_rerun = True
                        st.rerun()

# Display results or error
if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.ocr_result:
    st.markdown("---")
    st.header("Extracted Information")
    
    tab1, tab2 = st.tabs(["Structured Data", "Raw OCR"])
    
    with tab1:
        try:
            # Display JSON data as tables
            display_json_as_table(st.session_state.ocr_result)
            
            # Download structured data
            st.markdown(create_download_json(st.session_state.ocr_result), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying structured results: {str(e)}")
            st.json(st.session_state.ocr_result)  # Fallback to raw JSON display
    
    with tab2:
        st.markdown("### Raw OCR Text")
        
        if "raw_markdown" in st.session_state.ocr_result and st.session_state.ocr_result["raw_markdown"]:
            raw_text = st.session_state.ocr_result["raw_markdown"]
            st.text_area("", value=raw_text, height=400, disabled=True, key="raw_ocr_text")
            
            # Add download button for raw text
            st.markdown(create_download_text(raw_text, f"{st.session_state.file_name}_raw_ocr.txt"), 
                        unsafe_allow_html=True)
        else:
            st.error("Raw OCR text is not available.")
            st.write("This might happen for several reasons:")
            st.write("1. The API didn't return the raw OCR text")
            st.write("2. There was an error during OCR processing")
            st.write("3. The document doesn't contain any text that can be extracted")
            
            # Show debugging information
            st.subheader("Debugging Information:")
            st.write("API Response keys:", list(st.session_state.ocr_result.keys()))
            if "raw_markdown" in st.session_state.ocr_result:
                st.write("Raw Markdown value is empty or None")
            else:
                st.write("Raw Markdown key is missing from the response")
            
            # Check if raw OCR was stored separately
            if st.session_state.raw_ocr:
                st.success("Raw OCR text was found in session state (cached)")
                st.text_area("", value=st.session_state.raw_ocr, height=400, 
                            disabled=True, key="cached_raw_ocr_text")
