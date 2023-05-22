class GitHubUserException(Exception):
    pass


class ProjectNotFoundError(Exception):
    pass


class RateLimitExceededError(Exception):
    pass


class NoMoreTokensError(Exception):
    pass


class EmptyQueueError(Exception):
    pass


class ExtractError(Exception):
    pass


class LoadError(Exception):
    pass
