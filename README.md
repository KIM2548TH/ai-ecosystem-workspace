# FastAPI AI Ecosystem & React Web Application

An end-to-end modern AI platform combining a high-performance FastAPI backend microservice architecture with a modern React (Vite) frontend web application. The platform provides secure user authentication, object storage integration with MinIO, dataset metadata management with PostgreSQL 17, an append-only machine learning model registry, asynchronous automated training pipelines backed by Redis and ARQ, and structured JSON error logging.

---

## 1. Quick Start & Setup Guide

### Prerequisites
Before running the application, ensure the following software tools are installed on your environment:
- **Python 3.8+** (Python 3.10+ recommended)
- **Node.js 18+** & `npm`
- **Docker & Docker Compose** (for running backing services: PostgreSQL 17, Redis, MinIO, Label Studio)

### Step 1: Environment Setup
Copy the environment template file to create your active `.env` configuration file:
```bash
cp .env.sample .env
```
Review `.env` if you need to adjust database passwords, secret keys, or host ports.

### Step 2: Start Backing Services
Launch PostgreSQL 17, Redis, MinIO Object Storage, and Label Studio in background mode:
```bash
docker-compose up -d
```
Or using the Docker CLI V2 command:
```bash
docker compose up -d
```

### Step 3: Run FastAPI Backend Server
Execute the launcher script `run.sh`, which automatically detects virtual environments and starts the Uvicorn server:
```bash
./run.sh
```
To run the FastAPI backend server on a custom port (for example, port `8000`):
```bash
PORT=8000 ./run.sh
```

### Step 4: Run React Frontend Application
In a separate terminal, navigate to the `frontend` directory, install all Node dependencies, and start the Vite development server:
```bash
cd frontend
npm install
npm run dev
```

### System Access Endpoints & Web Interfaces

| Application / Service | Endpoint URL | Description & Credentials |
| :--- | :--- | :--- |
| **React Frontend UI** | [http://localhost:5173](http://localhost:5173) | User Registration, OAuth Login, and Protected Token Dashboard |
| **FastAPI Swagger OpenAPI Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive API Exploration and Endpoint Testing |
| **MinIO Console Interface** | [http://localhost:9001](http://localhost:9001) | User: `minioadmin` \| Password: `minioadmin` |
| **Label Studio Platform** | [http://localhost:8080](http://localhost:8080) | Data Annotation and Labeling Platform |

---

## 2. API Specifications & System Architecture Details

The system specifications and technical features are built upon the architecture defined in `agent_folder/fastapi_ai_ecosystem_slides_detail.md`.

### API Endpoints Specification

| Method | Endpoint | Expected Status | Description & Technical Scope |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/v1/auth/register` | `201 Created` | User registration with Bcrypt password hashing. |
| **POST** | `/api/v1/auth/login` | `200 OK` | OAuth2 Password Bearer authentication returning JWT Access Token. |
| **GET** | `/api/v1/auth/me` | `200 OK` | Fetches authenticated user profile using `Authorization: Bearer <token>`. |
| **POST** | `/api/v1/datasets/upload` | `201 Created` | Uploads binary raw datasets to MinIO `raw-datasets` bucket and registers metadata in PostgreSQL. |
| **GET** | `/api/v1/datasets` | `200 OK` | Lists dataset metadata with pagination and sorting. |
| **POST** | `/api/v1/models/register` | `201 Created` | Registers a new ML model version using the Append-Only Immutability pattern. |
| **GET** | `/api/v1/models` | `200 OK` | Returns registered model version listings and metrics lineage. |
| **POST** | `/api/v1/train` | `202 Accepted` | Triggers non-blocking asynchronous automated model training via ARQ & Redis Queue. |
| **POST** | `/api/v1/predict` | `200 OK` | Model inference engine that retrieves target model weights and computes prediction scores. |
| **GET** | `/api/v1/health` | `200 OK` | Diagnostic health check monitoring PostgreSQL, MinIO, Redis, and logging status in JSON format. |

### Detailed Module Explanations

#### Authentication Architecture
- **JWT HS256 Standard:** Access tokens are signed using HMAC-SHA256 with secret keys configured in `.env`.
- **Native Bcrypt Hashing:** Passwords are never stored in plain text. Passwords are securely hashed with native `bcrypt` via `passlib.context.CryptContext`.
- **Dependency Injection:** Endpoints protect routes by declaring `Depends(get_current_user)` to validate Bearer tokens on every incoming request.

#### Object Storage Flow
- **Dual-Layer Storage Separation:** Decouples binary payloads from metadata records.
- **MinIO Object Storage:** Stores actual raw dataset files in the dedicated `raw-datasets` bucket and model weights (`.pt`, `.onnx`) in artifact storage.
- **PostgreSQL Metadata Tracking:** Records file attributes (file name, MinIO object key path, file size in bytes, owner ID, upload timestamp) in PostgreSQL tables.

#### Model Registry Immutability Concept
- **Append-Only Pattern:** Existing database records in `model_record` are immutable and are never updated or deleted in-place.
- **Version Lineage Tracking:** Every training or model registration produces a distinct version row (for example `v1.0.0`, `v1.1.0`, `v2.0.0`) along with execution metrics (`accuracy`, `loss`).
- **Auditability and Rollback Safety:** Guarantees 100% auditability and allows seamless rollbacks to previous production model versions.

#### Async Training System Architecture
- **Non-blocking Execution:** Calls to `POST /api/v1/train` return immediate `202 Accepted` responses containing a unique `job_id`, preventing HTTP request timeouts.
- **ARQ & Redis Task Worker:** Tasks are enqueued into a Redis Queue. Background ARQ worker processes pull tasks, execute model training on CPU/GPU hardware, stream progress updates, and save trained weights back to MinIO and PostgreSQL.

#### Comprehensive Error Logging System
- **Structured JSON Logging:** All log output is serialized into standard JSON strings containing `timestamp`, `log_level`, `logger_name`, `message`, and contextual request attributes.
- **Log Files Location:** Main log files are stored under `logs/backend.log` (FastAPI Gateway logs) and `logs/app.log` (general application runtime logs), alongside `logs/database.log` and `logs/minio.log`.
- **Traceback and Debugging:** Captures detailed exception stack traces, request execution durations (`duration_ms`), and caller file/line metadata for debugging.

---

## 3. Project Directory Structure

```text
ai-eco/
├── backend/                        # FastAPI Backend Application Core
│   ├── core/                       # Core Configuration & Security Settings
│   │   ├── config.py               # Pydantic BaseSettings & Environment Configuration
│   │   └── security.py             # Bcrypt Password Hashing & JWT Token Management
│   ├── db/                         # Database Connection & Engine Setup
│   │   └── database.py             # SQLAlchemy Async/Sync Engine & Session Factories
│   ├── models/                     # SQLAlchemy Database ORM Models
│   │   ├── dataset.py              # DatasetModel (Metadata tracking for MinIO)
│   │   ├── model_registry.py       # ModelRegistryModel (Append-Only ML model records)
│   │   └── user.py                 # UserModel (User authentication & credentials)
│   ├── routes/                     # FastAPI Router Controllers (Endpoints)
│   │   ├── auth.py                 # Authentication Routes (/login, /register, /me)
│   │   ├── datasets.py             # Dataset Management Routes (/upload, /list)
│   │   ├── health.py               # Health & Diagnostic Check Routes (/health)
│   │   ├── inference.py            # Model Prediction Engine Routes (/predict)
│   │   ├── models.py               # Model Registry Routes (/register, /versions)
│   │   └── train.py                # Asynchronous Training Pipeline Routes (/train)
│   ├── schemas/                    # Pydantic Schemas & Request/Response Validation
│   │   ├── auth.py                 # Authentication Payload Schemas
│   │   ├── dataset.py              # Dataset Payload Schemas
│   │   ├── inference.py            # Inference Payload Schemas
│   │   ├── model.py                # Model Registry Payload Schemas
│   │   └── train.py                # Training Submission & Job Status Schemas
│   ├── services/                   # Business Logic & External Integrations
│   │   ├── enqueue_job.py          # ARQ Redis Task Dispatcher
│   │   ├── minio_service.py        # MinIO SDK Wrapper for Storage Operations
│   │   └── worker_settings.py      # ARQ Worker Handler Configurations
│   └── main.py                     # FastAPI Main App Entrypoint & Middleware Setup
├── frontend/                       # React Frontend Web Application (Vite)
│   ├── public/                     # Static Public Web Assets
│   ├── src/                        # React Source Code
│   │   ├── assets/                 # Graphics & Theme Assets
│   │   ├── App.css                 # Custom Styling & Design System
│   │   ├── App.jsx                 # Main Application Layout & Auth Routes
│   │   ├── index.css               # Global Base Styles
│   │   └── main.jsx                # React Entrypoint Mount
│   ├── package.json                # Node.js Dependencies & NPM Scripts
│   └── vite.config.js              # Vite Bundler & Server Settings
├── agent_folder/                   # Technical Documentation & Specifications
│   ├── fastapi_ai_ecosystem_slides_detail.md # Detailed Architecture Specification
│   ├── generate_report.py          # Executive PDF/Docx Report Generator
│   ├── README.md                   # Agent Folder Specifications Overview
│   ├── screenshots/                # Application Screenshots & Mockups
│   └── scripts/                    # Automation & Verification Scripts
├── logs/                           # System Subsystem JSON Log Files
│   ├── app.log                     # Application General Log
│   ├── app.log.sample              # Log Schema Sample Reference
│   ├── backend.log                 # FastAPI Gateway Log
│   ├── backend.log.sample          # Backend Log Sample Reference
│   ├── database.log                # PostgreSQL Log
│   ├── database.log.sample         # Database Log Sample Reference
│   ├── minio.log                   # MinIO Storage Operation Log
│   └── minio.log.sample            # MinIO Log Sample Reference
├── utils/                          # Common Utility Modules
│   ├── dir_utils.py                # Directory Structure Management Utilities
│   ├── logger.py                   # Custom Structured JSON Logger
│   └── logging_utils.py            # Logging & Metric Decorators
├── tests/                          # Automated Integration & Unit Tests
├── .env.sample                     # Environment Variables Configuration Template
├── compose.yml                     # Docker Compose Orchestration (PostgreSQL, Redis, MinIO, Label Studio)
├── pyproject.toml                  # Python Project Metadata & Dependencies
├── run.sh                          # FastAPI Uvicorn Server Launcher Script
├── task-graph.md                   # Task Breakdown & Execution Status
├── architecture.md                 # System Architecture Documentation
└── README.md                       # Project Root Documentation
```