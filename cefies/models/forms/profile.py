from fastapi import Form, UploadFile, File

from cefies.models.forms.base import BaseForm

class EditProfileForm(BaseForm):
    def __init__(
            self,
            name: str = Form(...),
            avatar: UploadFile = File(...),
    ):
        self.name = name
        self.avatar = avatar
