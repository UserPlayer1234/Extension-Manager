from datetime import datetime
import itertools

class Extension:
    """Class for tracking an extension request."""
    counter = itertools.count()

    def __init__(self, email='N/A', assignment='N/A', deadline='N/A', reason='N/A', date_submitted='N/A'):
        self.email: str = email
        self.assignment: str = assignment
        self.deadline: str = deadline
        self.reason: str = reason
        self.date_submitted: str = date_submitted
        self.approved: bool = False
        self.id: int = next(Extension.counter) if email != 'N/A' else -1

    def __repr__(self):
        return f"{self.id} : {self.approved}"

    def __eq__(self, value):
        if isinstance(value, Extension) and value.id == self.id:
            return True
        return False