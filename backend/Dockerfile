

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

# Avoid Python buffering
ENV PYTHONUNBUFFERED=1

# Install OS dependencies
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ADK
RUN pip install openai-adk

# Copy backend files
COPY . .

# Expose ADK FastAPI runtime port
EXPOSE 8000

# ADK runtime command
CMD ["adk", "serve", "--config", "agent.yml", "--host", "0.0.0.0", "--port", "8000"]


