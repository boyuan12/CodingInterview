import requests
import json


def get_code_result(code, lang, input):
    data = requests.post("https://codexweb.netlify.app/.netlify/functions/enforceCode",
        data=json.dumps({"code": code, "language": lang, "input": input}),
        headers={'Content-Type': 'application/json'}
    ).json()

    return data
