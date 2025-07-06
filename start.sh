#!/bin/bash

echo "Starting KeywordMiner AI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip install -r requirements.txt

# Install playwright browsers if needed
echo "Setting up Playwright..."
playwright install chromium

# Download NLTK data
echo "Setting up NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# Start backend in background
echo "Starting backend server on http://localhost:8000..."
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Give backend time to start
sleep 3

# Start frontend
echo "Starting frontend server on http://localhost:3001..."
cd ../frontend && python3 -m http.server 3001 &
FRONTEND_PID=$!

echo ""
echo "KeywordMiner AI is running!"
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait