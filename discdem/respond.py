from client import client


async def invalid_command(message):
    await client.send_message(message.channel, 'Invalid command, noob')


async def invalid_referendum(message):
    await client.send_message(message.channel, 'Invalid referendum params, noob')


async def not_enfranchised(message):
    await client.send_message(message.channel, 'You\'re not enfranchised, noob')


async def must_be_in_server(message):
    await client.send_message(message.channel, 'You\'re not in the server, noob')


async def invalid_referendum_function(message):
    await client.send_message(message.channel, 'Invalid referendum function, noob')


async def info(message, info_str):
    await client.send_message(message.channel, '{}: {}'.format(message.author.mention, info_str))
