import requests
import json


def list_rep(user_id):
    service = f'https://api.github.com/users/{user_id}/repos'
    req = requests.get(service, user_id)
    answer = json.loads(req.text)

    with open('answer.json', 'w') as f:
        json.dump(answer, f, indent=4)

    list_reps = []
    for i in answer:
        list_reps.append(i['name'])
    return list_reps


print(list_rep('thevasina'))
