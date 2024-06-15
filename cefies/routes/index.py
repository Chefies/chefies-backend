from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from cefies.models.firebase import DecodedIdToken
from cefies.models.generate import GenerationErrorModel, RecipeGenerationModel, RecipeListModel
from cefies.logic.recipe_generator import generate_recipe
from cefies.models.response import MessageResponse
from cefies.security import get_current_user


router = APIRouter()


@router.get("/")
def hello_world():
    return "Hello world!"


@router.post(
    "/generate/recipes",
    response_model=RecipeListModel,
    responses={500: {"model": MessageResponse}},
)
def generate_recipes(
    user: Annotated[DecodedIdToken, Depends(get_current_user)],
    request_body: RecipeGenerationModel,
):
    ingredients = request_body.ingredients
    topic = request_body.topic
    banned_recipes = request_body.banned_recipes
    recipe = generate_recipe(ingredients, topic, banned_recipes)
    if recipe:
        return recipe

    if isinstance(recipe, GenerationErrorModel):
        message = recipe.message
    else:
        message = "Cannot generate recipe"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=MessageResponse(error=True, message=message),
    )
