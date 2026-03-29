# custom base exception so we can catch all our app errors together
class HackHubError(Exception):
    """Base class for exceptions in this module."""
    pass

# specific error for when something goes wrong with a contest (like dates or status)
class ContestError(HackHubError):
    """Exception raised for errors in the contest management."""
    def __init__(self, message="A contest-related error occurred"):
        self.message = message
        super().__init__(self.message)

# error for submission issues, like file type or weird upload errors
class SubmissionError(HackHubError):
    """Exception raised for errors in the submission process."""
    def __init__(self, message="A submission-related error occurred"):
        self.message = message
        super().__init__(self.message)

# raised when something breaks during judge scoring
class ScoringError(HackHubError):
    """Exception raised for errors in the scoring process."""
    def __init__(self, message="A scoring-related error occurred"):
        self.message = message
        super().__init__(self.message)

# simple error for when a user tries to touch things they shouldn't
class PermissionDeniedError(HackHubError):
    """Exception raised when a user lacks required permissions."""
    def __init__(self, message="You do not have permission to perform this action"):
        self.message = message
        super().__init__(self.message)
