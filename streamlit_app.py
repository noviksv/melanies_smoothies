# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

option = st.selectbox("What is your favourite fruit?",
                     ("Banana", "Strawberries", "Peaches"))

st.write("Your favourite fruit is:", option)
name_on_order = st.text_input("Name on Smoothie")
st.write(f"the name on your smoothie will be:{name_on_order}")

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredents_list = st.multiselect("choose up to 5 ingridients:", my_dataframe,
                     max_selections=6)
if ingredents_list:
    ingredents_string = ''

    for fruit_chosen in ingredents_list:
        ingredents_string += fruit_chosen + ' '

    st.write(ingredents_string)
    
    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients,name_on_order)
            values ('{ingredents_string}','{name_on_order}' )"""

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        if ingredents_string:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
