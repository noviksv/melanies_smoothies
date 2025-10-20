# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)



name_on_order = st.text_input("Name on Smoothie")
st.write(f"the name on your smoothie will be:{name_on_order}")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(data=pd_df)


ingredents_list = st.multiselect("choose up to 5 ingridients:", my_dataframe,
                     max_selections=6)
if ingredents_list:
    ingredents_string = ''

    for fruit_chosen in ingredents_list:
        ingredents_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.write(ingredents_string)
    
    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients,name_on_order)
            values ('{ingredents_string}','{name_on_order}' )"""

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        if ingredents_string:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

