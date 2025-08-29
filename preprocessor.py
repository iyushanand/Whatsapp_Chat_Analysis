# making of a function that takes data and provide dataframe we need
import pandas as pd # preprocessor
import re
def preprocessor(data):  # copy pasting from the jupyter notebook we have
    pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}:\d{2}(?:\s|\u202F|\u00A0)?[AP]M)\]\s~(?:\s|\u202F|\u00A0)?(.*)'
    matches = re.findall(pattern, data, flags=re.MULTILINE)
    df = pd.DataFrame(matches, columns=["date", "user_messages"])
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%y, %I:%M:%S %p")

    users = []
    messages = []

    for msg in df['user_messages']:
        # Normal messages will have "User: Message"
        if re.search(r".+?:", msg):
            split_msg = msg.split(": ", 1)
            user = split_msg[0]
            message = split_msg[1] if len(split_msg) > 1 else ""

            # If it's a system notification, override user as group_notification
            if "joined using this group's invite link" in message or \
                "pinned a message" in message or\
                "Your security code with" in message or \
                    "created this group" in message or \
                    "changed this group's icon" in message or \
                    "added" in message:
                users.append("group_notification")
                messages.append(message.strip())
            else:
                users.append(user.strip())
                messages.append(message.strip())
        else:
            # If there's no ":", treat as system notification
            users.append("group_notification")
            messages.append(msg.strip())

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df # the main thing to display all the values



