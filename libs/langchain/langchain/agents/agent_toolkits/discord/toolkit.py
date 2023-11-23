from typing import Dict, List

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from langchain.tools.discord.prompt import (
    ASSIGN_ROLE_PROMPT,
    CREATE_TEXT_CHANNEL_PROMPT,
    CREATE_VOICE_CHANNEL_PROMPT,
    DELETE_MESSAGE_PROMPT,
    DELETE_TEXT_CHANNEL_PROMPT,
    DELETE_VOICE_CHANNEL_PROMPT,
    EDIT_MESSAGE_PROMPT,
    JOIN_VOICE_CHANNEL_PROMPT,
    KICK_USER_PROMPT,
    LEAVE_VOICE_CHANNEL_PROMPT,
    SEND_MESSAGE_PROMPT,
    SERVER_INFO_PROMPT,
)
from langchain.tools.discord.tool import DiscordAction
from langchain.utilities.discord import DiscordAPIWrapper


class DiscordToolkit(BaseToolkit):
    """Discord Toolkit."""

    tools: List[BaseTool] = []

    @classmethod
    def from_discord_api_wrapper(
        cls, discord_api_wrapper: DiscordAPIWrapper
    ) -> "DiscordToolkit":
        operations: List[Dict] = [
            {
                "mode": "assign_role",
                "name": "Assign Role",
                "description": ASSIGN_ROLE_PROMPT,
            },
            {
                "mode": "kick_user",
                "name": "Kick User",
                "description": KICK_USER_PROMPT,
            },
            {
                "mode": "create_text_channel",
                "name": "Create Text Channel",
                "description": CREATE_TEXT_CHANNEL_PROMPT,
            },
            {
                "mode": "delete_text_channel",
                "name": "Delete Text Channel",
                "description": DELETE_TEXT_CHANNEL_PROMPT,
            },
            {
                "mode": "create_voice_channel",
                "name": "Create Voice Channel",
                "description": CREATE_VOICE_CHANNEL_PROMPT,
            },
            {
                "mode": "join_voice_channel",
                "name": "Join Voice Channel",
                "description": JOIN_VOICE_CHANNEL_PROMPT,
            },
            {
                "mode": "leave_voice_channel",
                "name": "Leave Voice Channel",
                "description": LEAVE_VOICE_CHANNEL_PROMPT,
            },
            {
                "mode": "server_info",
                "name": "Server Info",
                "description": SERVER_INFO_PROMPT,
            },
            {
                "mode": "delete_voice_channel",
                "name": "Delete Voice Channel",
                "description": DELETE_VOICE_CHANNEL_PROMPT,
            },
            {
                "mode": "edit_message",
                "name": "Edit Message",
                "description": EDIT_MESSAGE_PROMPT,
            },
            {
                "mode": "send_message",
                "name": "Send Message",
                "description": SEND_MESSAGE_PROMPT,
            },
            {
                "mode": "delete_message",
                "name": "Delete Messages",
                "description": DELETE_MESSAGE_PROMPT,
            },
            # Add more operations as needed
        ]
        tools = [
            DiscordAction(
                name=action["name"],
                description=action["description"],
                mode=action["mode"],
                api_wrapper=discord_api_wrapper,
            )
            for action in operations
        ]
        return cls(tools=tools)

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools
