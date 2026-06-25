#!/bin/bash
# Exit early on errors
set -e

# Start the FastAPI backend in the background on port 8000
echo "Starting Backend on port 8000..."
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to be healthy
echo "Waiting for backend to initialize..."
sleep 3

# Start the Streamlit frontend on port 8501 (or $PORT if defined)
echo "Starting Frontend..."
PORT=${PORT:-7860}
cd frontend && streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false
