import os
import google.oauth2.service_account as service_account
import google.generativeai as genai

service_account_path = os.getenv("SERVICE_ACCOUNT_PATH")
if service_account_path:
    cred = service_account.Credentials.from_service_account_file(service_account_path)
else:
    raise ValueError("invalid google service account path")

genai.configure(credentials=cred)
llm = genai.GenerativeModel(model_name="gemini-pro")
