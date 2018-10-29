class Constraint:
    def is_met(self, data):
        pass

class UniqueConstraint:
    def __init__(self, past_choices):
        self.past_choices = past_choices

    def is_met(self, data):
        return len([choice for choice in self.past_choices if choice is data]) == 0