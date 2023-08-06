class BaseReleaserException(Exception):
    """The Base Releaser Exception class.
    """


class RequestError(BaseReleaserException):
    """An error sending the data to Slack.
    """


class ConfigError(BaseReleaserException):
    """An error parsing the config file.
    """
