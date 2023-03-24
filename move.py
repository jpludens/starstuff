class Move(object):
    # TODO: This should not require an actor.
    def __init__(self, actor, action, target=None, choice=None):
        self.actor = actor
        self.action = action
        self.target = target
        self.choice = choice
