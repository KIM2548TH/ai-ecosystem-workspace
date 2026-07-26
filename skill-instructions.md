# Verification Protocols & Instructions

## MinIO Verification
1. **Container Health**: Ensure the MinIO Docker container is running and healthy.
2. **Environment Variable Security**: Verify `compose.yml` contains NO hardcoded credentials or fallbacks (e.g., `:-minioadmin`) and strictly uses `${MINIO_ROOT_USER}`, `${MINIO_ROOT_PASSWORD}`, `${POSTGRES_USER}`, and `${POSTGRES_PASSWORD}`. Ensure `.env` is used for dynamic loading and `.env.sample` exists. Verify `backend/core/config.py` loads these via Pydantic Settings.
3. **Access & Connectivity**: Use `backend/core/config.py` variables to connect to MinIO via the `MinIOService` in `backend/services/minio_service.py`. Ensure no connection refused errors occur.
3. **Upload/Download Testing**: Run `tests/minio/test_upload_download.py` and `tests/minio/test_upload_photo.py` (importing from `backend.services.minio_service`) and verify:
   - Object is successfully uploaded to the specified bucket.
   - Object can be successfully downloaded and its integrity matches the uploaded file.
4. **Versioning Testing**: Run `tests/minio/test_versioning.py` (importing from `backend.services.minio_service`) and verify:
   - Versioning can be enabled on a bucket.
   - Uploading the same object name multiple times creates distinct versions.
   - Specific versions can be retrieved by providing the version ID.

## JSON Logging Verification
1. **File Creation**: Verify that running any script utilizing the logger automatically creates the host-mapped `logs/` directory and corresponding specific files (`logs/backend.log`, `logs/database.log`, `logs/minio.log`, `logs/system.log`) if they do not exist.
2. **Git Sample Validation**: Verify `.gitignore` is strictly ignoring `.log` files, but `.log.sample` files with sample JSON data are committed and visible in git.
3. **JSON Format Validation**: Inspect the separate `.log` files and the console output when running `tests/logging/test_logger.py`. Each line MUST be a valid JSON object. (Note: Both `tests/` and `sandbox/` paths are valid and supported).
4. **Field Presence**: Verify that every JSON log entry contains the mandatory fields: `timestamp`, `system_name`, `log_level`, `location`, `operation`, `status`, `duration_ms`, `message`, `details`, and `exception` (if applicable).
5. **Decorator Functionality**: Verify that `@log_execution` accurately captures the execution duration (`duration_ms`), infers the correct `location` (filename and line number), and correctly sets the `status`.
6. **Exception Tracing**: When an error is intentionally triggered and logged via `log_fail`, ensure the `exception` field contains the full, readable stack traceback.

## Fresh DOCX Generation Verification
1. **Generation Validation**: Verify that the script successfully generates a fresh document from scratch using `python-docx` without relying on existing templates.
2. **Output Files**: Verify that both `Assignment-4_6710110055.docx` and `6710110055ad4.docx` are generated.
3. **Header Validation**: Verify the document includes the Title "รายงานผลการปฏิบัติงาน Assignment #04 (MinIO Object Storage & System Logging Architecture)" and Student "นายจิตรกร จันทร์สังข์ (6710110055)".
4. **Formatting Requirements**:
   - **Thai Primary Language**: Verify that all text, section headers, explanations, and placeholder instructions are written in primary Thai language (ภาษาไทยทางการ 100%).
   - **Concise Code Summaries**: Verify that code snippets are not full-file dumps but specify the exact file path, short high-level mechanism, key functions, and a 3-5 line core code example.
   - **Placeholder Boxes & Guidance**: Verify there are clean placeholder table boxes `[ กรอบสำหรับวางรูปภาพ... ]` for all 6 image sections. Verify that under each box there is short Thai guidance detailing `📌 คำสั่งที่ต้องรัน/วิธีทำ` and `🖼️ รูปที่ต้องนำมาใส่`.
