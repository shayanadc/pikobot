import requests
import json

host = 'http://127.0.0.1:8000/'


def createOrFindUser(data):
    r = requests.post(host + 'api/users', data=data)
    return r.json()


def creatorGroup(data):
    r = requests.post(host + 'api/groups', data=data)
    return r.json()


def saveBill(data):
    r = requests.post(host + 'api/bills', data=data)
    return r.json()


def settle(ledgerId,data):
    headers = {'content-type': 'application/json'}
    r = requests.put(host + 'api/ledgers/'+ ledgerId, data=json.dumps(data), headers=headers)
    return r.json()

def attachUsersToGroup(data):
    r = requests.post(host + 'api/users/group', data=data)
    return r.json()


def findGroup(data):
    r = requests.get(host + 'api/groups/' + data)
    return r.json()

def findLedger(data):
    r = requests.get(host + 'api/ledgers' + data)
    return r.json()

def shareBill(data):
    headers = {'content-type': 'application/json'}
    r = requests.post(host + 'api/ledgers', data=json.dumps(data), headers=headers)
    return r.json()

def getUsersOfGroup(data):
    r = requests.get(host + 'api/groups/user/' + data)
    return r.json()
