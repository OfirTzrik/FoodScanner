import streamlit as st
import pandas as pd
import request_spoon as rs

st.title("Food Scanner")

search_options = st.selectbox("choose the searching mode:", ["by ingredients", "by nutrients"])
# The option to search food by the ingredients

if search_options == "by ingredients":
    if "items" not in st.session_state:
        st.session_state.items = []

    # input fields
    IngredientName = st.text_input("Enter item name:")
    Ingredient_amount = st.number_input("Enter the amount of the ingredient:",min_value=1, step=1, value=1)
    # a button the add the ingredient
    if st.button("Add to list"):
        if IngredientName.strip():
            found = False
            for item in st.session_state["items"]:
                if item["name"].lower() == IngredientName.strip().lower():
                    item["amount"] += Ingredient_amount
                    found = True
                    break
            
            if not found:
                st.session_state["items"].append({
                    "name": IngredientName.strip(),
                    "amount": Ingredient_amount
                })
            
            st.success(f"Added: {IngredientName}")

    # options to increase or decrease or delete the amount of each ingredient

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

            if delete.button("🗑️ Delete", key=f"delete_{item['name']}"):
                st.session_state["items"].remove(item)
                st.success(f"Deleted: {item['name']}")
                st.rerun()  # refresh UI after deletion

    # Request recipes as long as at least one ingredient was entered
    if st.button("Get recipes") and len(st.session_state["items"]) > 1:
        # Currently does not take amount into account
        items_as_list = [item["name"] for item in st.session_state["items"]]
        recipes = rs.requestRecipeSteps(items_as_list, 2); # For now request 2 recipes due to spoonacular API tier limits
        for info, steps in recipes:
            info_col, steps_col = st.columns(2)

            # left side column
            info_col.subheader(info.get("title", "No title"))
            info_col.image(info.get("image", ""), use_container_width=True)
            info_col.markdown("📝 Ingredients")

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

# The option to search food by the nutrients

elif search_options == "by nutrients":
    st.subheader("set your nutrients values to filter:")

    min_nutr, max_nutr = st.columns(2)
    with min_nutr:
        min_cal = st.number_input("Min Caloriea (g)", min_value=0, max_value=5000, value=0)
        min_protein = st.number_input("Min Protein (g)", min_value=0, max_value=200, value=0)
        min_carbs = st.number_input("Min Carbs (g)", min_value=0, max_value=500, value=0)
        min_fat = st.number_input("Min Fat (g)", min_value=0, max_value=500, value=0)

    with max_nutr:
        max_cal = st.number_input("Max Calorie (g)", min_value=0, max_value=5000, value=5000)
        max_protein = st.number_input("Max Protein (g)", min_value=0, max_value=200, value=100)
        max_carbs = st.number_input("Max Carbs (g)", min_value=0, max_value=500, value=100)
        max_fat = st.number_input("Max Fat (g)", min_value=0, max_value=150, value=50 )

    if(min_protein > max_protein or min_carbs > max_carbs or min_cal > max_cal or min_fat > max_fat):
        st.error("the min nutrients must be smaller then the max nutrients")
    else:
        if st.button("get recipe(nutrients)"):
            recipes = rs.requestRecipeByNutrients(
                min_carbs=min_carbs, max_carbs=max_carbs,
                min_protein=min_protein, max_protein=max_protein,
                min_calories=min_cal, max_calories=max_cal,
                min_fat=min_fat, max_fat=max_fat,
                number_of_recipes=2
            )
        
    
            for info, steps in recipes:
                info_col, steps_col = st.columns(2)

                 # Left side (recipe info + nutrients)
                info_col.subheader(info.get("title", "No title"))
                info_col.image(info.get("image", ""), use_container_width=True)

                info_col.markdown("📝 Ingredients")
                

                # 🥗 Show nutrients
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