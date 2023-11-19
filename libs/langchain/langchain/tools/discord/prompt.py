# flake8: noqa
ASSIGN_ROLE_PROMPT = """
This tool is used to assign a role to a user in a Discord server. Provide the username and role name.
Usage example:
- Username: john_doe
- Role Name: Moderator
"""

KICK_USER_PROMPT = """
This tool is used to kick a user from a Discord server. Provide the username of the user to be kicked.
Usage example:
- Username: unwanted_user
"""

CREATE_TEXT_CHANNEL_PROMPT = """
This tool is used to create a text channel in a Discord server. Provide the name of the text channel and an optional list of usernames to limit visibility.
Usage example:
- Channel Name: general_chat
- Optional Usernames (comma-separated): user1, user2
"""

DELETE_TEXT_CHANNEL_PROMPT = """
This tool is used to delete a text channel in a Discord server. Provide the name of the text channel.
Usage example:
- Channel Name: obsolete_channel
"""

CREATE_VOICE_CHANNEL_PROMPT = """
This tool is used to create a voice channel in a Discord server. Provide the name of the voice channel and an optional list of usernames to limit visibility.
Usage example:
- Channel Name: new_voice_channel
- Optional Usernames (comma-separated): user1, user2
"""

DELETE_VOICE_CHANNEL_PROMPT = """
This tool is used to delete a voice channel in a Discord server. Provide the name of the voice channel.
Usage example:
- Channel Name: obsolete_voice_channel
"""

JOIN_VOICE_CHANNEL_PROMPT = """
This tool is used to join a voice channel in a Discord server. Provide the name of the voice channel.
Usage example:
- Channel Name: voice_chat
"""

LEAVE_VOICE_CHANNEL_PROMPT = """
This tool is used to leave the current voice channel in a Discord server.
"""

SERVER_INFO_PROMPT = """
This tool is used to display information about the Discord server.
"""

EDIT_MESSAGE_PROMPT = """
This tool is used to edit a message in a Discord server. Provide the channel name, message ID, and the new content.
Usage example:
- Channel Name: general
- Message ID: 987654321098765432
- New Content: Updated message content
"""

SEND_MESSAGE_PROMPT = """
This tool is used to send a message to a Discord server. Provide the channel name and the content of the message.
Usage example:
- Channel Name: general
- Message Content: Hello, this is a test message!
"""

DELETE_MESSAGE_PROMPT = """
This tool is used to delete a specific message in a Discord server. Provide the channel name and the message ID.
Usage example:
- Channel Name: general
- Message ID: 987654321098765432
"""

# Add more prompts for other Discord tools if needed