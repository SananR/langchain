from typing import Optional

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import Field
from langchain.tools.base import BaseTool
from langchain.utilities.discord import DiscordAPIWrapper


class DiscordAction(BaseTool):
    """Tool for interacting with the Discord API."""

    api_wrapper: DiscordAPIWrapper = Field(default_factory=DiscordAPIWrapper)
    mode: str
    name: str = ""
    description: str = ""

    async def _run(
        self,
        instructions: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Discord API to run an operation."""
        return await self.api_wrapper.run(self.mode, instructions)
