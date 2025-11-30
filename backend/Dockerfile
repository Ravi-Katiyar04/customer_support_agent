

# FROM python:3.11-slim

# WORKDIR /app

# # Copy only the requirements first
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Now copy everything from backend folder
# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# OS dependencies
RUN apt-get update && apt-get install -y build-essential git

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install ADK from GitHub
RUN pip install git+https://github.com/openai/adk-python.git

# Copy backend code
COPY . .

# Expose port
EXPOSE 8000

# Run ADK server
CMD ["adk", "serve", "--config", "agent.yml", "--host", "0.0.0.0", "--port", "8000"]
