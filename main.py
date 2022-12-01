# This program exports channel subscribers from Telegram

from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import pandas as pd

# Variables

# Get it: https://my.telegram.org/apps
api_id = 0
api_hash = ''
allParticipants = []
# Keys are used to find users
queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
            'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш',
            'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
            'ґ', 'є', 'і', 'ї',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            '_', '.', '*', '@', '&']
firstNames = []
lastNames = []
usernames = []
ids = []
links = []
client = TelegramClient('Export session', api_id, api_hash)


# Function: Telegram login
def login():
    try:
        client.start()
    except Exception as e:
        # Red color
        print("\u001b[31m", end="")
        print(e)
        # Yellow color
        print("\u001b[33m", end="")
        login()


# Function: Asynchronous request to telegrams to get participants
# Telegram limit for channels: 200 users per request
async def makeRequest():
    try:
        offset: int = 0
        limit = 10000
        participants = await client(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(key), offset, limit,
            hash=0
        ))
        if not participants.users:
            return
        for participant in participants.users:
            try:
                if not participant in allParticipants:
                    allParticipants.append(participant)
            except:
                pass
        offset += len(participants.users)
        print("\u001b[33m" + "/", end="")
    except Exception as e2:
        # Red color
        print("\u001b[31m", end="")
        print(e2)
        # Yellow color
        print("\u001b[33m", end="")


# Yellow color
print("\u001b[33m", end="")

# Telegram login
login()

# Message to user
print("Remember that you must be a channel or group administrator to export subscribers!")
channel = input("Enter channel name: ")
print("\u001b[33m" + "Export participants from channel: " + channel.upper() + " in progress")

# Export
for key in queryKey:
    with client:
        client.loop.run_until_complete(makeRequest())

# Message to user
print("")
print("\u001b[32m" + "Total: " + str(len(allParticipants)))

# Convert data
for user in allParticipants:
    firstNames.append(user.first_name)
    lastNames.append(user.last_name)
    usernames.append(user.username)
    ids.append(str(user.id))
    if user.username is not None:
        links.append("https://t.me/" + str(user.username))
    else:
        links.append("")
data = {'First name': firstNames,
        'Last name': lastNames,
        'Username': usernames,
        'ID': ids,
        'Links': links}

# Saving data to Excel
fileName = channel.upper() + ' (participants).xlsx'
df = pd.DataFrame(data)
df.to_excel(fileName, index=False)
print("\u001b[32m" + "\033[1m" + "Saving to Excel file successfully." + "\033[0m")
