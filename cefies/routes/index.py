from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from cefies.models.firebase import DecodedIdToken
from cefies.models.generate import RecipeGenerationModel
from cefies.logic.recipe_generator import generate_recipe
from cefies.security import get_current_user


router = APIRouter()


@router.get("/")
def hello_world():
    return "Hello world!"


@router.post("/generate/recipes")
def generate_recipes(
    user: Annotated[DecodedIdToken, Depends(get_current_user)],
    request_body: RecipeGenerationModel,
):
    ingredients = request_body.ingredients
    recipe = generate_recipe(ingredients)
    if recipe:
        return JSONResponse(content=recipe.model_dump(), status_code=201)
    else:
        return JSONResponse(content={"detail": "invalid model response"}, status_code=500)
