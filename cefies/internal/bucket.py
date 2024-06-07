import os
import cefies.internal.firestore  # noqa: F401L: Intended to initialize firebase

from firebase_admin import storage

assets_bucket = storage.bucket(os.getenv("STORAGE_BUCKET", "chefies-assets"))


def upload_file(content: bytes | str, target_path: str):
    blob = assets_bucket.blob(target_path)
    blob.upload_from_string(content)

    return blob.public_url
