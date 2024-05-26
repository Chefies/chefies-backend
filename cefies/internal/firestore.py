import os
import firebase_admin
from firebase_admin import firestore, credentials

service_account_path = os.getenv("SERVICE_ACCOUNT_PATH")
if service_account_path:
    cred = credentials.Certificate(service_account_path)
else:
    cred = credentials.ApplicationDefault()

app = firebase_admin.initialize_app(cred)
db = firestore.client()
