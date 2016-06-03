#!/usr/bin/env python3
#TODO Maybe notification class


from slacker import Slacker


def notify_slack():
    """
    Slack notification
    """

    APT_TOKEN = "token"

    ICON = {
        'INFO', ':page_with_curl',
        'WARN', ':warning:',
        'ERROR', ':bangbang:',
        '*', ':slack:'
    }

    slack = Slacker(API_TOKEN)
    slack.chat.post_message('#channel', 'Message')


def is_valid_url(url):
    """
    Test if passed url is valid
    """

    return True
