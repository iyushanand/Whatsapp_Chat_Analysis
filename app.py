import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

import preprocessor
import helper
from helper import most_busy_users

st.sidebar.title("Whatsapp Chat Analyzer") # creates a side bar on the webpage with the title
# refer to the document online for streamlit to upload the file (google)
uploaded_files = st.sidebar.file_uploader("Choose a file")
if uploaded_files is not None:
    bytes_data = uploaded_files.getvalue()
    data = bytes_data.decode("utf-8")  # stream to string conversion -- important
   #st.text(data) # now you can see the data on the screen
    df = preprocessor.preprocessor(data) # called preprocess function and passed our data here
    # now this will show as a dataframe
    st.dataframe(df) # displays dataframe

    # fetch unique users
    user_list = df['user'].unique().tolist() # fetches all the unique users of the data
    user_list.remove('group_notification') # removes the group notification user to select
    user_list.sort() # sorted in ascending order
    user_list.insert(0,"Overall") # does group level analysis , placed at 0th position

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis:"):
        # Stats Area --> add everytime you are doing
        num_messages,words,num_links = helper.fetch_stats(selected_user,df)  # will store the num of messages

        col1,col2,col3 = st.columns(3) # create columns and heading

        with col1: # syntax to name the column header and title
            st.header("Total Messages") # creates special place for total message
            st.title(num_messages) # displays the number below it

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Links Shared")
            st.title(num_links)

        # finding the busiest users in the group
        if selected_user == 'Overall':
            col1,col2 = st.columns(2) # making two more columns
            # will divide in two parts , 1-->bar chart(top5) , 2--> percentage
            new_df , fig = most_busy_users(df) # pass the dataframe here`, renmaed new_df to match the dataframe
            with col1 : # the order must be the same , as shown in fig,new_df
                st.header("Most Busiest Users")
                st.pyplot (fig) # returns the figure here
            with col2:
                st.header("Activity Percentage")
                st.dataframe(new_df)

    # Wordcloud
    df_wc = helper.create_wordcloud(selected_user,df) # generate the wordcloud created in helper
    # plot the wordcloud
    st.title("Word Cloud")
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)