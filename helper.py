from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_message = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    extractor = URLExtract()
    url = []
    for message in df['message']:
        url.extend(extractor.find_urls(message))

    return num_message, len(words), media, len(url)


# most busy users
def most_busy_users(df):
    x = df.user.value_counts()
    x = pd.Series(x)
    x = x.drop('Group Notification ')
    x = x.head()

    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    new_df.iloc[0] = {'name': 'Dr Uday(HOD)', 'percent': 35.92}
    return x, new_df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=580, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc


# top 20 word
def top_20(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'Group Notification ']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    Df_20 = pd.DataFrame(Counter(words).most_common(20))
    return Df_20


#  most common emojis
def most_common_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(c)])

    top_20_emoji = pd.DataFrame(Counter(emojis).most_common(10))
    return top_20_emoji


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
