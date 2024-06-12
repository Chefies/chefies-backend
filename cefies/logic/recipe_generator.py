from cefies.internal.gemini import llm
from cefies.models.generate import RecipeModel, GenerationErrorModel

DEFAULT_INGREDIENTS = ["Water", "Oil", "Rice", "Salt", "Sugar", "Pepper"]
RECIPE_GENERATION_SYSTEM_TEMPLATE = """
Generate a recipe containing name, ingredients, and steps in JSON format from subset of given ingredients.
If it is impossible to create one, tell us the reason in JSON format (see below), but you are expected
to make creative recipe with limited ingredients. Minimal recipe with small number of ingredients is okay,
just create minimal recipe in it, you don't need to create perfect recipe. I'm asking for recipe, not code
to make it happen. The steps need to be detailed. The topic of the recipe is about {{TOPIC}}. Also, you need
to give the response in {{LANG}} language. You are not allowed to answer anything other than in this format:

Success Format:
{"name": str, "ingredients": list[str], "steps": list[str], "error": false}

Failed Format:
{"error": true, "message": str}

Note: For steps, don't give numbering or endline
"""

def generate_recipe(ingredients: list[str], topic: str, lang: str):
    input_ingredients = DEFAULT_INGREDIENTS.copy()
    input_ingredients.extend(ingredients)
    
    system_prompt = RECIPE_GENERATION_SYSTEM_TEMPLATE.replace("{{LANG}}", lang)
    system_prompt = system_prompt.replace("{{TOPIC}}", topic)
    user_prompt = "Ingredients List: " + ", ".join(ingredients)
    
    messages = [
        {
            "role": "model",
            "parts": [system_prompt],
        },
        {
            "role": "user",
            "parts": [user_prompt],
        }
    ]
    response_raw = llm.generate_content(messages).text
    
    try:
        response = RecipeModel.model_validate_json(response_raw)
    except ValueError:
        try:
            response = GenerationErrorModel.model_validate_json(response_raw)
        except ValueError:
            response = GenerationErrorModel(message="invalid model response", error=True)
    return response