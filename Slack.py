import requests
import json
import sys
import config

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
# Replace Token with the on in SLACK_TOKEN.txt
webhook_ = config.slackConfig.WEBHOOK
# SLACK_TOKEN = "xoxb-bottoken" # or a TEST token. Get one from https://api.slack.com/docs/oauth-test-tokens


def get_channel_id():
    channel_list = sc.api_call("channels.list")
    for each in channel_list['channels']:
        if each['name'] == 'general':
            return each['id']

# Post data to slack channel
def post(item):
    item_name = item['title']
    item_link = item['link']
    item_price = item['price']
    item_img = "{}{}".format("http://",item['img'][:-2])
    attachments = [{"title": item_name,
        "title_link":item_link,
        "fields": [{
            "title": "Retailer",
            "value": "Funko Shop"},{
            "title": "Price",
            "value": item_price},{
            "title": "Link",
            "value": item_link
            }
        ],
        "image_url": item_img }]
    # Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
    webhook_url = webhook_
    slack_data = attachments

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )
