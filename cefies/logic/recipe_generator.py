import json
from cefies.internal.gemini import llm
from cefies.models.generate import RecipeModel, GenerationErrorModel

RECIPE_GENERATION_TEMPLATE = """
Generate a recipe containing name, ingredients, and steps in JSON format from subset of given ingredients. If it is impossible to create one, tell us the reason in JSON format (see below). Minimal recipe with small number of ingredients is okay, just create minimal recipe in it, you don't need to create perfect recipe. I'm asking for recipe, not code to make it happen. You are not allowed to answer anything other than in this format:

Success Format:
{"name": str, "ingredients": list[str], "steps": list[str], "error": false}

Failed Format:
{"error": true, "message": str}

Note: For steps, don't give numbering or endline

Ingredient List:
"""

def generate_recipe(ingredients: list[str]):
    ingredient_contents = "\n- " + "\n- ".join(ingredients)
    contents = RECIPE_GENERATION_TEMPLATE + ingredient_contents
    response_raw = llm.generate_content(contents).text
    
    try:
        response = RecipeModel.model_validate_json(response_raw)
    except ValueError:
        try:
            response = GenerationErrorModel.model_validate_json(response_raw)
        except ValueError:
            response = GenerationErrorModel(message="invalid model response", error=True)
    return response