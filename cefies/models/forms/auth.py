from fastapi import Form

from cefies.models.forms.base import BaseForm

class RegisterForm(BaseForm):
    def __init__(
            self,
            email: str = Form(...),
            name: str = Form(...),
            password: str = Form(...),
            # TODO file: UploadFile = File(...),
    ):
        self.email = email
        self.name = name
        self.password = password
