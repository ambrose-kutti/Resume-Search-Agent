# 🚀 Resume Search Agent

<div align="center">

<!-- TODO: Add project logo -->

[![GitHub stars](https://img.shields.io/github/stars/ambrose-kutti/Resume-Search-Agent?style=for-the-badge)](https://github.com/ambrose-kutti/Resume-Search-Agent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ambrose-kutti/Resume-Search-Agent?style=for-the-badge)](https://github.com/ambrose-kutti/Resume-Search-Agent/network)
[![GitHub issues](https://img.shields.io/github/issues/ambrose-kutti/Resume-Search-Agent?style=for-the-badge)](https://github.com/ambrose-kutti/Resume-Search-Agent/issues)
[![GitHub license](https://img.shields.io/github/license/ambrose-kutti/Resume-Search-Agent?style=for-the-badge)](LICENSE)

**A production-grade AI Agent for intelligent resume search and talent matching.**

</div>

## 📖 Overview

The Resume Search Agent is a powerful, AI-driven application designed to revolutionize the talent acquisition process. Leveraging large language models (LLMs) and vector database technology (ChromaDB), this agent enables recruiters and hiring managers to semantically search through vast resume datasets, moving beyond traditional keyword matching. It features an intelligent ingestion pipeline for processing resumes and a robust search mechanism that understands context and intent, making it an indispensable tool for efficient and accurate candidate discovery.

## ✨ Features

-   🎯 **AI-powered Semantic Search**: Perform intelligent searches on resumes based on skill, experience, and contextual understanding rather than just keywords.
-   🧠 **Agent-based Query Refinement**: Utilize AI agents to interpret complex search queries and dynamically refine search parameters for more accurate results.
-   📄 **Resume Data Ingestion**: Efficiently parse, embed, and store resume data into a vector database for quick and scalable retrieval.
-   📊 **Vector Database Integration**: Seamlessly integrates with ChromaDB for high-performance similarity search and data management.
-   🚀 **Scalable API Backend**: Built with FastAPI, providing a robust, high-performance API for all agent functionalities.
-   🛠️ **Configurable LLM Integration**: Easily configure and integrate with various LLM providers for embeddings and agent reasoning.
-   🌐 **Separate Frontend**: Designed for flexibility with a decoupled frontend for user interaction.

## 🖥️ Screenshots

<!-- TODO: Add actual screenshots of the application, showing search interface, results, and potentially ingestion status. -->
<!-- ![Screenshot 1](path-to-screenshot-1.png) -->
<!-- ![Screenshot 2](path-to-screenshot-2.png) -->

## 🛠️ Tech Stack

**Backend:**
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LLM (Generic)](https://img.shields.io/badge/LLMs-FF9900?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/docs/guides/embeddings)
[![Requests](https://img.shields.io/badge/Requests-005B96?style=for-the-badge&logo=python&logoColor=white)](https://requests.readthedocs.io/en/latest/)

**Database:**
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0051B8?style=for-the-badge&logo=chroma&logoColor=white)](https://www.trychroma.com/)

**Frontend:**
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

## 🚀 Quick Start

Follow these steps to get your development environment up and running.

### Prerequisites

Before you begin, ensure you have the following installed:

-   **Python** (3.9 or higher recommended)
-   **pip** (Python package installer)
-   **Git**

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/ambrose-kutti/Resume-Search-Agent.git
    cd Resume-Search-Agent
    ```

2.  **Install backend dependencies**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    # TODO: Create a requirements.txt file in the root or api/ directory.
    # For now, install known dependencies manually or create a requirements.txt from config.py analysis.
    pip install fastapi uvicorn "python-dotenv>=1.0.0" chromadb requests langchain openai tiktoken
    ```
    *Note: A `requirements.txt` file is crucial for a production-ready setup. Please create one by running `pip freeze > requirements.txt` after installing all dependencies.*

3.  **Environment setup**
    Create a `.env` file in the root directory for your environment variables.
    ```bash
    cp .env.example .env # If .env.example exists. Otherwise, create manually.
    ```
    Configure your environment variables in the newly created `.env` file:
    ```
    # --- LLM Configuration ---
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY" # Required for OpenAI embeddings and chat models
    # Alternatively, specify a different LLM provider and its API key
    # LLM_PROVIDER="HUGGINGFACE"
    # HUGGINGFACE_API_KEY="YOUR_HUGGINGFACE_API_KEY"

    # --- ChromaDB Configuration ---
    CHROMA_DB_PATH="./chroma_db" # Path where ChromaDB will store its data (local persistent storage)

    # --- Backend API Configuration ---
    FASTAPI_HOST="0.0.0.0"
    FASTAPI_PORT=8000
    ```
    *Adjust the LLM-related variables based on your chosen LLM provider.*

4.  **Database setup**
    ChromaDB will initialize automatically on first use at the specified `CHROMA_DB_PATH`. No manual migration commands are typically needed for local ChromaDB instances.

5.  **Ingest Sample Resumes (Optional but Recommended for Testing)**
    The `generate_resumes.py` script can be used to generate synthetic resumes and ingest them into the system.
    ```bash
    python generate_resumes.py
    ```
    This script might require additional dependencies, please check its internal imports.

6.  **Start the backend development server**
    Navigate to the root of the project and run:
    ```bash
    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    This assumes your main FastAPI application is defined in `api/main.py` and the app instance is named `app`.

7.  **Start the frontend development server**
    The `frontend` directory contains the web UI. Please refer to its specific `README.md` or package manager instructions for setup.
    ```bash
    cd frontend
    # Example for a Node.js-based frontend (e.g., React, Vue, Angular):
    # npm install
    # npm run dev
    # cd .. # Go back to root directory
    ```
    *Note: The specific commands for the frontend will depend on its chosen framework and build tools. Please consult the `frontend/` directory for details.*

8.  **Open your browser**
    Once both backend and frontend are running, visit `http://localhost:[detected_frontend_port]` (e.g., `http://localhost:3000` for React/Next.js) to access the application. The backend API will be available at `http://localhost:8000`.

## 📁 Project Structure

```
Resume-Search-Agent/
├── .gitignore             # Specifies intentionally untracked files to ignore
├── api/                   # FastAPI backend application
│   ├── __init__.py        # Python package initialization
│   ├── main.py            # Main FastAPI application entry point (inferred)
│   ├── routes/            # API endpoints (inferred)
│   ├── services/          # Business logic and AI agent interactions (inferred)
│   └── models/            # Data models (Pydantic models for request/response) (inferred)
├── config.py              # Centralized configuration settings for the backend
├── frontend/              # Web user interface application
│   ├── public/            # Static assets (inferred)
│   ├── src/               # Frontend source code (inferred)
│   └── package.json       # Frontend dependencies and scripts (inferred)
├── generate_resumes.py    # Script for generating or processing sample resume data
├── ingestion/             # Module for resume data parsing, embedding, and storage
│   ├── __init__.py        # Python package initialization
│   ├── resume_parser.py   # Logic for parsing resume files (inferred)
│   ├── embedder.py        # Logic for creating embeddings (inferred)
│   └── pipeline.py        # Orchestrates the ingestion process (inferred)
├── search/                # Module for performing AI-powered resume searches
│   ├── __init__.py        # Python package initialization
│   ├── agent.py           # AI agent for query understanding and refinement (inferred)
│   ├── retriever.py       # Logic for interacting with ChromaDB (inferred)
│   └── orchestrator.py    # Combines agent and retriever for search (inferred)
└── README.md              # Project README file
```

## ⚙️ Configuration

### Environment Variables
The application uses environment variables for sensitive information and configuration. These are loaded from the `.env` file using `python-dotenv`.

| Variable        | Description                                       | Default        | Required |
|-----------------|---------------------------------------------------|----------------|----------|
| `OPENAI_API_KEY`| API key for OpenAI services (embeddings, LLM calls)| -              | Yes      |
| `LLM_PROVIDER`  | (Optional) Specify alternative LLM provider       | `OPENAI`       | No       |
| `HUGGINGFACE_API_KEY`| API key for HuggingFace models (if `LLM_PROVIDER` is `HUGGINGFACE`)| - | No |
| `CHROMA_DB_PATH`| Local path where ChromaDB will persist its data   | `./chroma_db`  | No       |
| `FASTAPI_HOST`  | Host for the FastAPI server                       | `0.0.0.0`      | No       |
| `FASTAPI_PORT`  | Port for the FastAPI server                       | `8000`         | No       |

### Configuration Files
-   `config.py`: This Python file contains application-specific settings, constants, and potentially default values for various components (e.g., LLM model names, embedding dimensions, search parameters). It centralizes non-sensitive application configurations.

## 🔧 Development

### Available Scripts (Backend)

-   `uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload`: Starts the FastAPI development server with auto-reloading.
-   `python generate_resumes.py`: Executes the script to generate and possibly ingest synthetic resume data.

### Development Workflow
1.  Ensure all prerequisites are met and dependencies are installed.
2.  Set up your `.env` file with necessary API keys and paths.
3.  Start the backend API server.
4.  Navigate to the `frontend/` directory and follow its instructions to start the frontend development server.
5.  Make changes to the respective backend or frontend codebases. The backend will hot-reload on changes.

## 🧪 Testing

No explicit testing framework or test files were detected in the top-level directory structure. For a production-grade application, it's highly recommended to implement unit and integration tests for both the backend API and AI agent logic.

**Recommendation:**
-   For Python backend: Use `pytest`.
-   For frontend (if JavaScript-based): Use `Jest` or `React Testing Library`.

## 🚀 Deployment

### Production Build (Backend)
To create a production-ready deployment for the backend, you would typically use a WSGI server like `Gunicorn` in conjunction with `FastAPI`:
```bash
gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Deployment Options
-   **Docker**: It is highly recommended to containerize both the backend and frontend applications using Docker for consistent and reproducible deployments. A `Dockerfile` for the FastAPI application would typically be placed in the root or `api/` directory.
-   **Cloud Platforms**: The backend can be deployed on various cloud platforms like AWS EC2, Google Cloud Run, Azure App Service, or Heroku.
-   **Frontend**: The frontend can be built and served as static files (e.g., on Netlify, Vercel, GitHub Pages, or any static file hosting).

## 📚 API Reference

The backend API is built with FastAPI, providing automatic interactive API documentation using Swagger UI (OpenAPI).

### Accessing API Documentation
Once the backend server is running, you can access the interactive API documentation at:
-   **Swagger UI**: `http://localhost:8000/docs`
-   **Redoc**: `http://localhost:8000/redoc`

### Key Endpoints (Inferred)

#### Resume Ingestion
-   **POST `/ingest-resume`**: Uploads and processes a new resume.
    -   **Parameters**: Expects multipart form data or JSON with resume content.
    -   **Response**: Status of ingestion (success/failure), unique resume ID.

#### Resume Search
-   **POST `/search`**: Initiates an AI-powered semantic search for resumes.
    -   **Parameters**:
        -   `query` (string, required): The natural language query for resume search (e.g., "Find candidates with extensive experience in machine learning and Python").
        -   `limit` (integer, optional): Maximum number of results to return (default: 10).
    -   **Response**: A list of matching resumes with relevance scores and key details.

#### Agent Interactions
-   **POST `/agent/refine-query`**: Uses an AI agent to refine a given search query.
    -   **Parameters**:
        -   `initial_query` (string, required): The original search query.
        -   `context` (string, optional): Additional context or feedback for refinement.
    -   **Response**: A refined query or suggested search parameters.

## 🤝 Contributing

We welcome contributions! If you're interested in improving the Resume Search Agent, please consider the following:

1.  **Fork the repository**.
2.  **Create a new branch** for your feature or bug fix.
3.  **Implement your changes** and write appropriate tests.
4.  **Ensure code quality** and follow existing coding standards.
5.  **Submit a pull request** with a clear description of your changes.

For more detailed information, please see our [Contributing Guide](CONTRIBUTING.md) <!-- TODO: Create CONTRIBUTING.md file -->.

### Development Setup for Contributors
The development setup is described in the [Quick Start](#🚀-quick-start) section. Ensure you have the backend and frontend running independently.

## 📄 License

This project is licensed under the [MIT License](LICENSE) <!-- TODO: Specify actual license if MIT, otherwise update --> - see the `LICENSE` file for details.

## 🙏 Acknowledgments

-   **FastAPI**: For providing an excellent framework for building robust APIs.
-   **ChromaDB**: For enabling efficient vector storage and similarity search.
-   **OpenAI/Other LLM Providers**: For powerful language models that drive the AI agent capabilities.
-   [Author Name] <!-- TODO: Add author name if different from repo owner -->

## 📞 Support & Contact

-   🐛 Issues: [GitHub Issues](https://github.com/ambrose-kutti/Resume-Search-Agent/issues)
-   💬 Discussions: [GitHub Discussions](https://github.com/ambrose-kutti/Resume-Search-Agent/discussions) <!-- TODO: Enable GitHub Discussions if desired -->
-   📧 Email: [ambrose.kutti@example.com] <!-- TODO: Add actual contact email -->

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [ambrose-kutti](https://github.com/ambrose-kutti)

</div>
