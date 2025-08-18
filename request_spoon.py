import requests
import streamlit as st

def requestRecipeSteps(ingredients: list, number_of_recipes: int):
    """
    Return the information and steps of some n recipes
    Accepts the list of ingredients the user has and a number of recipes to retrieve
    Returned as a zip with each row being <information about the recipe, the recipe's steps>
    """
    # Request the recipes based on the ingredients passed
    ingredients_str = ",+".join(ingredients)
    request_parameters = {"ingredients": ingredients_str, "number": number_of_recipes,"apiKey": st.secrets["API_KEY"]}
    try:
        recipes = requests.get("https://api.spoonacular.com/recipes/findByIngredients", params=request_parameters)
    # This happens when the daily points limit has been reached (too many requests from spoonacular)
    except Exception as e:
        return None

    # Request the steps for each of the recipes received
    recipes_steps = []
    for recipe in recipes:
        url = "https://api.spoonacular.com/recipes/" + str(recipe["id"]) + "/analyzedInstructions"
        try:
            steps = requests.get(url, params=request_parameters).json()
        # This happens when the daily points limit has been reached (too many requests from spoonacular)
        except Exception as e:
            return None
        recipes_steps.append(steps)

    # Return (recipe, the recipe's steps) for each recipe
    return zip(recipes, recipes_steps)