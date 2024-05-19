import json
import requests
import env_utils
import msg_client

from typing import Any
from pprint import pprint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

class JSON:
    pass

SLACK_BOT_OAUTH_TOKEN = env_utils.config('SLACK_BOT_OAUTH_TOKEN', default=None, cast=str)


def send_message_from_slackbot_to_user(message :str, channel_id :str | None = None, user_id :str | None = None) -> JSON:
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

    return requests.post(url, json=data, headers=headers)


@csrf_exempt
@require_POST
def slack_events_controller(request):
    json_data = {}
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print(e)
        pass
    data_type = json_data.get('type')
    print(data_type, json_data)
    allowed_data_type = set(
        ["url_verification","event_callback"]
        )


    if data_type not in allowed_data_type:
        return HttpResponse("Not Allowed", status = 400)
    if data_type == "url_verification":
        challenge = json_data.get('challenge')
        if challenge is None:
            return HttpResponse("Not Allowed", status = 400)
        return HttpResponse(challenge, status=200)

    elif data_type == "event_callback":
        event :dict[Any]= json_data.get('event') or {}
        pprint(event)
        msg_text = event.get('text')
        user_id = event.get('user')
        channel_id = event.get('channel')
        message_timestamp :str = event.get('ts')
        thread_timestamp :str = event.get('event_ts') or message_timestamp
        bot_message_to_user = msg_client.send_message_from_slackbot_to_user(msg_text, channel_id=channel_id, user_id=user_id, thread_timestamp = thread_timestamp)
        return HttpResponse("Success", status=200)
    return HttpResponse("Success", status=200)
