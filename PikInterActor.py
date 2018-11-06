import PikService
def getUser(user):
    username = user['id']
    surname = None
    name = None
    telegram_username = None
    if 'last_name' in user:
        surname = user['last_name']
    if 'first_name' in user:
        name = user['first_name']
    if 'username' in user:
        telegram_username = user['username']
    return PikService.createOrFindUser(name,surname,username,telegram_username)

def createBillAndShare(userId,dataStory):
    #Todo: check data is ready
    #Todo: use phone number
    bill_desc = dataStory['description']
    bill_cost = dataStory['cost']
    user = PikService.createOrFindUser(None,None,userId,None)
    if 'group_id' in dataStory:
        groupId = dataStory['group_id']

    if 'group_name' in dataStory:
        group_name = dataStory['group_name']
        group = PikService.creatorGroup(group_name,user['id'])
        groupId = group['id']

    if 'shareToAll' in dataStory:
        shareUserIds = getUserIdsOfGroup(groupId)
    if 'shareTo' in dataStory:
        members = dataStory['shareTo']
        shareUsers = []
        for mem in members:
            member = members[mem]
            fname, lname =None,None
            if 'first_name' in member:
                fname = member['first_name']
            if 'last_name' in member:
                lname = member['last_name']
            userMem = PikService.createOrFindUser(fname,lname,member['user_id'],None)
            shareUsers.append(userMem)
        shareUserIds = [user['id']]
        for um in shareUsers:
            shareUserIds.append(um['id'])
        attach = PikService.attachUsersToGroup(groupId,shareUserIds)
    #check double attach to Group
    bill = PikService.saveBill(bill_desc,bill_cost,user['id'],groupId)
    divide = PikService.shareBill(bill['id'], shareUserIds)
    return divide

def getUsersOfGroup(id):
    group = PikService.findGroup(id)
    return group['users']

def getUserIdsOfGroup(userId):
    users = getUsersOfGroup(userId)
    userIds =[]
    for user in users:
        userIds.append(user['id'])
    return userIds

def getMyGroups(userId):
    user = PikService.createOrFindUser(None,None,userId,None)
    groups = PikService.getGroupsOfUser(user['id'])
    l = []
    item=[]
    for group in groups:
        callback_data = 'G'+ str(group['id'])
        item = [dict(text=group['name'],callback_data=callback_data)]
        l.append(item)
    return l

def getUserLedger(userId):
    user = PikService.createOrFindUser(None,None,userId,None)
    return PikService.findLedger(user['id'],ledger=True)

def getMyOwe(userId):
    all = getUserLedger(userId)
    if 'creditor' not in all or len(all) == 0: return None
    return all['creditor']

def getMyCreditor(userId):
    all = getUserLedger(userId)
    if 'owe' not in all or len(all) == 0: return None
    return all['owe']

def getUserOweButton(userId):
    userOwe = getMyOwe(userId)
    if userOwe is None: return None
    l = []
    item = []
    for v in userOwe:
        callback_data = 'O' + str(v['id'])
        item = [dict(text=v['name'], callback_data=callback_data)]
        l.append(item)
    return l

def getUserCreditorButton(userId):
    userCreditor = getMyCreditor(userId)
    if userCreditor is None: return None
    l = []
    item = []
    for v in userCreditor:
        callback_data = 'C' + str(v['id'])
        item = [dict(text=v['name'], callback_data=callback_data)]
        l.append(item)
    return l

def getTotalAccBetween(userTId, friendId):
    user = PikService.createOrFindUser(None, None, userTId, None)
    ledger = PikService.findLedger(user['id'],friend=friendId,calc=True)
    if ledger is None or len(ledger) == 0 : return 'clear'
    totalAmount = 0
    for l in ledger:
        if l['creditor'] == user['id']:
            totalAmount += float(l['amount'])
        if l['owe'] == user['id']:
            totalAmount -= float(l['amount'])

    if totalAmount is None : return 'clear'
    if totalAmount < 0:
        totalAmount = -int(totalAmount)
        statement = 'you are totally owe:' + str(totalAmount)
    if totalAmount > 0:
        statement = 'you are totally creditor:' + str(totalAmount)
    return statement

def getTotalAcc(userId):
    user = PikService.createOrFindUser(None,None,userId,None)
    ledger = PikService.findLedger(user['id'],calc=True)
    if ledger is None or len(ledger) == 0: return None
    totalAmount = 0
    for l in ledger:
        if l['creditor'] == user['id']:
            totalAmount += float(l['amount'])
        if l['owe'] == user['id']:
            totalAmount -= float(l['amount'])
    return totalAmount

def makeTotalAccStatement(userId):
    totalAmount = getTotalAcc(userId)
    if totalAmount is None : return 'clear'
    if totalAmount < 0:
        totalAmount = -int(totalAmount)
        statement = 'you are totally owe:' + str(totalAmount)
    if totalAmount > 0:
        statement = 'you are totally creditor:' + str(totalAmount)
    return statement

# def settle(userId):
