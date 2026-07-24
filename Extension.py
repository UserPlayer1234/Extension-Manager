from datetime import datetime
import itertools

class Extension:
    """Class for tracking an extension request."""
    counter = itertools.count()

    def __init__(self, email, assignment, deadline, reason, date_submitted):
        self.email: str = email
        self.assignment: str = assignment
        self.deadline: datetime = deadline
        self.reason: str = reason
        self.date_submitted: datetime = date_submitted
        self.approved: bool = False
        self.id: int = next(Extension.counter)

    def __repr__(self):
        return f"{self.id} : {self.email} | {self.assignment} | {self.reason}"

    