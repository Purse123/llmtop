import re
import pandas

def read_whatsapp_chat(file_path: str) -> pandas.DataFrame:
    e2e_msg = "Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more."
    media_msg = "<Media omitted>"
    email_msg = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'    # raw string r' '
    url_msg = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    edited_msg = "<This message was edited>"
    deleted_msg = "You deleted this message"
    null_msg = "null"
    created_group_msg = "created group"
    added_u_msg = "added you"
    tagging_pattern = r'@[\w]+'

    #
    # TODOS
    #
    
    # 1. read the chat file
    with open(file_path, 'r', encoding='utf=8') as f:
        lines = f.readlines()
        
    # 2. apply filters to remove unwanted lines
    filtered_lines = []
    for line in lines:
        if (
            e2e_msg not in line and
            media_msg not in line and
            not re.search(email_msg, line) and
            not re.search(url_msg, line) and
            edited_msg not in line and
            deleted_msg not in line and
            null_msg != line.split(" ")[-1] and
            created_group_msg not in line and
            added_u_msg not in line
        ):
            # Hello! <This message was edited>" to "Hello!"
            line = line.replace(edited_msg, "").strip()
            # "hello @purse." to "hello."
            line = re.sub(tagging_pattern, "", line).strip()
            filtered_lines.append(line)

    # 3. regex to match whatsapp messages
    # date, time_AM/PM - person: msg
    pattern = r'(\d{2}/\d{2}/\d{2,4}, \d{1,2}:\d{2}(?:\s?[ap]m)?) - (.*?): (.*?)(?=\n\d{2}/\d{2}/\d{2,4}, \d{1,2}:\\d{2}(?:\\s?[ap]m)? -|$)'
    content = '\n'.join(filtered_lines)
    messages = re.findall(pattern, content, re.DOTALL)
    
    # 4. Create a dataframe
    print("Filtered lines:")
    print(filtered_lines)
    df = pandas.DataFrame(messages, columns=['timestamp', 'sender', 'message'])
    print("Final DataFrame:")
    print(df)
    
    # 5. Convert timestamps to datatime object
    timestamps = []
    for timestamp in df['timestamp']:
        try:
            timestamp = pd.to_datetime(timestamp, format='mixed', dayfirst=True)
        except Exception as e:
            print(f"Error parsing timestamp '{timestamp}': {e}")
            timestamp = pd.NaT
        timestamps.append(timestamp)

    # 6. return dataframes
    df['timestamp'] = timestamps
    return df

d = read_whatsapp_chat("WhatsApp.txt")
print(d)
