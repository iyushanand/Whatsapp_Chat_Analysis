import streamlit as st
from matplotlib import pyplot as plt

import preprocessor
import helper
from helper import most_busy_users
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer") # creates a side bar on the webpage with the title
# refer to the document online for streamlit to upload the file (google)
uploaded_files = st.sidebar.file_uploader("Choose a file")
if uploaded_files is not None:
    bytes_data = uploaded_files.getvalue()
    data = bytes_data.decode("utf-8")  # stream to string conversion -- important
   #st.text(data) # now you can see the data on the screen
    df = preprocessor.preprocessor(data) # called preprocess function and passed our data here
    # now this will show as a dataframe
    #st.dataframe(df) # displays dataframe

    # fetch unique users
    user_list = df['user'].unique().tolist() # fetches all the unique users of the data
     # fetches all the unique users of the data

    # safely remove "group_notification" if present
    if "group_notification" in user_list: # error that persisted
        user_list.remove("group_notification")

    user_list.sort()  # sorted in ascending order
    user_list.insert(0, "Overall")  # does group level analysis , placed at 0th position
    # removes the group notification user to select
    user_list.sort() # sorted in ascending order
    user_list.insert(0,"Overall") # does group level analysis , placed at 0th position

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis:"):
        # Stats Area --> add everytime you are doing
        num_messages,words,num_links = helper.fetch_stats(selected_user,df)  # will store the num of messages
        st.title("Top Statistics")
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

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        # plotting timeline bar graph
        if not timeline.empty:
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')  # labels at x axis rotates
            st.pyplot(fig)
        else:
            st.write("Not enough data for Monthly Timeline.")

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        # plotting timeline bar graph
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['onlydate'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')  # labels at x axis rotates
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Heatmap --> error occured for singl echat so use if else
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heat_map(selected_user, df)
        if not user_heatmap.empty:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)
        else:
            st.write("Not enough data to  display heatmap.")

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
    if df_wc: # for individual data
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    else:
        st.write("Not enough data for Word Cloud.")

    # most common words
    most_common_df = helper.most_common_words(selected_user,df)

    # st.dataframe(most_common_df) # prints a dataframe of above variable that has value
    # removing above dataframe and plotting as a graph
    if not most_common_df.empty:
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)  # to display on streamlit interface
    else:
        st.write("Not enough data for Word Cloud.")

    # emoji analysis
    emoji_df = helper.emoji_helper(selected_user,df)# stored under the same variable name for no confusion
    st.title("Emoji Analysis")

    if not emoji_df.empty:
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df) # prints dataframe in col1
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f") # prints the top 5 pie charts in col2
    else:
        st.write("Not enough data for Emoji Analysis.")
