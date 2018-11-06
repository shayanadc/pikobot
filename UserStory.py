import ast
from pymemcache.client import base
client = base.Client(('localhost', 11211))

def getUserStroy(chatId):
    cacheUser = client.get(str(chatId))
    if cacheUser is None:
        cacheUser = {}
        cacheUser['steps'] = {1: "welcome"}
        cacheUser['data'] = {}
    else:
        cacheUser = ast.literal_eval(cacheUser.decode())
    return cacheUser


def freshUserSteps(chatId):
    client.delete(str(chatId))

def getLastStep(chatId):
    userStory = getUserStroy(chatId)
    steps = userStory['steps']
    try:
        return max([*steps])
    except:
        return 1

def getUserShareToMembers(chatId):
    f = getUserStroy(chatId)
    members = []
    for mem in f['data']['shareTo']:
        members.append(mem['user_id'])
    return members

def isStoreData(chatId,data):
    f = getUserStroy(chatId)
    if str(data) in f['data']:
        return True
    return False

def storeData(chatId,data):
    f = getUserStroy(chatId)
    for k in data:
        if k in f['data']:
            if type(data[k]) != dict :
                f['data'].update(data)
            else:
                new = f['data'][k]
                new.update(data[k])
        else:
            f['data'].update(data)

    client.set(str(chatId), f)

def getLastStage(chatId):
    lastStepNumb = getLastStep(chatId)
    steps = getUserStroy(chatId)
    return steps['steps'][lastStepNumb]


def storeNewStep(chatId, stepName):
    userStory = getUserStroy(chatId)
    lastStep = getLastStep(chatId)
    newStep = lastStep + 1
    userStory['steps'][newStep] = str(stepName)
    client.set(str(chatId), userStory)
