# Astrological Calculations API

A Python-based API service for performing astrological calculations using FastAPI and ephem.

## Requirements

- Python 3.11 (required for compatibility with dependencies)
- pip (Python package manager)

## Setup

1. Install Python 3.11 if not already installed:
```bash
# On macOS with Homebrew:
brew install python@3.11
```

2. Create a virtual environment (recommended):
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

To start the server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## Available Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- Ephem: Astronomical calculations
- Pydantic: Data validation 
