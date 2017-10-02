from actions import votable_actions


def get_referendum(referendum_id):
    pass


def referendum_exists(referendum_id):
    pass


def get_server_id_for_referendum(referendum_id):
    pass


def is_user_enfranchised(user_id, server_id):
    return True  # TODO


def get_referendum_func(referendum_func_name):
    return votable_actions[referendum_func_name]


def register_referendum(referendum_func, referendum_args):
    pass
