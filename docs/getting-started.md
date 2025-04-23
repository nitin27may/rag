---
layout: default
title: Getting Started
nav_order: 2
permalink: /getting-started/
---

# Getting Started
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This guide will help you quickly set up and run the Comprehensive RAG System.

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.8+ 
- Node.js and npm (for frontend)
- PostgreSQL database (optional, can use SQLite for development)
- MinIO or S3-compatible object storage (optional)
- Docker and Docker Compose (optional, for containerized deployment)

## Quick Setup

### Option 1: Using Docker (Recommended for Production)

The easiest way to get started is with Docker:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag.git
   cd rag
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file to set your API keys, database connection, etc.

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### Option 2: Manual Setup (Development)

For development or if you prefer not to use Docker:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag.git
   cd rag
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv rag_env
   # On Windows
   rag_env\Scripts\activate
   # On macOS/Linux
   source rag_env/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   python run.py
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   # Create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   npm run dev
   ```

4. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

## Next Steps

- Learn about the [system architecture](../architecture/)
- See the [user guide](../user-guide/) for details on how to use the system
- Check the [troubleshooting](../troubleshooting/) guide if you encounter issues
- Understand [how RAG works](../rag-explained/) in this implementation