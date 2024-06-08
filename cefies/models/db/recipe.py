from typing import List
from fireo.typedmodels import TypedModel
from cefies.models.db.user import User


class Recipe(TypedModel):
    creator: User
    image: str
    ingredients: List[str]
    steps: List[str]
    title: str

    class Meta:
        collection_name = "recipes"
