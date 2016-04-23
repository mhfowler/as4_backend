from hello_utilities.slack_helper import slack_notify_message


def _log(message, channel_id=None):
    """
    instead of using print, call this function, and then handle behavior based on environment appropriately
    :param message: string to log
    :return: None
    """
    print message
    slack_notify_message(message, channel_id=channel_id)



