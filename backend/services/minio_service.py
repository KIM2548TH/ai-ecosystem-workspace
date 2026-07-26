from minio import Minio
from minio.versioningconfig import VersioningConfig, ENABLED
from backend.core.config import settings
from utils.logger import get_custom_logger

logger = get_custom_logger("MinIOService", settings.log_level, "minio")

class MinIOService:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_root_user,
            secret_key=settings.minio_root_password,
            secure=False
        )
        self.default_bucket = settings.minio_bucket

    def ensure_bucket(self, bucket_name: str = None):
        bucket = bucket_name or self.default_bucket
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)
            logger.info(
                f"Created bucket '{bucket}'",
                extra={"operation": "ensure_bucket", "status": "SUCCESS"}
            )
        else:
            logger.info(
                f"Bucket '{bucket}' already exists",
                extra={"operation": "ensure_bucket", "status": "INFO"}
            )

    def upload_file(self, object_name: str, file_path: str, bucket_name: str = None):
        bucket = bucket_name or self.default_bucket
        self.ensure_bucket(bucket)
        res = self.client.fput_object(bucket, object_name, file_path)
        logger.info(
            f"Uploaded '{file_path}' to '{bucket}/{object_name}'",
            extra={"operation": "upload_file", "status": "SUCCESS"}
        )
        return res

    def download_file(self, object_name: str, file_path: str, bucket_name: str = None, version_id: str = None):
        bucket = bucket_name or self.default_bucket
        self.client.fget_object(bucket, object_name, file_path, version_id=version_id)
        logger.info(
            f"Downloaded '{bucket}/{object_name}' to '{file_path}' (version: {version_id})",
            extra={"operation": "download_file", "status": "SUCCESS"}
        )

    def enable_versioning(self, bucket_name: str = None):
        bucket = bucket_name or self.default_bucket
        self.ensure_bucket(bucket)
        self.client.set_bucket_versioning(bucket, VersioningConfig(ENABLED))
        logger.info(
            f"Enabled versioning for bucket '{bucket}'",
            extra={"operation": "enable_versioning", "status": "SUCCESS"}
        )
