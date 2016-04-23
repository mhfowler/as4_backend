from hello_utilities.slack_helper import slack_notify_message
from hello_settings import VERBOSE_LOG


def _log(message, channel_id=None, debug=False):
    """
    instead of using print, call this function, and then handle behavior based on environment appropriately
    :param message: string to log
    :return: None
    """
    print message
    if not debug or debug and VERBOSE_LOG:
        slack_notify_message(message, channel_id=channel_id)



