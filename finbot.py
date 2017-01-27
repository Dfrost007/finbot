import json

from flask import Flask, request
import requests

app = Flask(__name__)

# Enter the Page Access Token
PAT = 'EAADEk32ZBIZCIBAIrX4yZBIxqs7m4A8DxiRpCTsoO4ati4zUNn0TG5qG59hwOoUPqqj8EuMGb9V0agZAdQKdVNhC8KUtpZB3nSf9bgHwheN7XTYNVal6IZBZBWwhCcM4xEw1ng201pfq4aGIfjWzWZCLhkEe32DPHoalrE3UUrcSMwZDZD'


@app.route('/', methods=['GET'])
def verification():
    print("Handling Verification.")
    if request.args.get('hub.verify_token', '') == 'i_am_hacker_so_be_careful':
        print("Verified")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling Messages")
    payload = request.get_data()
    print(payload)
    for sender, message in messaging_events(payload):
        print("Incoming from %s: %s" % (sender, message))
        if message == "texts":
            send_message(PAT, sender, message)
        if message == "images":
            send_image(PAT, sender)
        if message == "videos":
            send_video(PAT, sender)
        return "ok"


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
        yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """
    user_details_url = "https://graph.facebook.com/v2.6/%s" % recipient
    user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': token}
    user_details = requests.get(user_details_url, user_details_params).json()
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({"recipient": {"id": recipient},
                                       "message": {"text": text + user_details['first_name']}
                                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)


def send_image(token, recipient):
    """Send the message text to recipient with id recipient.
    """
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({"recipient": {"id": recipient},
                                       "message": {"attachment": {"type": "image", "payload": {"url": "http://cartoonbros.com/wp-content/uploads/2016/08/pikachu-13-150x150.png"}}}
                                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)


def send_video(token, recipient):
    """Send the message text to recipient with id recipient.
    """
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({"recipient": {"id": recipient},
                                       "message": {"attachment": {"type": "video", "payload": {"url": ""}}}
                                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)


if __name__ == '__main__':
    app.run()

