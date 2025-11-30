

# FROM python:3.11-slim

# WORKDIR /app

# # Copy only the requirements first
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Now copy everything from backend folder
# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# Base image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install OS dependencies including git for ADK install
RUN apt-get update && apt-get install -y build-essential git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenAI ADK from GitHub
RUN pip install git+https://github.com/openai/adk-python.git

# Copy backend files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Add CORS middleware to main.py (if not already)
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Run ADK server
CMD ["adk", "serve", "--config", "agent.yml", "--host", "0.0.0.0", "--port", "8000"]
