# Samsung Advisor 🤖📱

An intelligent AI-powered Samsung smartphone advisor that helps users find detailed information about Samsung devices through natural language queries. Built with web scraping, PostgreSQL database, and Google's Gemini AI using RAG (Retrieval-Augmented Generation) architecture.

## 🌟 Features

- **Natural Language Queries**: Ask questions in plain English about Samsung phones
- **Intelligent SQL Generation**: Automatically converts questions to SQL queries using AI
- **Comprehensive Phone Data**: Scrapes detailed specs from GSMArena including:
  - Model information and release dates
  - Display specifications
  - Battery capacity and type
  - Camera megapixels
  - Storage options
  - Pricing in multiple currencies (USD, BDT)
- **RESTful API**: FastAPI-powered endpoints for easy integration
- **Smart Web Scraping**: Retry logic and rate limiting for reliable data collection
- **RAG Architecture**: Combines retrieval and generation for accurate answers

## 🔄 Project Workflow

![Workflow Diagram](/Samsung-Advisor/assets/Samsung Workflow.png)
<!-- Add your workflow diagram image to ./assets/workflow.png -->
## 📹 Project Demo
YT Link: https://youtu.be/xJuQkneAqlc

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Model**: Google Gemini 2.5 Flash
- **Web Scraping**: BeautifulSoup4 + Requests
- **Server**: Uvicorn (ASGI server)
- **Environment Management**: python-dotenv

## 📁 Project Structure

```
Samsung-Advisor/
├── advisor_app/
│   ├── main.py              # FastAPI application entry point
│   ├── routes.py            # API endpoint definitions
│   ├── model.py             # Database schema (SQLAlchemy models)
│   ├── database.py          # Database connection management
│   ├── scraper.py           # Web scraping engine for GSMArena
│   ├── preprocess.py        # Data cleaning and normalization
│   ├── ingest.py            # Data ingestion pipeline (live scraping)
│   ├── insert.py            # Database insertion operations
│   ├── rag.py               # RAG agent (SQL query generation)
│   ├── llm.py               # LLM response generation agent
│   └── preprocess_txt.py    # PDF data processing (easier alternative)
├── check.py                 # Standalone scraper testing script
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Google Gemini API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/ZarinSaima333/Samsung-Advisor.git
cd Samsung-Advisor
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database

```bash
# Log into PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE Samsung_Phones;

# Exit PostgreSQL
\q
```

### Step 5: Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/Samsung_Phones

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here
```

To get a Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

### Step 6: Create Database Tables

Create a file `advisor_app/database.py` with:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Then run:

```python
from advisor_app.model import SamsungDevice
from advisor_app.database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)
```

### Step 7: Scrape and Ingest Data

**Option A: Live Web Scraping (Full Data Collection)**

```bash
# Run the data ingestion script
python advisor_app/ingest.py
```

This will:
- Scrape Samsung phone data from GSMArena in real-time
- Process and normalize the data
- Insert into PostgreSQL database

**Note**: This process may take 15-30 minutes depending on the number of devices.

**Option B: PDF Processing (Easier & Faster Alternative) ⚡**

If you already have scraped data stored in a PDF file:

```bash
# Run the PDF processing script
python advisor_app/preprocess_txt.py
```

This is the **easiest method** as it:
- Reads pre-scraped data from a PDF file
- Processes and normalizes it
- Inserts into the database much faster
- No risk of being blocked by the website

**Recommended**: Use Option B if you have a PDF of scraped data, otherwise use Option A.

### Step 8: Run the Application

```bash
# Start the FastAPI server
uvicorn advisor_app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📖 Usage & Demo

### FastAPI Interactive Documentation

![FastAPI Demo Screenshot](./assets/fastapi-demo.png)
<!-- Add your FastAPI demo screenshot to ./assets/fastapi-demo.png -->

Visit `http://localhost:8000/docs` for Swagger UI interactive documentation where you can test all endpoints directly in your browser.

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "OK",
  "message": "FastAPI is running!"
}
```

#### 2. Test Database Connection
```bash
GET /test-db
```

**Response:**
```json
{
  "status": "DB connected",
  "devices": [
    {
      "model": "Samsung Galaxy S25 Ultra",
      "release_date": "2025-01-22",
      "price_usd": 1299.99
    }
  ]
}
```

#### 3. Ask Questions (Main Feature)
```bash
POST /ask
Content-Type: application/json

{
  "question": "What is the price of Samsung Galaxy A07?"
}
```

**Response:**
```json
{
  "answer": "The Samsung Galaxy A07 is priced at approximately $120 USD (14,640 BDT)."
}
```

### Example Queries

**Price Information:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How much does the Samsung Galaxy S25 cost?"}'
```

**Display Comparison:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Which Samsung Z series phone has the biggest display?"}'
```

**Latest Phone:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the latest Samsung phone?"}'
```

**Battery Comparison:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Which Samsung A series phone has the best battery?"}'
```

## 🧪 Testing the Scraper

Test the web scraper independently:

```bash
python check.py
```

This will scrape and display Samsung phone specifications without storing them in the database.

## 🏗️ How It Works

### RAG Architecture

1. **User Query** → User asks a natural language question
2. **RAG Agent** (`rag.py`) → Converts question to SQL using Gemini AI
3. **Database Query** → Executes SQL to fetch relevant phone data
4. **LLM Agent** (`llm.py`) → Generates human-friendly answer from data
5. **Response** → Returns natural language answer to user

### Data Flow

```
GSMArena → Scraper → Preprocessor → PostgreSQL → RAG → Gemini AI → User
```

## 🔧 Configuration

### Database Schema

The `samsung_devices` table includes:
- `id`: Primary key
- `model`: Phone model name
- `series`: Series category (A, M, S, Z, Other)
- `device_type`: Device type (default: "phone")
- `release_date`: Official release date
- `display_inches`: Screen size in inches
- `battery_mah`: Battery capacity
- `battery_type`: Battery technology
- `camera_main_mp`: Main camera megapixels
- `storage`: Storage options
- `price_value`: Original price value
- `price_currency`: Currency code
- `price_usd`: Price in USD
- `price_bdt`: Price in Bangladeshi Taka
- `source_url`: GSMArena source URL

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Solution: Check your DATABASE_URL in .env file and ensure PostgreSQL is running
```

**2. Gemini API Key Invalid**
```
Solution: Verify your GEMINI_API_KEY in .env file is correct
```

**3. Scraping Blocked (Too Many Requests)**
```
Solution: The scraper includes retry logic. Wait a few minutes and try again, or use the PDF processing method (preprocess_txt.py)
```

**4. No Data in Database**
```
Solution: Run python advisor_app/ingest.py or python advisor_app/preprocess_txt.py to populate the database
```

**5. Module Import Errors**
```
Solution: Ensure you're in the virtual environment and all dependencies are installed
pip install -r requirements.txt
```

## 📊 Example Questions You Can Ask

- "What's the price of Samsung Galaxy A55?"
- "Compare battery life between Galaxy S24 and S25"
- "Which phone has the best camera in the M series?"
- "Show me all phones with 6.7 inch display"
- "What's the latest foldable Samsung phone?"
- "Which is cheaper: Galaxy A15 or Galaxy A25?"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Zarin Saima**
- GitHub: [@ZarinSaima333](https://github.com/ZarinSaima333)

## 🙏 Acknowledgments

- Data source: [GSMArena](https://www.gsmarena.com/)
- AI Model: Google Gemini 2.5 Flash
- Framework: FastAPI

---

**Note**: This project is for educational purposes. Please respect GSMArena's robots.txt and terms of service when scraping.