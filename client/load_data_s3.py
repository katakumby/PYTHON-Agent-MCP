import os
import sys
import boto3
import logging
from dotenv import load_dotenv

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

load_dotenv()


def get_s3_client():
    aws_key = os.getenv('S3_AKID') or os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret = os.getenv('S3_SK') or os.getenv('AWS_SECRET_ACCESS_KEY')
    s3_endpoint = os.getenv('S3_ENDPOINT')
    aws_region = os.getenv('AWS_REGION') or "us-east-1"

    if not aws_key or not aws_secret:
        logger.error("❌ Brak poświadczeń AWS/MinIO w .env")
        sys.exit(1)

    session = boto3.Session(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret, region_name=aws_region)

    if s3_endpoint:
        logger.info(f"🔌 Łączenie z MinIO: {s3_endpoint}")
        return session.client('s3', endpoint_url=s3_endpoint)
    else:
        return session.client('s3')


def upload_recursive(s3_client, bucket_name):
    local_path = os.getenv("LOCAL_DATA_PATH")
    if not local_path or not os.path.exists(local_path):
        logger.error(f"❌ Ścieżka LOCAL_DATA_PATH nie istnieje: {local_path}")
        sys.exit(1)

    # Normalizacja ścieżki
    root_path = os.path.abspath(local_path)
    logger.info(f"📂 Źródło danych: {root_path}")
    logger.info(f"📦 Cel S3 Bucket: {bucket_name}")
    logger.info("-" * 50)

    files_uploaded = 0

    # Przechodzimy przez wszystkie foldery
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            # Pomijamy pliki ukryte (np. .DS_Store, .git)
            if filename.startswith('.'):
                continue

            full_local_path = os.path.join(dirpath, filename)

            # Tworzymy ścieżkę relatywną, np: ISO20022/Cash Management/MDR/plik.pdf
            relative_path = os.path.relpath(full_local_path, root_path)

            # S3 wymaga slashy /, nawet na Windows
            s3_key = relative_path.replace(os.path.sep, "/")

            try:
                print(f"⬆️  {s3_key}")
                s3_client.upload_file(full_local_path, bucket_name, s3_key)
                files_uploaded += 1
            except Exception as e:
                logger.error(f"❌ Błąd przy {filename}: {e}")

    logger.info("-" * 50)
    logger.info(f"✅ Zakończono. Wysłano {files_uploaded} plików.")


if __name__ == "__main__":
    bucket = os.getenv("S3_BUCKET")
    if not bucket:
        print("Brak S3_BUCKET w .env")
        sys.exit(1)

    cli = get_s3_client()

    # Auto-tworzenie bucketa
    try:
        cli.head_bucket(Bucket=bucket)
    except:
        print(f"⚠️  Tworzenie bucketa {bucket}...")
        cli.create_bucket(Bucket=bucket)

    upload_recursive(cli, bucket)