import discord

from client import client
from referendum import make_votable


@make_votable
async def addchannel(server, channel_name, channel_type_str):
    if channel_type_str == 'text':
        channel_type = discord.ChannelType.text
    else:
        channel_type = discord.ChannelType.voice

    everyone_perms = discord.PermissionOverwrite(read_messages=False)
    my_perms = discord.PermissionOverwrite(read_messages=True)
    everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
    mine = discord.ChannelPermissions(target=server.me, overwrite=my_perms)
    await client.create_channel(server, channel_name, everyone, mine, type=channel_type)



votable_actions = {
    'addchannel': addchannel,
}
