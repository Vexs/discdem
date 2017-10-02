import asyncio
from client import client  # TODO
import logging

import store
import respond





@client.event
async def on_message(message):
    logging.warning('Recieved message: {}'.format(message.content))
    if message.content.startswith('!vote'):
        await handle_vote_message(message)
    elif message.content.startswith('!info'):
        await handle_info_message(message)
    elif message.content.startswith('!'):
        await handle_create_referendum_message(message)


async def handle_vote_message(message):
    message_args = message.content.split()

    # ensure message is well formed
    if len(message_args) != 3:
        await respond.invalid_command(message)
        return

    # ensure referendum_id exists
    referendum_id = message_args[1]
    if not store.referendum_exists(referendum_id):
        await respond.invalid_referendum(message)
        return

    # ensure user is enfranchised on the server the referendum_id applys to
    if not store.is_user_enfranchised(message.author, referendum_id):
        await respond.not_enfranchised(message)
        return

    vote_str = message_args[2]
    if vote_str.lower() not in ('yes', 'no'):
        await respond.invalid_command(message)
        return

    vote_is_yes = vote_str.lower() == 'yes'

    # apply vote
    referendum = store.get_referendum(referendum_id)
    referendum.set_vote(message.author, vote_is_yes)

    # signify vote parsed with a checkmark emoji
    # TODO


async def handle_info_message(message):
    message_args = message.content.split()

    # ensure message is well formed
    if len(message_args) != 2:
        await respond.invalid_command(message)
        return

    # ensure referendum_id exists
    referendum_id = message_args[1]
    if not store.referendum_exists(referendum_id):
        await respond.invalid_referendum(message)
        return

    # ensure user is enfranchised on the server the referendum_id applys to
    server_id = store.get_server_id_for_referendum(referendum_id)
    if not store.is_user_enfranchised(message.author.id, server_id):
        await respond.not_enfranchised(message)
        return

    # respond with vote info
    referendum = store.get_referendum(referendum_id)
    info_str = 'referendum id: {}, action: {}({}), referendum expiry: {} (in {} minutes)'.format(
        referendum.referendum_id,
        referendum.action_fn,
        ', '.join(map(repr, referendum.action_argv)),
        referendum.expiry_dt.strftime("%b %d %Y %H:%M:%S", time.gmtime(t)),
        'a few (TODO)',
    )
    await respond.info(message, info_str)


async def handle_create_referendum_message(message):
    message_params = message.content.split()
    referendum_fn_name = message_params[0][1:]  # remove the ! prefix
    referendum_args = message_params[1:]

    # ensure referendum command was sent in a server
    if message.server is None:
        await respond.must_be_in_server(message)
    
    # ensure user is enfranchised
    if not store.is_user_enfranchised(message.author.id, message.server.id):
        await respond.not_enfranchised(message)
        return

    # ensure referendum function is valid
    referendum_func = store.get_referendum_func(referendum_fn_name)
    if referendum_func is None:
        await respond.invalid_referendum_function(message)
    
    # TODO: ensure function has valid params

    # ensure function performs valid action
    # TODO: no functions written so far need this, so its not yet necessary

    # create referendum
    # TODO: dynamic vote_threshold, expiry_dt offset, not preset
    referendum_func(message.server, *referendum_args)
    store.register_referendum(referendum_func, referendum_args)
