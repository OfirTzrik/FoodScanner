import streamlit as st
import pandas as pd
import request_spoon as rs
import os
from PIL import Image

def updatePageConfig():
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    os.chdir("..")
    icon = Image.open("assets/logo.png")
    st.set_page_config(page_title="Food Scanner", page_icon=icon)
    left, center, right = st.columns([1,1.5,1])
    center.image(icon)

def showByIngredients():
    """
    Search for recipes based on the ingredients entered by the user.
    Returns 2 recipes (Spoonacular's API (free tier) is limited to 50 points per day).
    """
    if "items" not in st.session_state:
        st.session_state.items = [] # Holds the list of ingredients entered

    # Enter ingredients and add to list
    ingredient_name = st.text_input("Enter item name:")
    ingredient_amount = st.number_input("Enter the amount of the ingredient:",min_value=1, step=1, value=1)
    if st.button("Add to list"):
        if ingredient_name.strip():
            found = False
            for item in st.session_state["items"]:
                if item["name"].lower() == ingredient_name.strip().lower():
                    item["amount"] += ingredient_amount
                    found = True
                    break
            
            # Ingredient was not found
            if not found:
                st.session_state["items"].append({
                    "name": ingredient_name.strip().capitalize(),
                    "amount": ingredient_amount
                })
            
            st.success(f"Added: {ingredient_name}")

    # Increase / decrease amount of each ingredient
    if st.session_state["items"]:
        st.subheader("List of ingredients:")
        for item in st.session_state["items"]:
            col1, increase, decrease, delete = st.columns([2,1,1,1])
            col1.write(f"{item['name']}: {item['amount']}")

            if increase.button("➕", key=f"plus_{item['name']}"):
                item["amount"] += 1

            if decrease.button("➖", key=f"minus_{item['name']}"):
                if item["amount"] > 1:
                    item["amount"] -= 1
                else:
                    st.warning(f"{item['name']} can’t be less than 1")

            # Remove the ingredient from the list
            if delete.button("🗑️ Delete", key=f"delete_{item['name']}"):
                st.session_state["items"].remove(item)
                st.success(f"Deleted: {item['name']}")
                st.rerun() # Refresh UI after deletion

    # Request recipes as long as at least one ingredient was entered
    if st.button("Get recipe(s)") and len(st.session_state["items"]) > 1:
        # Currently does not take amount into account
        items_as_list = [item["name"] for item in st.session_state["items"]]
        recipes = rs.requestRecipeByIngredients(items_as_list, 2); # For now request 2 recipes due to spoonacular API tier limits
        for info, steps in recipes:
            info_col, steps_col = st.columns(2)

            # left side column
            info_col.subheader(info.get("title", "No title"))
            info_col.image(info.get("image", ""), use_container_width=True)
            info_col.markdown("📝 Missing ingredients")
            # List the missing ingredients
            if "missedIngredients" in info:
                for ing in info["missedIngredients"]:
                    col1, col2 = st.columns([1,4])
                    if "image" in ing:
                        col1.image(ing["image"], width=40)
                    col2.write(f"**{ing['original']}**")
            
            # right side column
            steps_col.markdown("👩‍🍳 Instructions")
            if steps and isinstance(steps, list) and len(steps) > 0:
                for step in steps[0]["steps"]:
                    steps_col.markdown(f"{step['number']}. {step['step']}")
            else:
                steps_col.write("No instructions available.")

def showByNutrients():
    """
    Search for recipes based on the nutrients values entered by the user.
    returns 2 recipes (Spoonacular's API (free tier) is limited to 50 points per day).
    """
    st.subheader("Set your nutrients values to filter:")
    
    min_cal, max_cal = st.slider("Min to max calories", 0, 5000, (500, 4500), 50)
    min_protein, max_protein = st.slider("Min to max protiens (g)", 0, 200, (50, 150), 5)
    min_carbs, max_carbs = st.slider("Min to max carbs (g)", 0, 500, (50, 450), 5)
    min_fat, max_fat = st.slider("Min to max fats (g)", 0, 500, (50, 450), 5)

    if min_protein >= max_protein or min_carbs >= max_carbs or min_cal >= max_cal or min_fat >= max_fat:
        st.error("Minimum nutrients must be less than maximum nutrients.")
    else:
        if st.button("Get recipe(s)"):
            recipes = rs.requestRecipeByNutrients(min_carbs=min_carbs, max_carbs=max_carbs, min_protein=min_protein, max_protein=max_protein, min_calories=min_cal, max_calories=max_cal, min_fat=min_fat, max_fat=max_fat, number_of_recipes=2)

            for info, steps in recipes:
                full_info = rs.requestRecipeInformation(info["id"])
                info_col, steps_col = st.columns(2)
                 # Left side (recipe info + nutrients)
                info_col.subheader(info.get("title", "No title"))
                info_col.image(info.get("image", ""), use_container_width=True)

                # List the required ingredients
                info_col.markdown("📝 Ingredients")
                if "extendedIngredients" in full_info:
                    for ing in full_info["extendedIngredients"]:
                        col1, col2 = info_col.columns([1,4])
                        if "image" in ing:
                            col1.image(f"https://spoonacular.com/cdn/ingredients_100x100/{ing['image']}", width=40)
                        col2.write(f"**{ing['original']}**")
                else:
                    info_col.write("No ingredient details available.")

                # Show nutrient facts
                info_col.markdown("### Nutrition facts")
                info_col.write(f"Calories: {info.get('calories', 'N/A')}")
                info_col.write(f"Protein: {info.get('protein', 'N/A')}")
                info_col.write(f"Fat: {info.get('fat', 'N/A')}")
                info_col.write(f"Carbs: {info.get('carbs', 'N/A')}")

                steps_col.markdown("👩‍🍳 Instructions")
                if steps:
                    for step in steps[0]["steps"]:
                        steps_col.markdown(f"{step['number']}. {step['step']}")
                else:
                    steps_col.write("No instructions available.")

updatePageConfig()
st.header("Food Scanner", divider=True)
search_options = st.selectbox("Choose search mode:", ["by ingredients", "by nutrients"])

# Display the fields depending on the search option
if search_options == "by ingredients":
    showByIngredients()
elif search_options == "by nutrients":
    showByNutrients()