# 📄 MistralOCR - AI-Powered Document Extraction

![GitHub stars](https://img.shields.io/github/stars/nirmitee/mistralOCR?style=social)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-blue)

<p align="center">
  <img src="https://i.imgur.com/PJYz4vG.png" alt="MistralOCR Banner" width="720">
</p>

> **Transform any document into structured data with Mistral AI's powerful OCR and LLM capabilities**

MistralOCR is an open-source application that extracts structured information from documents using Mistral's cutting-edge AI. It processes images and PDFs to transform unstructured text into clean, structured JSON data that you can actually use.

## ✨ Features

- 🤖 **Powered by Mistral AI** - Utilizes Mistral's state-of-the-art OCR and LLM models
- 🧠 **Smart Data Extraction** - Intelligently structures information based on document context
- 📊 **Clean UI Dashboard** - User-friendly Streamlit interface for easy document processing
- 🔌 **API-First Design** - FastAPI backend for integration with your applications
- 🔑 **Flexible Authentication** - Use your own Mistral API key or configure from environment
- 🏁 **One-Click Setup** - Simple installation and startup process

## 🚀 Quick Demo

<p align="center">
  <img src="https://i.imgur.com/ZdCsY6Y.gif" alt="MistralOCR Demo" width="720">
</p>

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/nirmitee/mistralOCR.git
cd mistralOCR

# Install dependencies
pip install -r requirements.txt

# Set your Mistral API key (or add it later through the UI)
echo "MISTRAL_API_KEY=your_api_key_here" > .env

# Start the application
python run_app.py
```

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

Project Link: [https://github.com/nirmitee/mistralOCR](https://github.com/nirmitee/mistralOCR)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/nirmitee">Akshay</a>
</p>
