# Architecture: Assignment #04

## Student Identity
- **Student Name**: นายจิตรกร จันทร์สังข์
- **Student ID**: 6710110055

## Overview
This architecture integrates MinIO for object storage and implements a robust, structured JSON logging system. It ensures all system events are captured in a predictable format, facilitating easier debugging, monitoring, and audit trails.

## Infrastructure: MinIO Docker Setup
- **Containerization**: MinIO runs as a Docker container defined in `compose.yml`.
- **Storage**: Persistent volumes are used to ensure object storage survives container restarts.
- **Access (Security Protocol)**: Hardcoded credentials and default fallbacks (e.g., `:-minioadmin`) are strictly prohibited in `compose.yml`. Credentials (`MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) are loaded dynamically from an isolated `.env` file, while `compose.yml` strictly references `${MINIO_ROOT_USER}`, `${MINIO_ROOT_PASSWORD}`, `${POSTGRES_USER}`, and `${POSTGRES_PASSWORD}`. An `.env.sample` documents the required variables.
- **Logging**: The MinIO container is configured to use the Docker `json-file` logging driver.

## Backend MinIO Service Architecture
- **Configuration**: `backend/core/config.py` contains MinIO Pydantic Settings (`minio_endpoint`, `minio_root_user`, `minio_root_password`, `minio_bucket`), which load credentials via environment variables to maintain security.
- **Service Layer**: `backend/services/minio_service.py` houses the `MinIOService` class, wrapping the `minio` Python SDK to handle bucket setup, object operations (`fput_object`, `fget_object`), and bucket versioning.
- **Testing & Sandboxes**: Organized test scripts in `tests/` (e.g., `tests/minio/test_upload_download.py`, `tests/minio/test_upload_photo.py`, `tests/minio/test_versioning.py`, `tests/logging/test_logger.py`). Both `tests/` and `sandbox/` paths are supported for testing and execution. They import from `backend.services.minio_service` to validate uploads, downloads, and versioning functionality.

## JSON Logging Specification
All system logs are structured as JSON payloads with the following mandatory fields:

- `timestamp`: ISO-8601 string (e.g., "2026-07-26T10:22:44+07:00")
- `system_name`: Component or Service Name
- `log_level`: DEBUG / INFO / WARNING / ERROR
- `location`: filename:line_number
- `operation`: Operation name
- `status`: SUCCESS / FAIL / IN_PROGRESS
- `duration_ms`: Execution time in milliseconds
- `message`: Log text
- `details`: Context dictionary
- `exception`: Traceback details if error occurred

## Logging Implementation
- **Formatters**: `JSONFormatter` in `utils/logger.py` ensures the structure matches the specification.
- **Handlers**:
  - `StreamHandler`: Outputs JSON logs to the standard output for immediate visibility.
  - `FileHandler`: Persists JSON logs to separated files in host directory `./logs/` for historical analysis.
    - `logs/backend.log` (Backend API & Logic)
    - `logs/database.log` (Postgres / Query logs)
    - `logs/minio.log` (MinIO Object Storage operations)
    - `logs/system.log` (Overall System & Lifecycle events)
- **Git Sample Log Tracking**: Real `.log` files are excluded via `.gitignore`, but `.log.sample` files with valid JSON entries are tracked and committed for inspection.
- **Decorators/Helpers**: `@log_execution` wraps functions to automatically measure `duration_ms` and determine `status`. `log_success` and `log_fail` provide standardized entry points for logging outcomes.

## Fresh DOCX Generation Protocol
- **Generation Method**: Generate a fresh, perfectly formatted document from scratch using `python-docx`.
- **Target Files**: Output to both `Assignment-4_6710110055.docx` and `6710110055ad4.docx`.
- **Document Header**: 
  - Title: รายงานผลการปฏิบัติงาน Assignment #04 (MinIO Object Storage & System Logging Architecture)
  - Student: นายจิตรกร จันทร์สังข์ (6710110055)
- **Formatting Requirements**:
  - **Thai Primary Language**: All text, section headers, explanations, and instructions must be written in primary Thai language (ภาษาไทยทางการ 100%).
  - **Clean Placeholder Boxes**: Use clean placeholder table boxes `[ กรอบสำหรับวางรูปภาพ... ]` for all 6 image sections.
  - **Concise Code Summaries**: Specify the exact file path, short high-level mechanism, key functions, and a 3-5 line core code example instead of full file dumps.
  - **Placeholder Guidance**: Under each placeholder box, provide short Thai guidance detailing `📌 คำสั่งที่ต้องรัน/วิธีทำ` and `🖼️ รูปที่ต้องนำมาใส่`.
