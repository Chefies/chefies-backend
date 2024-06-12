from enum import Enum
from pydantic import BaseModel, Field, StringConstraints
from typing import List, Annotated

class LangEnum(str, Enum):
    id = 'indonesian'
    en = 'english'

class RecipeGenerationModel(BaseModel):
    ingredients: List[str] = Field(..., min_length=1)
    topic: Annotated[str, StringConstraints(min_length=1)] = 'cheap meals'
    lang: LangEnum = LangEnum.en

class RecipeModel(BaseModel):
    name: str
    ingredients: List[str] = Field(..., min_length=1)
    steps: List[str] = Field(..., min_length=1)
    error: bool

class GenerationErrorModel(BaseModel):
    message: str
    error: bool
