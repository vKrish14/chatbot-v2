# Chatbot V2

Production-ready Chatbot with FastAPI Backend and Streamlit Frontend.

## Features
- **Memory Layer**: Session memory with configurable context windows.
- **Prompt Layer**: Automatic prompt improvement using LLM.
- **Inspector**: Real-time tracking of reasoning, metrics, and pipeline latency.

## Setup Instructions

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in your OpenAI API Key.
3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Access Frontend at `http://localhost:8501` and Backend API at `http://localhost:8000/docs`.

## Deployment (Railway)
This repository is structured to be easily deployed on Railway:
1. Create a new project from this repo.
2. Create two services: one for backend (pointing to `Dockerfile.backend`) and one for frontend (pointing to `Dockerfile.frontend`).
3. Set the `API_BASE_URL` environment variable in the frontend service to the public URL of the backend service.
