# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :balloon:")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# -----------------------------
# SESSION HANDLING (FIX)
# -----------------------------
try:
    # Works ONLY inside Snowflake Streamlit
    session = get_active_session()
except:
    # Fallback for GitHub / local execution
    connection_parameters = {
        "account" : "BZNJCAL-DLB00315",
        "user" : "Avanindraa",
        "password" : "Allstargod12**",
        "role" : "SYSADMIN",
        "warehouse" : "COMPUTE_WH",
        "database" : "SMOOTHIES",
        "schema" : "PUBLIC",
        "client_session_keep_alive" : "true"
    }
    session = Session.builder.configs(connection_parameters).create()

# -----------------------------
# APP LOGIC (UNCHANGED)
# -----------------------------
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)

if ingredients_list:
    ingredients_string = ""

    for fruit in ingredients_list:
        ingredients_string += fruit + " "

        api_name = fruit_df.loc[
            fruit_df["FRUIT_NAME"] == fruit, "SEARCH_ON"
        ].values[0]

        st.subheader(f"{fruit} Nutrition Information")

        response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{api_name}"
        )

        st.dataframe(response.json(), use_container_width=True)

    insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")



