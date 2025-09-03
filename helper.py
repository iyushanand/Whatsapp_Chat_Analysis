# function created that provides the statistics when given a user
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user,df): # will fetch stats of the selected user
    if selected_user == 'Overall':
        num_messages =  df.shape[0] # will return the number of messages, total number of messages
        words = []  # these three lines will fetch the number of words
        for message in df['message']:
            words.extend(message.split())
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))

    else : # for selected user
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0] # throws total number of messages from the user  # go to jupyter notebook for the same
        words = []  # these three lines will fetch the number of words
        for message in new_df['message']:
            words.extend(message.split())
        # fetch number of media messages
        # df[df['message'] == '<Media omitted'\n]   # cannot determine as whatsapp export has no such content

        # calculating total number of link shared --> can do from the above process , or
        # use library url extract ---> terminal pip install
        links = []
        for message in new_df['message']:
            links.extend(extract.find_urls(message))  # extract is the object created above

    return num_messages, len(words), len(links) # this code can become short 1;00;00

def most_busy_users(df):
    x = df['user'].value_counts().head(6)
    if len(x) > 1:
        x = x[1:]  # exclude system messages (if multiple users)
    name = x.index  # prints the name
    count = x.values  # prints the values
    # printing bar chart
    fig, ax = plt.subplots()
    ax.bar(name, count, color='red')
    ax.set_xlabel("Users")
    ax.set_ylabel("Message Count")
    ax.set_title("Top 5 Most Active Users")
    plt.xticks(rotation='vertical')
    # average message by each individual
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    # Display the plot in Streamlit , and return the activity percentage
    return new_df , fig


def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user!='Overall': # if this is not overall then it df will be changed else it will be same in the case of overall
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    def remove_stop_word(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    if selected_user!='Overall': # if this is not overall then it df will be changed else it will be same in the case of overall
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')  # wc is the object made
    if temp.shape[0] > 0:
        temp['message'] = temp['message'].apply(remove_stop_word)
        df_wc = wc.generate(temp['message'].astype(str).str.cat(sep=" ")) # generates image
        return df_wc  # our wordcloud will not have hinglish stop words
    else:
        return None

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user!='Overall':

        df = df[df['user'] == selected_user]
         # 1 . remove the group messages
    temp = df[df['user'] != 'group_notification'] # can do this filtering above also
    words = []

    for message in temp['message']:  # will use this dataframe
        for word in message.lower().split():  # split necessary to get word by word
            if word not in stop_words:  # if the word is not in the stop word file then only append to the word
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20)) # now it will print the non stopping words (top20)
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])  # if any emoji matches then put in emojis list

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))) # changed to dataframe and most common also found
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()  # messages monthwise, total
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))  # did this in our format to plot the chart

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('onlydate').count()['message'].reset_index()  # count message on a daily basis
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heat_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc = 'count').fillna(0)
    return user_heatmap