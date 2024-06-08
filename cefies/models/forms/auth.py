from fastapi import Form, UploadFile, File

from cefies.models.forms.base import BaseForm

class RegisterForm(BaseForm):
    def __init__(
            self,
            email: str = Form(...),
            name: str = Form(...),
            password: str = Form(...),
            avatar: UploadFile = File(...),
    ):
        self.email = email
        self.name = name
        self.password = password
        self.avatar = avatar
