from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class LangEnum(str, Enum):
    id = 'indonesian'
    en = 'english'

class RecipeGenerationModel(BaseModel):
    ingredients: List[str] = Field(..., min_length=1)
    lang: LangEnum = LangEnum.en

class RecipeModel(BaseModel):
    name: str
    ingredients: List[str] = Field(..., min_length=1)
    steps: List[str] = Field(..., min_length=1)

class RecipeListModel(BaseModel):
    error: bool
    recipes: List[RecipeModel]

class GenerationErrorModel(BaseModel):
    message: str
    error: bool
