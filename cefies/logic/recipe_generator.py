import json
from cefies.internal.gemini import llm
from cefies.models.generate import RecipeModel

RECIPE_GENERATION_TEMPLATE = """
Generate a recipe containing name, ingredients, and steps in JSON format from strictly given ingredients. If it is impossible to create one, just output -1, don't try to add new ingredients. I'm asking for recipe, not code to make it happen. You are not allowed to answer anything other than in this format:

Success Format:
{"name": str, "ingredients": list[str], "steps": list[str]}

Failed Format:
-1

Note: For steps, don't give numbering or endline

Ingredient List:
"""

def generate_recipe(ingredients: list[str]):
    ingredient_contents = "\n- " + "\n- ".join(ingredients)
    contents = RECIPE_GENERATION_TEMPLATE + ingredient_contents
    response_raw = llm.generate_content(contents).text
    
    try:
        response = json.loads(response_raw)
        recipe = RecipeModel(**response)
    except Exception:
        return None
    return recipe