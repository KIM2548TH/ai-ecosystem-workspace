# Task Graph: Assignment #04 - MinIO Object Storage & JSON System Logging Architecture

## Phase 1: Core Configuration & Docker Infrastructure
- [ ] Task 1.1: Update `compose.yml` to include MinIO service with `json-file` logging driver. It must NOT contain hardcoded credentials or default fallbacks (e.g., `:-minioadmin`), but strictly reference environment variables `${MINIO_ROOT_USER}`, `${MINIO_ROOT_PASSWORD}`, `${POSTGRES_USER}`, and `${POSTGRES_PASSWORD}`.
- [ ] Task 1.2: Implement Environment Variable Isolation by creating `.env` (loaded dynamically) and `.env.sample` (for documentation) to store credentials like `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`.
- [ ] Task 1.3: Update `.gitignore` to exclude `logs/` directory and `.env` files (but allow `.env.sample`).

## Phase 2: Custom JSON System Logging Architecture
- [ ] Task 2.1: Create `utils/logger.py` with `JSONFormatter` to structure logs as JSON.
- [ ] Task 2.2: Implement `StreamHandler` and multiple `FileHandler`s in `utils/logger.py` to route logs to specific component files (`logs/backend.log`, `logs/database.log`, `logs/minio.log`, `logs/system.log`).
- [ ] Task 2.3: Implement logging decorators and helper functions: `@log_execution`, `log_success`, `log_fail` (with traceback capture).
- [ ] Task 2.4: Create `tests/logging/test_logger.py` to verify the JSON logging format and routing to the respective separate log files. (Note: Both `tests/` and `sandbox/` paths are supported for testing and execution).
- [ ] Task 2.5: Create sample log files (e.g., `logs/app.log.sample`, `logs/backend.log.sample`, `logs/minio.log.sample`) with valid JSON entries, and verify `.gitignore` strictly ignores `.log` but allows `.sample`.

## Phase 3: Backend MinIO Service Architecture & Sandboxes
- [ ] Task 3.1: Update `backend/core/config.py` to include MinIO Pydantic Settings (`minio_endpoint`, `minio_root_user`, `minio_root_password`, `minio_bucket`), which load the credentials dynamically via environment variables.
- [ ] Task 3.2: Create `backend/services/minio_service.py` containing `MinIOService` class wrapping `minio` Python SDK for bucket setup, `fput_object`, `fget_object`, and bucket versioning.
- [ ] Task 3.3: Create `tests/minio/test_upload_download.py` and `tests/minio/test_upload_photo.py` importing from `backend.services.minio_service` to demonstrate basic object upload and download. (Note: Both `tests/` and `sandbox/` paths supported).
- [ ] Task 3.4: Create `tests/minio/test_versioning.py` importing from `backend.services.minio_service` to demonstrate MinIO object versioning capabilities.

## Phase 4: Fresh DOCX Report Generation
- [ ] Task 4.1: Create a script in `agent_folder/scripts/` to generate a fresh, perfectly formatted document from scratch using `python-docx`.
- [ ] Task 4.2: Ensure the report includes the Title: "รายงานผลการปฏิบัติงาน Assignment #04 (MinIO Object Storage & System Logging Architecture)" and Student: "นายจิตรกร จันทร์สังข์ (6710110055)".
- [ ] Task 4.3: Apply the following formatting requirements:
  - **Thai Primary Language**: All text, section headers, explanations, and instructions must be written in primary Thai language (ภาษาไทยทางการ 100%).
  - **Clean Placeholder Boxes**: Create clean placeholder table boxes `[ กรอบสำหรับวางรูปภาพ... ]` for all 6 image sections.
  - **Concise Code Summaries**: Specify the exact file path, short high-level mechanism, key functions, and a 3-5 line core code example instead of full file dumps.
  - **Placeholder Action Summary**: Under each placeholder box, provide short Thai guidance detailing `📌 คำสั่งที่ต้องรัน/วิธีทำ` and `🖼️ รูปที่ต้องนำมาใส่`.
- [ ] Task 4.4: Generate the document and save it to both target files: `Assignment-4_6710110055.docx` and `6710110055ad4.docx`.
- [ ] Task 4.5: Create `agent_folder/README.md` to document the agent tools used.

**NOTE:** Do NOT add any git push task ("ห้ามพุตก่อน").
