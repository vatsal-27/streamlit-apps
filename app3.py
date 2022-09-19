import pandas as pd
import streamlit as st
from load_css import local_css

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
local_css("stye.css")
# st.title("Auto Filter Dataframes in Streamlit")
# st.write(
#     """This app accomodates the blog [here](<https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/>)
#     and walks you through one example of how the Streamlit
#     Data Science Team builds add-on functions to Streamlit.
#     """
# )


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")
    if not modify:
        return df 

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)


    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)

    for column in to_filter_columns:
        left, right = st.columns((1, 20))
        left.write("↳")


        if is_categorical_dtype(df[column]) or df[column].nunique() < 80:
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].unique(),
                default=list(df[column].unique()),
            )
            df = df[df[column].isin(user_cat_input)]


        elif is_numeric_dtype(df[column]):
            _min = float(df[column].min())
            _max = float(df[column].max())
            step = (_max - _min) / 100
            user_num_input = right.slider(
            f"Values for {column}",
            min_value=_min,
            max_value=_max,
            value=(_min, _max),
            step=step,
            )
            df = df[df[column].between(*user_num_input)]


        elif is_datetime64_any_dtype(df[column]):
            user_date_input = right.date_input(
                f"Values for {column}",
                value=(
                    df[column].min(),
                    df[column].max(),
                ),
            )
            if len(user_date_input) == 2:
                user_date_input = tuple(map(pd.to_datetime, user_date_input))
                start_date, end_date = user_date_input
                df = df.loc[df[column].between(start_date, end_date)]

        else:
            user_text_input = right.text_input(
                f"Substring or regex in {column}",
            )
            if user_text_input:
                df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


# data_url = "https://raw.githubusercontent.com/mcnakhaee/palmerpenguins/master/palmerpenguins/data/penguins.csv"

# df = pd.read_csv(data_url)
#df = pd.read_csv("final_final_file.tsv" ,  sep='\t', engine="pyarrow")
df1=pd.read_csv("0 sliced_final_file.tsv" ,  sep='\t', engine="pyarrow")
df2=pd.read_csv("1 sliced_final_file.tsv" ,  sep='\t', engine="pyarrow")
df3=pd.read_csv("2 sliced_final_file.tsv" ,  sep='\t', engine="pyarrow")
df4=pd.read_csv("3 sliced_final_file.tsv" ,  sep='\t', engine="pyarrow")
df5=pd.read_csv("4 sliced_final_file.tsv" ,  sep='\t', engine="pyarrow")
df6=pd.read_csv("5 sliced_final_file.tsv" ,  sep='\t', engine="pyarrow")
df = pd.concat([df1,df2,df3,df4,df5,df6]) 
#df.rename(columns = {'karaka Relation':'karakarelation'}, inplace = True)
#print(df.columns)
#df['karakarelation'] = df.karakarelation.astype('category')
#st.dataframe(filter_dataframe(df))

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    
    
    options.configure_selection("multiple")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
	height=450,
	width='100%',
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )		

    print(selection)
    print("row:")
    print(selection["selected_rows"])
    print("data:")
    print(selection["data"])
    return selection


okk1 = pd.read_csv(
    "send_id.csv", engine="pyarrow")

id_sen_dict  = okk1.set_index('sent_id').to_dict()['sentence']
#df1=filter_dataframe(df)
selection = aggrid_interactive_table(df=df)

# csv  = df1.to_csv().encode('utf-8')
# st.download_button(
#      label="Download data as CSV",
#      data=csv,
#      file_name='filter.csv',
#      mime='text/csv',
#  )
print(selection)
if selection["selected_rows"]:

    for i in range(len(selection["selected_rows"])):
    	print("row:")
    	print(selection["selected_rows"])
    	print("data:")
    	print(selection["data"])
    	print("ok done")
    	key = selection["selected_rows"][i]['sent_id']
    	head_index = selection["selected_rows"][i]['head_index']
    	inflection_word = selection["selected_rows"][i]['Inflection/Surface form']
    	head_word = selection["selected_rows"][i]['head_inflection']
    	print(inflection_word)
    	print(head_word)
    	row  = df.loc[(df['sent_id'] == key)& (df['index'] == head_index)]
    	st.header("Sentence")
    	sen=id_sen_dict[key]
    	st.write(sen)
    	# split_sen = sen.split(inflection_word,1)    	
    	# print(split_sen)
    	# if head_word in split_sen[0]:
        #     head_split_sen = split_sen[0].split(head_word,1)  
        #     flag=0
    	# else:
        #     head_split_sen = split_sen[1].split(head_word,1)
        #     flag=1
    	# if(flag==0):
    	#     t1 = "<div>"+head_split_sen[0]+"<span class='highlight red'>"+head_word+"</span>"+head_split_sen[1]+"<span class='highlight blue'>"+inflection_word+"</span>"+split_sen[1]+"</div>"
    	# else:
        #     t1 = "<div>"+split_sen[0]+"<span class='highlight blue'>"+inflection_word+"</span>"+head_split_sen[0]+"<span class='highlight red'>"+head_word+"</span>"+head_split_sen[1]+"</div>"
    	# st.markdown(t1, unsafe_allow_html=True)
    	st.header("Head Information")
    	st.json(row.to_dict(orient='index'))
    











    
