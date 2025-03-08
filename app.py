from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from mistralai import Mistral
from mistralai import ImageURLChunk, TextChunk, DocumentURLChunk
from pathlib import Path
import base64
import json
import os
import tempfile
from pydantic import BaseModel
from enum import Enum
import pycountry
from typing import Any, Dict, List, Optional, TypeVar, Type, Union
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Structured OCR API",
    description="An API for extracting structured data from documents using Mistral AI OCR",
    version="1.0.0"
)

# Language enum for structured output
languages = {lang.alpha_2: lang.name for lang in pycountry.languages if hasattr(lang, 'alpha_2')}

class LanguageMeta(Enum.__class__):
    def __new__(metacls, cls, bases, classdict):
        for code, name in languages.items():
            classdict[name.upper().replace(' ', '_')] = name
        return super().__new__(metacls, cls, bases, classdict)

class Language(Enum, metaclass=LanguageMeta):
    pass

class StructuredOCR(BaseModel):
    file_name: str
    topics: list[str]
    languages: list[Language]
    ocr_contents: dict
    raw_markdown: str  # Add this field to include raw OCR text

class HealthResponse(BaseModel):
    status: str
    api: str

T = TypeVar('T', bound=BaseModel)

def get_mistral_client(api_key: Optional[str] = None) -> Mistral:
    """Get Mistral client using provided API key or environment variable"""
    key = api_key or os.environ.get("MISTRAL_API_KEY")
    if not key:
        raise HTTPException(status_code=401, detail="Mistral API key not provided")
    return Mistral(api_key=key)

def process_image_ocr(image_path: str, api_key: Optional[str] = None) -> dict:
    """Process an image with OCR and return the raw OCR result"""
    client = get_mistral_client(api_key)
    
    image_file = Path(image_path)
    encoded_image = base64.b64encode(image_file.read_bytes()).decode()
    base64_data_url = f"data:image/jpeg;base64,{encoded_image}"
    
    # Process image with OCR
    image_response = client.ocr.process(
        document=ImageURLChunk(image_url=base64_data_url), 
        model="mistral-ocr-latest"
    )
    
    return json.loads(image_response.model_dump_json())

def process_pdf_ocr(pdf_path: str, api_key: Optional[str] = None) -> dict:
    """Process a PDF with OCR and return the raw OCR result"""
    client = get_mistral_client(api_key)
    
    pdf_file = Path(pdf_path)
    
    # Upload file for OCR
    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )
    
    # Get signed URL
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    
    # Process PDF with OCR
    pdf_response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url), 
        model="mistral-ocr-latest", 
        include_image_base64=False
    )
    
    return json.loads(pdf_response.model_dump_json())

def structured_ocr(file_path: str, api_key: Optional[str] = None, response_model: Type[T] = StructuredOCR) -> T:
    """Process a file and return structured OCR output"""
    client = get_mistral_client(api_key)
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension in ['.jpg', '.jpeg', '.png']:
        # Image processing
        ocr_result = process_image_ocr(file_path, api_key)
        image_ocr_markdown = ocr_result["pages"][0]["markdown"]
        
        # Encode image again for the chat model
        image_file = Path(file_path)
        encoded_image = base64.b64encode(image_file.read_bytes()).decode()
        base64_data_url = f"data:image/jpeg;base64,{encoded_image}"
        
        # Parse OCR result into structured JSON
        chat_response = client.chat.parse(
            model="pixtral-12b-latest",
            messages=[
                {
                    "role": "user",
                    "content": [
                        ImageURLChunk(image_url=base64_data_url),
                        TextChunk(text=(
                            "This is the image's OCR in markdown:\n"
                            f"<BEGIN_IMAGE_OCR>\n{image_ocr_markdown}\n<END_IMAGE_OCR>.\n"
                            "Convert this into a structured JSON response with the OCR contents in a sensible dictionary."
                        ))
                    ],
                },
            ],
            response_format=response_model,
            temperature=0
        )
        
        parsed_result = chat_response.choices[0].message.parsed
        
        # Add the raw markdown to the result
        parsed_dict = json.loads(parsed_result.model_dump_json())
        parsed_dict["raw_markdown"] = image_ocr_markdown
        
        # Log the raw markdown for debugging
        print(f"Raw markdown length: {len(image_ocr_markdown)}")
        print(f"Raw markdown snippet: {image_ocr_markdown[:100]}...")
        
        # Convert back to response model
        return response_model.model_validate(parsed_dict)
    
    elif file_extension == '.pdf':
        # PDF processing
        ocr_result = process_pdf_ocr(file_path, api_key)
        pdf_ocr_markdown = "\n\n".join([page["markdown"] for page in ocr_result["pages"]])
        
        # Parse OCR result into structured JSON
        chat_response = client.chat.parse(
            model="ministral-8b-latest",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "This is the PDF's OCR in markdown:\n"
                        f"<BEGIN_PDF_OCR>\n{pdf_ocr_markdown}\n<END_PDF_OCR>.\n"
                        "Convert this into a structured JSON response with the OCR contents in a sensible dictionary."
                    )
                },
            ],
            response_format=response_model,
            temperature=0
        )
        
        parsed_result = chat_response.choices[0].message.parsed
        
        # Add the raw markdown to the result
        parsed_dict = json.loads(parsed_result.model_dump_json())
        parsed_dict["raw_markdown"] = pdf_ocr_markdown
        
        # Log the raw markdown for debugging
        print(f"Raw markdown length: {len(pdf_ocr_markdown)}")
        print(f"Raw markdown snippet: {pdf_ocr_markdown[:100]}...")
        
        # Convert back to response model
        return response_model.model_validate(parsed_dict)
    
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

async def save_upload_file(upload_file: UploadFile) -> tuple[str, str]:
    """Save an uploaded file to a temporary location and return the path and temp dir"""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, upload_file.filename)
    
    # Write the file content
    with open(file_path, "wb") as f:
        content = await upload_file.read()
        f.write(content)
    
    # Reset file pointer for potential future reads
    await upload_file.seek(0)
    
    return file_path, temp_dir

def get_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    """Extract API key from headers if provided"""
    return x_api_key

@app.post("/api/structured-ocr", response_model=StructuredOCR, summary="Extract structured data from documents")
async def structured_ocr_endpoint(
    file: UploadFile = File(...),
    api_key: Optional[str] = Depends(get_api_key)
):
    """
    Process a document with OCR and return structured data extracted from the document.
    
    - **file**: The document file (PDF, JPG, JPEG, or PNG)
    - **X-API-Key**: (Optional) Mistral API key in header
    
    Returns structured data extracted from the document using Mistral's OCR and LLM capabilities.
    """
    # Check if file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Save file temporarily
    try:
        file_path, temp_dir = await save_upload_file(file)
        
        # Process file for structured output
        result = structured_ocr(file_path, api_key)
        
        # Verify raw_markdown is included
        result_dict = json.loads(result.model_dump_json())
        if "raw_markdown" not in result_dict or not result_dict["raw_markdown"]:
            print("Warning: raw_markdown is missing or empty in result")
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temporary files
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            os.rmdir(temp_dir)

@app.get("/health", response_model=HealthResponse, summary="Health check endpoint")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api": "Structured OCR Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
