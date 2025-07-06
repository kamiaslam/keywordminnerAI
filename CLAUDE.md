# Project: KeywordMiner

## Overview
This project is located at `/Users/kayaslam/Desktop/ENV-MindMeta-files/KeywordMiner`.
# 📘 Product Requirements Document (PRD)

**Product Name:** KeywordMiner AI  
**Prepared For:** Internal Dev Team / Claude Code  
**Prepared By:** AI Agent & Web Automation Architect  
**Last Updated:** July 6, 2025  

---

## 🧭 1. Overview

**Objective:**  
Build a local AI web application to analyze SEO keyword opportunities from any website. The tool will extract all visible and meta content, detect keywords, get real-time search volume & CPC, and recommend SEO strategies to increase organic traffic globally or regionally.

This document includes a complete setup for local proof-of-concept (POC) using only free tools and APIs.

---

## 🌐 2. Features Summary

### 2.1 Landing Page
- Simple responsive UI with Tailwind or Bootstrap.
- Fields:
  - 🔗 URL Input
  - 🌍 Region Selector (auto + manual)
  - 📨 Optional: Email for results (optional)

### 2.2 Scraping Engine (MCP Web Agent)
- **Tech Used:** Puppeteer (Node.js) or Playwright (Python)
- **MCP Agent Name:** `KeywordScraperAgent`
- Extract:
  - `<title>`, `<meta>`, `<h1>`–`<h6>`, `<p>`, `<a>`, `alt tags`
- Clean HTML → NLP tokenization → N-gram keyword generation (1-3 grams)

### 2.3 Keyword Discovery Engine
- Context-aware keyword expansion
- Use `nltk`, `spaCy`, or OpenAI GPT for keyword suggestion
- Grouped by:
  - Short-tail
  - Long-tail
  - Mid-tail
- Tags: Informational, Commercial, Navigational

### 2.4 Keyword Metrics Integration
- **Free APIs for POC**:
  - `KeywordTool.io` free tier (scrapes autocomplete)
  - `Ubersuggest` browser scraping via Playwright
  - `Keyword Surfer` extension via simulated headless scraping
- Metrics Fetched:
  - Monthly Volume
  - CPC
  - SEO/Paid Competition
  - Global vs Local stats (country, city)

### 2.5 Report Generation
- Table output (HTML + CSV/PDF export)
- Filters:
  - 🔎 High-volume / low-competition
  - 💰 High CPC
  - 🟢 Region-specific
- Export via `jsPDF`, `html2canvas`, or `Pandas to CSV`

### 2.6 Visualizations
- Use:
  - Chart.js (volume/CPC scatter)
  - Keyword cloud (D3.js)
  - Keyword ranking bar chart

---

## 🌍 3. Regional & International SEO Data

### 3.1 GeoIP Detection
- Free IP geolocation via:
  - `ipapi.co/json`
  - `ipinfo.io` (50k free/month)
- Default region auto-detected; user may override

### 3.2 Multilingual Keyword Expansion
- Use Google Translate API (or `deep-translator` Python lib)
- Show:
  - Source keywords
  - Regional language synonyms and intent tags

### 3.3 Regional Metrics Tagging
- Examples:
  - 🔥 “Trending in UAE”
  - 📈 “High CPC in Australia”
  - 🌍 “Emerging Global Opportunity”

---

## 🧠 4. Backend Architecture (Local POC)

- **Frontend**: React.js or basic HTML + JS
- **Backend**: FastAPI (Python) or Express.js (Node.js)
- **Scraper**: Puppeteer (Node.js) or Playwright (Python)
- **NLP Tools**: spaCy / NLTK / GPT-3.5-turbo (OpenAI Free Tier)
- **Database**: SQLite or JSON for local storage
- **Job Queue**: Local threadpool / Celery (optional)

---

## 🛠 5. Local Installation Instructions

### 5.1 Prerequisites
Install the following tools:

```bash
# Backend
pip install fastapi uvicorn beautifulsoup4 playwright nltk spacy

# Frontend
npm install react tailwindcss chart.js

# Puppeteer or Playwright Setup
pip install playwright
playwright install

# Optional NLP Model
python -m spacy download en_core_web_sm

## Development Commands
<!-- Add your common development commands here -->
# Run backend
uvicorn backend.main:app --reload

# Serve frontend (simple way)
cd frontend && python3 -m http.server 3001

## Project Structure
<!-- Add important directories and files here -->
keywordminer/
├── backend/
│   ├── main.py (FastAPI app)
│   ├── scraper.py (Playwright scraping logic)
│   └── nlp_engine.py (Keyword parsing)
├── frontend/
│   ├── index.html or React app
│   └── keyword_results.js
├── static/
│   └── results.csv / report.pdf
├── .env (API keys if needed)
└── README.md

## Notes
<!-- Add any important notes or context for future development -->