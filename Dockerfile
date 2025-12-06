# Stage 1: Build Vue
FROM node:20-alpine as build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Run FastAPI
FROM python:3.11-slim
WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend
COPY backend/ ./backend

# Copy Built Assets from Stage 1
COPY --from=build-stage /app/frontend/dist /app/frontend/dist

# Cloud Run Requirement: Listen on port 8080
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]