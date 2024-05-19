import requests
import env_utils

class JSON:
    pass

SLACK_BOT_OAUTH_TOKEN = env_utils.config('SLACK_BOT_OAUTH_TOKEN', default=None, cast=str)


def send_message_from_slackbot_to_user(message :str, channel_id :str | None = None, user_id :str | None = None, thread_timestamp : str | None = None) -> JSON:
    url= "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {SLACK_BOT_OAUTH_TOKEN}",
        "Accept":"application/json"
    }

    if user_id is not None:
        message = f"<@{user_id}> {message}"

    data = {
        "channel" :f"{channel_id}",
        "text": f"{message}".strip()
    }

    if thread_timestamp is not None:
        #official docs of slack say we need thread-ts argument in the returned json
        data["thread_ts"] = thread_timestamp

    return requests.post(url, json=data, headers=headers)
