class Move(object):
    def __init__(self, actor, action, target=None):
        self.actor = actor
        self.action = action
        self.target = target
