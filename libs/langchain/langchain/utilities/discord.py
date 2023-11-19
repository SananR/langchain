import discord
from discord.ext import commands
from langchain.pydantic_v1 import BaseModel, Extra, root_validator
from langchain.utils import get_from_dict_or_env

class DiscordAPIWrapper(BaseModel):
    """Wrapper for Discord API."""

    def __init__(self, bot):
        self.bot = bot

    @root_validator()
    def validate_environment(cls, values: dict) -> dict:
        """Validate that the bot token exists in the environment."""
        bot_token = get_from_dict_or_env(values, "bot_token", "DISCORD_BOT_TOKEN")
        guild_id = get_from_dict_or_env(values, "guild_id", "DISCORD_SERVER_ID")
        role_name = get_from_dict_or_env(values, "role_name", "DISCORD_ROLE_NAME")
        channel_id = get_from_dict_or_env(values, "channel_id", "DISCORD_CHANNEL_ID", default=None)

        values["bot_token"] = bot_token
        values["guild_id"] = guild_id
        values["role_name"] = role_name
        values["channel_id"] = channel_id

        return values

    async def initialize_discord_bot(self, values: dict) -> commands.Bot:
        """Initialize and run the Discord bot."""
        bot = commands.Bot(command_prefix="!")  # Set your desired command prefix

        @bot.event
        async def on_ready():
            print(f'We have logged in as {bot.user}')

        await bot.start(values["bot_token"])  # Use await with bot.start()
        return bot

    @commands.command(name="assign_role")
    def assign_role(self, ctx, user_name: str, role_name: str):
        """Assign a role to a user."""
        member = self.find_user_by_name(ctx, user_name)
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if not member:
            return f'User {user_name} not found in this server.'

        if not role:
            return f'Role {role_name} not found in this server.'

        if role.position >= ctx.author.top_role.position:
            return f'You do not have permission to assign the {role_name} role.'

        # Add the role to the user
        member.add_roles(role)
        return f'{member.display_name} now has the {role_name} role.'

    @commands.command(name="kick_user")
    def kick_user(self, ctx, user_name: str):
        """Kick a user."""
        member = self.find_user_by_name(ctx, user_name)

        if not member:
            return f'User {user_name} not found in this server.'

        if member == ctx.author:
            return 'You cannot kick yourself.'

        try:
            # Kick the user
            member.kick()
            return f'{member.display_name} has been kicked.'
        except discord.Forbidden:
            return 'I do not have the necessary permissions to kick members.'

    def find_user_by_name(self, ctx, user_name: str):
        """Find a Discord user by name."""
        # Check if the provided username is not empty
        if not user_name:
            return None

        # Check if the provided username is a valid string
        if not isinstance(user_name, str):
            return None

        # Try to find the user in the server's member list
        user = discord.utils.get(ctx.guild.members, name=user_name)

        # Check if the user is not found
        if not user:
            return None

        return user

    @commands.command(name="create_text_channel")
    async def create_text_channel(self, ctx, channel_name: str, *usernames: str):
        """Create a text channel."""
        if usernames:
            users = [discord.utils.get(ctx.guild.members, name=username) for username in usernames]
            users = [user for user in users if user is not None]  # Remove None values

            # Check if at least one valid user is provided
            if not users:
                return 'No valid users found.'

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            }

            for user in users:
                overwrites[user] = discord.PermissionOverwrite(read_messages=True)

            try:
                channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
                return f'Text channel {channel_name} created with limited access.'
            except discord.Forbidden:
                return 'I do not have the necessary permissions to create text channels.'

        else:
            try:
                await ctx.guild.create_text_channel(channel_name)
                return f'Text channel {channel_name} created.'
            except discord.Forbidden:
                return 'I do not have the necessary permissions to create text channels.'
    @commands.command(name="delete_text_channel")
    def delete_text_channel(self, ctx, channel_name: str):
        """Delete a text channel."""
        if not ctx.author.guild_permissions.manage_channels:
            return 'You do not have permission to delete text channels.'

        channel = discord.utils.get(ctx.guild.channels, name=channel_name, type=discord.ChannelType.text)
        if not channel:
            return f'Text channel {channel_name} not found.'

        try:
            channel.delete()
            return f'Text channel {channel_name} deleted.'
        except discord.Forbidden:
            return 'I do not have the necessary permissions to delete text channels.'

    @commands.command(name="create_voice_channel")
    async def create_voice_channel(self, ctx, channel_name: str, *usernames: str):
        """Create a voice channel."""
        if not ctx.author.guild_permissions.manage_channels:
            return 'You do not have permission to create voice channels.'

        # Check if usernames were provided
        if usernames:
            users = [discord.utils.get(ctx.guild.members, name=username) for username in usernames]
            users = [user for user in users if user is not None]  # Remove None values

            # Check if at least one valid user is provided
            if not users:
                return 'No valid users found.'

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
                ctx.guild.me: discord.PermissionOverwrite(connect=True)
            }

            for user in users:
                overwrites[user] = discord.PermissionOverwrite(connect=True)

            try:
                channel = await ctx.guild.create_voice_channel(channel_name, overwrites=overwrites)
                return f'Voice channel {channel_name} created with limited access.'
            except discord.Forbidden:
                return 'I do not have the necessary permissions to create voice channels.'

        else:
            try:
                await ctx.guild.create_voice_channel(channel_name)
                return f'Voice channel {channel_name} created.'
            except discord.Forbidden:
                return 'I do not have the necessary permissions to create voice channels.'
    @commands.command(name="delete_voice_channel")
    def delete_voice_channel(self, ctx, channel_name: str = None):
        """Delete a voice channel."""
        if not ctx.author.guild_permissions.manage_channels:
            return 'You do not have permission to delete voice channels.'

        channel = discord.utils.get(ctx.guild.channels, name=channel_name, type=discord.ChannelType.voice)
        if not channel:
            return f'Voice channel {channel_name} not found.'

        try:
            channel.delete()
            return f'Voice channel {channel_name} deleted.'
        except discord.Forbidden:
            return 'I do not have the necessary permissions to delete voice channels.'

    @commands.command(name="join_voice_channel")
    def join_voice_channel(self, ctx, channel_name: str = None):
        """Join a voice channel."""
        if not ctx.author.guild_permissions.connect:
            return 'You do not have permission to join voice channels.'

        channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
        if not channel:
            return f'Voice channel {channel_name} not found.'

        try:
            voice_channel = channel.connect()
            return f'Joined voice channel {channel_name}'
        except discord.Forbidden:
            return 'I do not have the necessary permissions to join voice channels.'

    @commands.command(name="leave_voice_channel")
    def leave_voice_channel(self, ctx):
        """Leave the current voice channel."""
        if ctx.voice_client:
            ctx.voice_client.disconnect()
            return 'Left the voice channel'
        else:
            return 'Not connected to a voice channel'

    @commands.command(name="server_info")
    def server_info(self, ctx):
        """Display server information."""
        if not ctx.author.guild_permissions.view_audit_log:
            return 'You do not have permission to view server information.'

        guild = ctx.guild
        info = f'Server Name: {guild.name}\nServer ID: {guild.id}\nMember Count: {guild.member_count}'
        return info

    @commands.command(name="send_message")
    async def send_message(self, ctx, content: str, channel_name: str = None):
        """Send a message to a channel."""
        if channel_name:
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            if not channel:
                return f'Channel {channel_name} not found in this server.'
        else:
            # Send to the general channel if no channel is specified
            channel = ctx.guild.get_channel(ctx.guild.id)

        try:
            message = await channel.send(content)
            return f'Message sent: {message.content}'
        except discord.Forbidden:
            return 'I do not have the necessary permissions to send messages in that channel.'

    @commands.command(name="edit_message")
    async def edit_message(self, ctx, new_content: str, channel_name: str = None):
        """Edit the last message by the user in a channel."""
        if channel_name:
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            if not channel:
                return f'Channel {channel_name} not found in this server.'
            channel_id = channel.id
        else:
            # Find the general channel by name (modify as needed)
            general_channel = discord.utils.get(ctx.guild.channels, name="general")
            if not general_channel:
                return 'General channel not found in this server.'
            channel_id = general_channel.id

        try:
            # Get the last message by the user in the specified channel
            message = discord.utils.get(await channel.history().flatten(), author=ctx.author)
            if not message:
                return f'No message found to edit in {channel.name} by {ctx.author.display_name}.'

            message.edit(content=new_content)
            return f'Message edited: {message.content}'
        except discord.Forbidden:
            return 'I do not have the necessary permissions to edit messages in that channel.'
    
    @commands.command(name="delete_message")
    async def delete_message(self, ctx, channel_name: str = None):
        """Delete the last message by the user in a channel."""
        if channel_name:
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            if not channel:
                return f'Channel {channel_name} not found in this server.'
            channel_id = channel.id
        else:
            # Find the general channel by name (modify as needed)
            general_channel = discord.utils.get(ctx.guild.channels, name="general")
            if not general_channel:
                return 'General channel not found in this server.'
            channel_id = general_channel.id

        try:
            # Get the last message by the user in the specified channel
            message = discord.utils.get(await channel.history().flatten(), author=ctx.author)
            if not message:
                return f'No message found to delete in {channel.name} by {ctx.author.display_name}.'

            message.delete()
            return f'Message deleted: {message.content}'
        except discord.Forbidden:
            return 'I do not have the necessary permissions to delete messages in that channel.'


    def run(self, mode: str, query: list, ctx: DiscordContext) -> str:
        command = self.bot.get_command(mode)
        if command:
            return self.bot.invoke(command, ctx, *query).result()
        else:
            raise ValueError("Invalid command: " + mode)
        
def setup(bot):
    bot.add_cog(DiscordAPIWrapper(bot))