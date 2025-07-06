# 🚀 KeywordMiner AI

An intelligent SEO keyword analysis and competitor research tool powered by AI. Analyze any website to discover keyword opportunities, search volumes, CPC data, and competitor intelligence.

## ✨ Features

### 🔍 **Keyword Analysis**
- Extract keywords from any website using AI-powered NLP
- Get search volume, CPC, and competition data  
- Categorize keywords by type (short-tail, mid-tail, long-tail, branded)
- Classify by search intent (commercial, informational, navigational)
- Regional targeting and localization

### 🏆 **Intelligent Competitor Analysis**  
- Auto-detect industry and find relevant competitors
- AI companies → OpenAI, Cohere, HuggingFace
- E-commerce → Amazon, Shopify, eBay
- SaaS → Salesforce, HubSpot, Slack
- And more industry-specific competitors

### 📊 **Rich Analytics**
- Interactive keyword distribution charts
- Keyword gap analysis and opportunities
- Traffic estimates and domain authority scores
- Export results to CSV for further analysis

### 🎨 **User-Friendly Interface**
- Clean, responsive design with Tailwind CSS
- Smart URL input (works with or without https://)
- One-click example URLs for testing
- Real-time filtering and search

## 🚀 Live Demo

Try it live: [KeywordMiner AI on Vercel](https://keywordminner-ai.vercel.app)

## 🛠 Technology Stack

- **Frontend**: HTML5, JavaScript (ES6+), Tailwind CSS, Chart.js
- **Backend**: FastAPI (Python), Playwright, NLTK, BeautifulSoup
- **AI/NLP**: Natural Language Processing for keyword extraction
- **Deployment**: Vercel, GitHub

## Features

- 🔍 Website content scraping using Playwright
- 🧠 NLP-based keyword extraction
- 📊 Keyword categorization (short-tail, mid-tail, long-tail, branded)
- 🎯 Intent classification (commercial, informational, navigational)
- 🌍 Regional targeting support
- 📈 Visual keyword distribution charts
- 💾 CSV export functionality

## Installation

1. Clone the repository:
```bash
cd /Users/kayaslam/Desktop/ENV-MindMeta-files/KeywordMiner
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

4. Download NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Serve the frontend (in a new terminal):
```bash
cd frontend
python3 -m http.server 3001
```

3. Open your browser and navigate to:
```
http://localhost:3001
```

## Usage

1. Enter a website URL to analyze
2. Select your target region (or use auto-detect)
3. Optionally provide an email for results
4. Click "Analyze Website"
5. View and filter keyword results
6. Export data as CSV or print report

## Project Structure

```
keywordminer/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── scraper.py       # Web scraping with Playwright
│   └── nlp_engine.py    # Keyword extraction logic
├── frontend/
│   ├── index.html       # Main UI
│   └── app.js          # Frontend JavaScript
├── static/              # Static files and exports
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Future Enhancements

- Integration with real keyword volume APIs
- Advanced competitor analysis
- Multi-language support
- Batch URL processing
- Historical data tracking
- AI-powered content suggestions