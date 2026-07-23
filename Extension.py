from dataclasses import dataclass
from datetime import datetime

@dataclass
class Extension:
    """Class for tracking an extension request."""
    email: str
    assignment: str
    deadline: datetime
    reason: str
    date_submitted: datetime