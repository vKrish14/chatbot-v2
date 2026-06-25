FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (curl for healthchecks, etc)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy backend and frontend requirements
COPY backend/requirements.txt ./backend_requirements.txt
COPY frontend/requirements.txt ./frontend_requirements.txt

# Combine and install requirements
RUN pip install --no-cache-dir -r backend_requirements.txt
RUN pip install --no-cache-dir -r frontend_requirements.txt

# Copy all code
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Copy startup script
COPY start.sh ./
RUN chmod +x start.sh

# Expose Streamlit port
EXPOSE 7860

# Command to run the startup script
CMD ["./start.sh"]
