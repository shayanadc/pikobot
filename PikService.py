import PikAPI


def createOrFindUser(name, surname, username,telegram_username):
    data = convertArgsToDict(name=name, surname=surname, username=username,telegram_username=telegram_username)
    return PikAPI.createOrFindUser(data)


def creatorGroup(name, creator_id):
    data = convertArgsToDict(name=name, creator_id=creator_id)
    return PikAPI.creatorGroup(data)


def saveBill(description, cost, owner, group_id):
    data = convertArgsToDict(description=description, cost=cost, owner=owner, group_id=group_id)
    return PikAPI.saveBill(data)

def shareBill(bill_id,members):
    data = convertArgsToDict(bill_id=bill_id, members=members)
    return PikAPI.shareBill(data)

def attachUsersToGroup(group_id, users_id):
    data = convertArgsToDict(group_id=group_id, users_id=users_id)
    return PikAPI.attachUsersToGroup(data)


def settle(ledgID):
    data = {'settle' : True}
    return PikAPI.settle(str(ledgID),data)

def getGroupsOfUser(userId):
    return PikAPI.getUsersOfGroup(str(userId))

def findGroup(userId):
    return PikAPI.findGroup(str(userId))

def findLedger(user, **kwargs):
    data = '?user=' + str(user)
    for k, v in kwargs.items():
        data += '&' + str(k) + '=' + str(v)
    return PikAPI.findLedger(data)


def convertArgsToDict(**kwargs):
    # data = {}
    # for k,v in kwargs.items():
    #     data[str(k)] = str(v)
    return kwargs
