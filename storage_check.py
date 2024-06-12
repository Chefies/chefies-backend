from firebase_admin import credentials, storage
import firebase_admin
import os

import dotenv
dotenv.load_dotenv()

cred = credentials.Certificate("keys/credentials.json")
firebase_admin.initialize_app(cred)

bucket = storage.bucket(name="chefies-dev.appspot.com")
lst = bucket.list_blobs()
for blob in lst:
    print(blob)