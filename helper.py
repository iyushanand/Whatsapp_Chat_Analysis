# function created that provides the statistics when given a user
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
    x = df['user'].value_counts().head(6)[1:]
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

    if selected_user!='Overall': # if this is not overall then it df will be changed else it will be same in the case of overall
        df = df[df['user'] == selected_user]

    wc = WordCloud(width = 500,height=500,min_font_size=10,background_color='white').generate(selected_user) # wc is the object made
    df_wc = wc.generate(df['message'].str.cat(sep=' ')) # this object create the image
    return df_wc




