import re
import pandas

def read_whatsapp_chat(file_path: str) -> pandas.DataFrame:
    e2e_msg = "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more."
    media_msg = "<Media omitted>"
    # email_msg = regx
    # url_msg = regx
    edited_msg = "<This message was edited>"
    deleted_msg = "You deleted this message"
    null_msg = "null"
    created_group_msg = "created group"
    added_u_msg = "added you"
    # tagging_pattern = regx

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
            # regx check: not re.search(email, line) and
            # regx check: not re.search(url, line) and
            edited_msg not in line and
            deleted_msg not in line and
            null_msg != line.split(" ")[-1] and
            created_group_msg not in line and
            added_u_msg not in line
        ):
            line = line.replace(edited_msg, "").strip()
            # line = re.sub(tagging_pattern, "", line).strip()
            filtered_lines.append(line)
    
    # 3. regex to match whatsapp messages
    # 4. Create a dataframe
    # 5. Convert timestamps to datatime object
    # 6. return dataframes
