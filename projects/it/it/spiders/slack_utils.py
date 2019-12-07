def slack_send(data):
    slack_url = os.environ['IT_VIEC_SLACK_WEBHOOK_URL']
    headers = {'Content-type': 'application/json'}
    try:
        act = requests.post(
            slack_url,
            data=json.dumps(data),
            headers=headers)
    except act.exceptions.HTTPError as e:
        print(e)