from .base import BaseEntityHelpDesk


class Topic(BaseEntityHelpDesk):
    pass


class Priority(BaseEntityHelpDesk):
    pass


class State(BaseEntityHelpDesk):
    name = None

    def __repr__(self):
        return "<Status %s>" % self.name

