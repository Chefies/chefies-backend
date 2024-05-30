from pydantic import BaseModel, Field
from typing import List

class RecipeGenerationModel(BaseModel):
    ingredients: List[str] = Field(..., min_length=1)

class RecipeModel(BaseModel):
    name: str
    ingredients: List[str] = Field(..., min_length=1)
    steps: List[str] = Field(..., min_length=1)
