import streamlit as st
import matplotlib.pyplot as plt
import helper
import preprocess
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
    data = bytes_data.decode("utf-8")

    # st.text(data)
    df = preprocess.preprosess(data)

    # st.dataframe(df)
    #   unique user
    user_list = df['user'].unique().tolist()
    user_list.remove("Group Notification ")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt ", user_list)
    if st.sidebar.button("Show Analysis"):

        num_message, num_words, num_media, num_url = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media  Shared")
            st.title(num_media)
        with col4:
            st.header("URL shared")
            st.title(num_url)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the most busy user in the chat
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WorldCloud
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.title("WordCloud Of Chat")
        st.pyplot(fig)
        # top 20 word
        df_20 = helper.top_20(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(df_20[0], df_20[1])
        plt.xticks(rotation='vertical')

        st.title("Most Common Words")
        st.pyplot(fig)

        # top 20 emoji
        st.title("Most Common Emoji")
        top_20_emoji = helper.most_common_emoji(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(top_20_emoji)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(top_20_emoji[1], labels=top_20_emoji[0], autopct="%0.2f")
            st.pyplot(fig)
