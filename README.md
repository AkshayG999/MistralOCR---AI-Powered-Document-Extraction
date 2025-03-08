# 📄 MistralOCR - AI-Powered Document Extraction

![GitHub stars](https://img.shields.io/github/stars/nirmitee/mistralOCR?style=social)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-blue)

<p align="center">
  <img src="https://github.com/AkshayG999/MistralOCR---AI-Powered-Document-Extraction/blob/main/public/UI-imag.png" alt="MistralOCR Banner" width="720">
</p>

> **Transform any document into structured data with Mistral AI's powerful OCR and LLM capabilities**

MistralOCR is an open-source application that extracts structured information from documents using Mistral's cutting-edge AI. It processes images and PDFs to transform unstructured text into clean, structured JSON data that you can actually use.

**Keywords:** OCR, Optical Character Recognition, Document AI, Document Processing, Text Extraction, Structured OCR, Fast OCR, PDF OCR, Image OCR, Intelligent Document Processing (IDP), Invoice OCR, Receipt OCR, Document Parsing, Data Extraction, AI Document Analysis

## ✨ Features

- 🤖 **Powered by Mistral AI** - Utilizes Mistral's state-of-the-art OCR and LLM models
- 🧠 **Smart Data Extraction** - Intelligently structures information based on document context
- 📊 **Clean UI Dashboard** - User-friendly Streamlit interface for easy document processing
- 🔌 **API-First Design** - FastAPI backend for integration with your applications
- 🔑 **Flexible Authentication** - Use your own Mistral API key or configure from environment
- 🏁 **One-Click Setup** - Simple installation and startup process
- 📱 **Multi-Format Support** - Process PDFs, JPGs, PNGs with a unified workflow
- ⚡ **High-Performance OCR** - Fast and accurate text recognition capabilities
- 🔄 **Real-time Processing** - Get structured results in seconds

## 🚀 Quick Demo

<p align="center">
  <img src="https://github.com/AkshayG999/MistralOCR---AI-Powered-Document-Extraction/blob/main/public/Screen%20Recording%202025-03-08%20at%201.04.23%E2%80%AFPM.mov" alt="MistralOCR Demo" width="720">
</p>

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- A Mistral AI API key (get one at [mistral.ai](https://mistral.ai))

### Option 1: Using Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/AkshayG999/MistralOCR---AI-Powered-Document-Extraction.git
cd MistralOCR---AI-Powered-Document-Extraction

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your Mistral API key
# Option 1: Create a .env file
echo "MISTRAL_API_KEY=your_api_key_here" > .env

# Option 2: Set environment variable
# For Windows:
# set MISTRAL_API_KEY=your_api_key_here
# For macOS/Linux:
# export MISTRAL_API_KEY=your_api_key_here

# Start the application
python run_app.py
```

### Option 2: Direct Installation

```bash
# Clone the repository
git clone https://github.com/AkshayG999/MistralOCR---AI-Powered-Document-Extraction.git
cd MistralOCR---AI-Powered-Document-Extraction

# Install dependencies
pip install -r requirements.txt

# Set your Mistral API key (or add it later through the UI)
echo "MISTRAL_API_KEY=your_api_key_here" > .env

# Start the application
python run_app.py
```

After running the application:
1. The FastAPI backend will start on port 8000
2. The Streamlit UI will start on port 8501
3. Your default web browser will automatically open to the Streamlit interface

## 🧩 How It Works

1. **Document Upload** - Upload any image or PDF document through the UI
2. **OCR Processing** - The document is processed using Mistral's advanced OCR
3. **AI Structuring** - OCR output is intelligently parsed into structured data
4. **Results Display** - View the extracted information in a clean, organized format
5. **Download Options** - Export the data as JSON or raw text

## 📋 Use Cases

- **Invoice Processing** - Extract vendor, amounts, line items, dates, and payment terms
- **Receipt Analysis** - Pull purchase details, totals, store information, and discounts
- **ID Document Extraction** - Capture name, date of birth, ID numbers, and other fields
- **Form Digitization** - Convert paper forms into digital data automatically
- **Contract Analysis** - Extract key terms, dates, parties, and clauses
- **Medical Record Digitization** - Structured extraction from medical documents
- **Business Card OCR** - Extract contact details and company information
- **Academic Document Processing** - Process transcripts, certificates, and research papers
- **Financial Document Analysis** - Extract data from bank statements, reports, and prospectuses

## 📊 Example Output

```json
{
  "file_name": "invoice_example",
  "topics": ["Invoice", "Payment", "Order"],
  "languages": ["English"],
  "ocr_contents": {
    "invoice_number": "INV-12345",
    "date": "2024-03-15",
    "due_date": "2024-04-15",
    "vendor": "ABC Supplies Ltd.",
    "customer": {
      "name": "Acme Corporation",
      "address": "123 Business St, Cityville, ST 12345",
      "email": "accounts@acme.com"
    },
    "items": [
      {
        "description": "Premium Widget",
        "quantity": 10,
        "unit_price": 49.99,
        "total": 499.90
      },
      {
        "description": "Deluxe Gadget",
        "quantity": 5,
        "unit_price": 129.99,
        "total": 649.95
      }
    ],
    "subtotal": 1149.85,
    "tax": 114.99,
    "total": 1264.84,
    "payment_terms": "Net 30"
  }
}
```

## 🧪 Technologies Used

- **FastAPI** - High-performance API framework
- **Streamlit** - Interactive UI for document processing
- **Mistral AI** - State-of-the-art OCR and LLM capabilities
- **Pydantic** - Data validation and settings management
- **Docker** - Containerization for easy deployment

## 🌐 API Documentation

Comprehensive API documentation is available at `/docs` when running the application:

```
http://localhost:8000/docs
```

## 🚢 Deployment

### Docker

```bash
# Build the Docker image
docker build -t mistral-ocr .

# Run the container
docker run -p 8000:8000 -p 8501:8501 -e MISTRAL_API_KEY="your_api_key_here" mistral-ocr
```

### Cloud Deployment

The application can be easily deployed to any cloud platform that supports Docker containers.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## ✉️ Contact

Project Link: [https://github.com/AkshayG999/MistralOCR---AI-Powered-Document-Extraction](MistralOCR---AI-Powered-Document-Extraction)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/AkshayG999">Akshay</a>
</p>

<!-- SEO Keywords -->
<!-- 
Document OCR, FastAPI OCR, Streamlit OCR, OCR API, Document Data Extraction, 
PDF Text Extraction, AI OCR, Automated Data Extraction, OCR Processing, 
Invoice OCR Processing, OCR Solution, Neural OCR, Intelligent OCR, 
Document Recognition, Text Recognition, Document Intelligence, Data Capture,
Receipt Scanner, OCR Automation, Document Digitization, Mistral OCR
-->
