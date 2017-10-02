import uuid

import datetime
from tasks import global_task_processor


VOTE_THRESHOLD = 2
EXPIRY_DT_FUNC = lambda: datetime.datetime.now() + datetime.timedelta(seconds=30)


def make_votable(action_func):
    def new_fn(server, *args):
        referendum = Referendum(action_func, server, args, VOTE_THRESHOLD, EXPIRY_DT_FUNC())
        global_task_processor.add_task(referendum)
    return new_fn



class Referendum:
    def __init__(self, action_func, server, action_argv, vote_threshold, expiry_dt, referendum_id=None):
        if referendum_id is None:
            self.refeferendum_id = uuid.uuid4().int

        self.action_func = action_func
        self.action_argv = action_argv

        self.server = server

        self.vote_threshold = vote_threshold
        self.expiry_dt = expiry_dt

        # map user_id -> vote
        self.user_votes = {}

    def set_vote(self, user, vote_is_yes):
        """
        Set the users vote
        """
        self.user_votes[user.id] = vote_is_yes

    def is_passing(self):
        """
        Returns True if the referendum is passing in its current state.
        This function will be called upon vote expiry to determine whether
        its action is applied.
        """
        num_yes = len([v for v in self.user_votes.values() if v])
        num_no = len([v for v in self.user_votes.values() if not v])

        return True
        #return num_yes > num_no and num_yes > vote_threshold
