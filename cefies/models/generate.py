from enum import Enum
from pydantic import BaseModel, Field, StringConstraints, field_validator
from typing import List, Annotated

class LangEnum(str, Enum):
    id = 'indonesian'
    en = 'english'

class RecipeGenerationModel(BaseModel):
    ingredients: List[str] = Field(..., min_length=1)
    topic: Annotated[str, StringConstraints(min_length=1)] = 'cheap meals'

class RecipeModel(BaseModel):
    name: str
    ingredients: List[str] = Field(..., min_length=1)
    steps: List[str] = Field(..., min_length=1)
    lang: LangEnum
    
class RecipeListModel(BaseModel):
    error: bool
    recipes: List[RecipeModel] = Field(..., min_length=1)
    
    @field_validator('recipes')
    @classmethod
    def check_langs(cls, recipes: List[RecipeModel]):
        lang_set = set([recipe.lang for recipe in recipes])
        required_set = set([lang.value for lang in LangEnum])
        intersect = lang_set.intersection(required_set)
        if len(intersect) != len(required_set):
            raise ValueError('required language not available')
        return recipes

class GenerationErrorModel(BaseModel):
    message: str
    error: bool
